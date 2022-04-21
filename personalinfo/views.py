import datetime

import xlrd
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from personalinfo.models import *


def toLogin(request):
    return render(request, 'before_login.html')


def toRegister(request):
    return render(request, 'register.html')


def Register(request):
    r_name = request.POST.get('name', '')
    r_pwd = request.POST.get('pwd', '')
    r_identity = request.POST.get('identity', '')
    r_in_year = request.POST.get('in_year', '')
    r_classes = request.POST.get('classes', '')
    r_dormitory = request.POST.get('dormitory', '')
    r_phone = request.POST.get('phone', '')
    r_email = request.POST.get('email', '')
    num = Classes.objects.filter(classes=r_classes).count()

    try:
        if r_name and r_pwd and r_identity and r_in_year and r_classes and r_dormitory and r_phone and r_email:
            r_id = r_in_year + r_classes + str(num).rjust(2, '0')
            state = Users.objects.filter(u_id=r_id).count()
            if state == 0:
                userinfo = Users(u_id=r_id, u_name=r_name, u_password=r_pwd, identity=r_identity, phone=r_phone,
                                 email=r_email)
                userinfo.save()
                classinfo = Classes(u_id=r_id, classes=r_classes)
                dormitoryinfo = Dormitory(u_id=r_id, department=int(r_dormitory[0:2]), room_id=r_dormitory[-3:])
                healthinfo = Healthcode(u_id=r_id, healthcode='green')
                passphrase = Passphrase(u_id=r_id, passphrase='yes')
                classinfo.save()
                dormitoryinfo.save()
                healthinfo.save()
                passphrase.save()
                value = {"id": r_id}
                # return HttpResponse("注册成功,你的id为{}".format(r_id))
                return render(request, 'u_login.html', context=value)
            else:
                messages.error(request, "该用户已存在，请重新注册")
                return HttpResponseRedirect(reverse('to_Register'))
                # return HttpResponse("该用户已存在，请重新注册")
        else:
            messages.error(request, "请输入完整信息")
            return HttpResponseRedirect(reverse('to_Register'))
            # return HttpResponse("请输入完整信息")
    except:
        messages.error(request, "系统目前出现故障，请稍后重试")
        return HttpResponseRedirect(reverse('to_Register'))
        # return HttpResponse("系统目前出现故障，请稍后重试")


def logout(request):
    return render(request, 'before_login.html')


def get_now_time():
    from django.utils import timezone
    import pytz
    import datetime
    tz = pytz.timezone('Asia/Shanghai')

    now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    return now


def monitor(request):
    # 监测出入校门
    now_time = get_now_time()
    io_date = Iotable.objects.filter(state=0)
    for line1 in io_date:
        start = datetime.datetime.strptime(str(now_time), "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(str(line1.io_time)[:-6], "%Y-%m-%d %H:%M:%S")
        detail_time = end - start
        days = (end - start).days
        hours = str(detail_time).split(',')[1].split(':')[0].replace(' ', '')
        minutes = str(detail_time).split(',')[1].split(':')[1]
        real_hours = -(days * 24 + int(hours) + float(int(minutes) / 60))
        judge = Judge.objects.filter(state=1, situation=0, u_id=line1.u_id)
        j_hours = 2
        for line2 in judge:
            j_hours = line2.l_time
        if real_hours == j_hours:
            name = Users.objects.get(u_id=line1.u_id).u_name
            identity = Users.objects.get(u_id=line1.u_id).identity
            mail = Users.objects.get(u_id=line1.u_id).email
            content = "{}{}，您出校已超过规定时间，目前您的通行码被停用，请及时联系管理员！".format(name, identity)
            send_email(content=content, email=mail)
            Passphrase.objects.filter(u_id=line1.u_id).update(passphrase="no")
        Judge.objects.filter(state=1, situation=0, u_id=line1.u_id).update(situation=1)
    # 监测每日打卡
    now_time = get_now_time()
    now_time = datetime.datetime.strptime(str(now_time), "%Y-%m-%d %H:%M:%S")
    if int(now_time.hour) == 21 and int(now_time.minute) == 38:
        t_year = str(datetime.date.today().year).zfill(4)
        t_month = str(datetime.date.today().month).zfill(2)
        t_day = str(datetime.date.today().day).zfill(2)
        now_date = "{}-{}-{}%%".format(t_year, t_month, t_day)
        d_id = DailyClock.objects.raw("select * from daily_clock where c_time like %s", [now_date])
        t_id = Users.objects.all()
        for line in t_id:
            yes = 0
            for i in d_id:
                if line.u_id == i.u_id:
                    yes = 1
                    break
            if yes == 0:
                name = Users.objects.get(u_id=line.u_id).u_name
                identity = Users.objects.get(u_id=line.u_id).identity
                mail = Users.objects.get(u_id=line.u_id).email
                content = "{}{}，您当日未进行打卡，目前您的通行码被停用，请及时联系管理员！".format(name, identity)
                send_email(content=content, email=mail)
                Passphrase.objects.filter(u_id=line.u_id).update(passphrase="no")

    return HttpResponse('secret')


def send_email(content, email):
    # 值1：  邮件标题   值2： 邮件主体
    # 值3： 发件人      值4： 收件人
    send_mail('防疫系统提示',
              content,
              '2477911988@qq.com',
              [email])
