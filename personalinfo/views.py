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


def toUlogin(request):
    return render(request, 'u_login.html')


def toAlogin(request):
    return render(request, 'a_login.html')


def u_Login(request):
    user = request.POST.get('user', '')
    pwd = request.POST.get('pwd', '')

    if user and pwd:
        state_u = Users.objects.filter(u_id=user, u_password=pwd).count()
        if state_u >= 1:
            u_name = Users.objects.get(u_id=user).u_name
            u_identity = Users.objects.get(u_id=user).identity
            value = {"id": user, "name": u_name, "identity": u_identity}
            # return HttpResponse("欢迎{} {}登入校园疫情防控信息管理系统".format(u_name, u_identity))
            return render(request, 'u_navigation.html', context=value)
        else:
            messages.error(request, "用户账号或密码有误")
            return HttpResponseRedirect(reverse('u_Login'))
            # return render(request, 'before_login.html')
    else:
        messages.error(request, "用户账号或密码不能为空")
        # return render(request, 'before_login.html')
        return HttpResponseRedirect(reverse('u_Login'))


def a_Login(request):
    user = request.POST.get('user', '')
    pwd = request.POST.get('pwd', '')

    if user and pwd:
        state_a = Admin.objects.filter(a_id=user, a_password=pwd).count()
        if state_a >= 1:
            # a_name = Admin.objects.get(a_id=user).a_name
            # value = {"name": a_name}
            # return HttpResponse("欢迎admin 管理员登入校园疫情防控信息管理系统".format(a_name))
            # return render(request, 'a_navigation.html')
            value = {"id": user}
            return render(request, 'a_navigation.html', context=value)
        else:
            messages.error(request, "管理员账号或密码有误")
            return HttpResponseRedirect(reverse('a_Login'))
            # return render(request, 'before_login.html')
    else:
        messages.error(request, "管理员账号或密码不能为空")
        # return render(request, 'before_login.html')
        return HttpResponseRedirect(reverse('a_Login'))


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


def u_return(request, u_id):
    data = Users.objects.get(u_id=u_id)
    value = {"id": data.u_id, "name": data.u_name, "identity": data.identity}
    return render(request, 'u_navigation.html', context=value)


def a_return(request):
    value = {"id": 'admin'}
    return render(request, 'a_navigation.html', context=value)


def logout(request):
    return render(request, 'before_login.html')


def to_batch(request):
    return render(request, "batch_upload.html")


def excel_upload(request):
    if request.method == "POST":
        f = request.FILES['my_file']
        type_excel = f.name.split('.')[1]
        if 'xls' == type_excel:
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            nrows = table.nrows
            try:
                with transaction.atomic():
                    for i in range(1, nrows):
                        rowValues = table.row_values(i)
                        userinfo = Users(u_id=str(rowValues[0])[:-2], u_name=str(rowValues[1]),
                                         u_password=str(rowValues[2])[:-2], identity=str(rowValues[3]),
                                         phone=str(rowValues[6])[:-2],
                                         email=str(rowValues[7]))
                        userinfo.save()
                        classinfo = Classes(u_id=str(rowValues[0])[:-2], classes=str(rowValues[4])[:-2])
                        dormitoryinfo = Dormitory(u_id=str(rowValues[0])[:-2], department=int(str(rowValues[5])[0:2]),
                                                  room_id=str(rowValues[5])[-3:])
                        healthinfo = Healthcode(u_id=str(rowValues[0])[:-2], healthcode='green')
                        passphrase = Passphrase(u_id=str(rowValues[0])[:-2], passphrase='yes')
                        classinfo.save()
                        dormitoryinfo.save()
                        healthinfo.save()
                        passphrase.save()
            except Exception as e:
                messages.error(request, "数据存在错误....")
                return HttpResponseRedirect(reverse('batch'))
                # return HttpResponse('数据存在错误....')

            messages.error(request, "上传成功")
            return HttpResponseRedirect(reverse('batch'))
            # return HttpResponse('上传成功')

        messages.error(request, "上传文件格式不是xls")
        return HttpResponseRedirect(reverse('batch'))
        # return HttpResponse('上传文件格式不是xls')

    messages.error(request, "不是post请求")
    return HttpResponseRedirect(reverse('batch'))
    # return HttpResponse('不是post请求')


def u_info(request, u_id):
    data = Users.objects.get(u_id=u_id)
    cla = Classes.objects.get(u__u_id=u_id)
    dor = Dormitory.objects.get(u__u_id=u_id)
    judge = Judge.objects.filter(u_id=u_id).order_by('-id')
    interfacciami = Interfacciami.objects.filter(u_id=u_id).count()
    quarantine = Quarantine.objects.filter(u_id=u_id)
    passphrase = Passphrase.objects.get(u_id=u_id)
    o_code = Healthcode.objects.get(u_id=u_id)
    code = o_code.healthcode
    if code == "green":
        code = "绿码"
    elif code == "yellow":
        code = "黄码"
    else:
        code = "红码"
    state = ""
    situation = ""
    l_time = ""
    for line in judge:
        if line.state == 1:
            state = "同意"
        elif line.state == 2:
            state = "不同意"
        else:
            state = "未审核"
        if line.situation == 0:
            situation = "未出门"
        else:
            situation = "已过期"
        l_time = line.l_time
        break
    q1 = "暂时无隔离数据"
    q2 = "暂时无隔离数据"
    for line in quarantine:
        q1 = line.q_location
        q2 = line.cancel_time
        break

    value = {'id': u_id, 'name': data.u_name, 'identity': data.identity, 'phone': data.phone, 'email': data.email,
             'year': u_id[:4], 'class': cla.classes, 'dor': str(dor.department) + dor.room_id, 'j1': state,
             'j2': l_time, 'j3': situation, 'interfacciami': interfacciami, 'code': code, 'q1': q1, 'q2': q2,
             'passphrase': passphrase.passphrase}
    return render(request, 'u_information.html', context=value)


def a_u_info(request):
    u_id = request.POST.get('id', '')
    t_info = []
    if u_id:
        data = Users.objects.get(u_id=u_id)
        t_info = [[data.u_id, data.u_name, data.identity, data.phone, data.email]]
    else:
        data = Users.objects.all()
        for line in data:
            l_info = [line.u_id, line.u_name, line.identity, line.phone, line.email]
            t_info.append(l_info)
    return render(request, 'a_u_info.html', {'data': t_info})


def a_dayclock_info(request):
    u_id = request.POST.get('id', '')
    t_info = []
    t_year=datetime.date.today().year
    t_month = datetime.date.today().month
    t_day = datetime.date.today().day
    if u_id:
        data = DailyClock.objects.filter(u_id=u_id).order_by('c_time')
    else:
        data = DailyClock.objects.all().order_by('c_time')
    for line in data:
        date_time = line.c_time
        c_year = date_time.year
        c_month = date_time.month
        c_day = date_time.day
        if c_year == t_year and c_month == t_month and c_day == t_day:
            situation = "已打卡"
            clock_time = line.c_time
        else:
            situation = "未打卡"
            clock_time = "无"
        l_info = {"u_id": line.u_id, "situation": situation, "c_time": clock_time, }
        t_info.append(l_info)
    return render(request, "a_dayclock_info.html",{'data': t_info})


def a_day_clock(request,u_id):

    t_info = []
    if u_id:
        data = DailyClock.objects.filter(u_id=u_id).order_by('id')
        for line in data:
            l_info = [line.u_id, line.temperature, line.qrcode, line.emergency_phone,line.c_time]
            t_info.append(l_info)
    else:
        data = DailyClock.objects.all()
        for line in data:
            l_info = [line.u_id, line.temperature, line.qrcode, line.emergency_phone,line.c_time]
            t_info.append(l_info)
    return render(request, 'a_day_clock.html', {'data': t_info})


def a_examine(request):
    u_id = request.POST.get('id', '')
    t_info = []
    if u_id:
        data = Judge.objects.filter(u_id=u_id).order_by('-id')
    else:
        data = Judge.objects.all().order_by('-id')
    for line in data:
        if line.state == 1:
            state = "同意"
        elif line.state == 2:
            state = "不同意"
        else:
            state = "未审核"
        if line.situation == 0:
            situation = "未出门"
        else:
            situation = "已过期"
        l_info = {"id": line.id, "u_id": line.u_id, "l_time": line.l_time, "reason": line.reason, "states": state,
                  "situation": situation}
        t_info.append(l_info)
    return render(request, 'a_examine.html', {'data': t_info})


def a_quarantine_info(request):
    u_id = request.POST.get('id', '')
    t_info = []
    if u_id:
        data = Quarantine.objects.filter(u_id=u_id).order_by('-id')
    else:
        data = Quarantine.objects.all().order_by('-id')
    for line in data:

        l_info = { "u_id": line.u_id, "q_location": line.q_location ,"cancel_time": line.cancel_time,}
        t_info.append(l_info)
    return render(request, 'a_quarantine_info.html', {'data': t_info})


def a_t_quarantine(request):
    u_id = request.POST.get('id', '')
    t_info = []
    if u_id:
        data = TQuarantine.objects.filter(u_id=u_id).order_by('-id')
    else:
        data = TQuarantine.objects.all().order_by('-id')
    for line in data:
        l_info = { "u_id": line.u_id, "q_location": line.q_location ,"i_time": line.i_time,"o_time":line.o_time}
        t_info.append(l_info)
    return render(request, 'a_t_quarantine.html', {'data': t_info})


def to_a_quarantine_up(request):
    return render(request, 'a_quarantine_up.html')


def a_quarantine_up(request):
    u_id = request.POST.get('u_id', '')
    q_location = request.POST.get('q_location', '')
    cancel_time = request.POST.get('cancel_time')
    Quarantine.objects.create(u_id=u_id,q_location=q_location,cancel_time=cancel_time)
    return HttpResponseRedirect(reverse('a_quarantine_up'))


def to_a_f_examine(request, l_id):
    return render(request, 'a_f_examine.html', {'l_id': l_id})


def a_f_examine(request, l_id):
    state = request.POST.get('state', '')
    Judge.objects.filter(id=l_id).update(state=state)
    return HttpResponseRedirect(reverse('a_examine'))


def a_inout_query(request):
    u_id = request.POST.get('id', '')
    t_info = []
    if u_id:
        data = Iotable.objects.filter(u_id=u_id).order_by('-io_time')
        for line in data:
            if line.in_out == 1:
                in_out = "进"
            else:
                in_out = "出"
            l_info = [line.u_id, in_out, line.io_time, line.door_id]
            t_info.append(l_info)
    else:
        data = Iotable.objects.all()
        for line in data:
            if line.in_out == 1:
                in_out = "进"
            else:
                in_out = "出"
            l_info = [line.u_id, in_out, line.io_time, line.door_id]
            t_info.append(l_info)
    return render(request, 'a_inout_query.html', {'data': t_info})


def to_u_schedul(request, u_id):
    time = get_now_time()
    value = {'id': u_id, 'time': time}
    return render(request, 'u_schedul.html', context=value)


def u_schedul(request, u_id):
    time = get_now_time()
    p = request.POST.get('province', '')
    c = request.POST.get('city', '')
    d = request.POST.get('district', '')
    l = request.POST.get('location', '')
    schedule = USchedule(u_id=u_id, location=p + c + d + l, o_time=time)
    schedule.save()
    data = Users.objects.get(u_id=u_id)
    value = {"id": data.u_id, "name": data.u_name, "identity": data.identity}
    return render(request, 'u_navigation.html', context=value)


def to_u_go_out(request, u_id):
    value = {'id': u_id}
    return render(request, 'u_go_out.html', context=value)


def u_go_out(request, u_id):
    time = request.POST.get('time', '')
    reason = request.POST.get('reason', '')
    judge = Judge(u_id=u_id, l_time=int(time), reason=reason, state=0, situation=0)
    judge.save()
    data = Users.objects.get(u_id=u_id)
    value = {"id": data.u_id, "name": data.u_name, "identity": data.identity}
    return render(request, 'u_navigation.html', context=value)


def to_u_covid_test(request, u_id):
    value = {'id': u_id}
    return render(request, 'u_covid_test.html', context=value)


def u_covid_test(request, u_id):
    result = request.POST.get('value', '')
    time = get_now_time()
    cov_test = NucleicAcid(u_id=u_id, t_time=time, result=result)
    cov_test.save()
    data = Users.objects.get(u_id=u_id)
    value = {"id": data.u_id, "name": data.u_name, "identity": data.identity}
    return render(request, 'u_navigation.html', context=value)


def to_u_daycard(request, u_id):
    time = get_now_time()
    data = Healthcode.objects.get(u_id=u_id)
    code = data.healthcode
    b_time = DailyClock.objects.filter(u_id=u_id).order_by('-id')
    be_time = ""
    for line in b_time:
        be_time = line.c_time
        break
    if code == "green":
        code = "绿码"
    elif code == "yellow":
        code = "黄码"
    else:
        code = "红码"
    value = {'id': u_id, 'time': time, 'code': code, 'b_time': be_time}
    return render(request, 'u_daycard.html', context=value)


def u_daycard(request, u_id):
    time = get_now_time()
    temperature = request.POST.get('temp', '')
    emergency_person = request.POST.get('en', '')
    emergency_phone = request.POST.get('ep', '')
    data = Healthcode.objects.get(u_id=u_id)
    code = data.healthcode
    data = Users.objects.get(u_id=u_id)
    b_time = DailyClock.objects.filter(u_id=u_id).order_by('-id')
    be_time = ""
    for line in b_time:
        be_time = line.c_time
        break
    if code == "green":
        code = "绿码"
    elif code == "yellow":
        code = "黄码"
    else:
        code = "红码"
    value = {"id": data.u_id, "name": data.u_name, "identity": data.identity, 'time': time, 'code': code,
             'b_time': be_time}
    if str(time)[:10] == str(be_time)[:10]:
        messages.error(request, "您今天已完成打卡，请勿重复打卡")
        return render(request, 'u_daycard.html', context=value)
    else:
        code = data.healthcode
        daycard = DailyClock(u_id=u_id, temperature=float(temperature), emergency_person=emergency_person,
                             emergency_phone=emergency_phone, c_time=time, qrcode=code)
        daycard.save()

    return render(request, 'u_navigation.html', context=value)


def to_u_inout_door(request, u_id):
    time = get_now_time()
    value = {'id': u_id, 'time': time}
    return render(request, 'u_inout_door.html', context=value)


def u_inout_door(request, u_id):
    io = request.POST.get('i_o', '')
    door = request.POST.get('door', '')
    time = get_now_time()
    data = Users.objects.get(u_id=u_id)
    value = {"id": data.u_id, "name": data.u_name, "identity": data.identity, "time": time}
    state = 1
    if io == "出":
        io = 0
    else:
        io = 1
    date = Iotable.objects.filter(u_id=u_id).order_by('-id')
    for line in date:
        state = line.state
        break
    date = Passphrase.objects.get(u_id=u_id)
    passphrase = date.passphrase
    if passphrase == "yes":
        if state == 1:
            if io == 0:
                iotable = Iotable(u_id=u_id, in_out=io, io_time=time, door_id=door, state=0)
                iotable.save()
                return render(request, 'u_navigation.html', context=value)
            else:
                messages.error(request, "您还未出门")
                return render(request, 'u_inout_door.html', context=value)
        else:
            if io == 0:
                messages.error(request, "您已出门")
                return render(request, 'u_inout_door.html', context=value)
            else:
                iotable = Iotable(u_id=u_id, in_out=io, io_time=time, door_id=door, state=1)
                Iotable.objects.filter(u_id=u_id).update(state=1)
                iotable.save()
                return render(request, 'u_navigation.html', context=value)
    else:
        messages.error(request, "您目前没有通行码，无法出入校门")
        return render(request, 'u_inout_door.html', context=value)


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
        print(detail_time)
        days = (end - start).days
        hours = str(detail_time).split(',')[1].split(':')[0].replace(' ', '')
        minutes = str(detail_time).split(',')[1].split(':')[1]
        real_hours = -(days * 24 + int(hours) + float(int(minutes)/60))
        judge = Judge.objects.filter(state=1, situation=0, u_id=line1.u_id)
        j_hours = 2
        for line2 in judge:
            j_hours = line2.l_time
        print(j_hours, real_hours)
        if real_hours == j_hours:
            name = Users.objects.get(u_id=line1.u_id).u_name
            identity = Users.objects.get(u_id=line1.u_id).identity
            mail = Users.objects.get(u_id=line1.u_id).email
            content = "{}{}，您出校已超过规定时间，目前您的通行码被停用，请及时联系管理员！".format(name, identity)
            send_email(content=content, email=mail)
            Passphrase.objects.filter(u_id=line1.u_id).update(passphrase="no")
        Judge.objects.filter(state=1, situation=0, u_id=line1.u_id).update(situation=1)

    return 0


def send_email(content, email):
    # 值1：  邮件标题   值2： 邮件主体
    # 值3： 发件人      值4： 收件人
    send_mail('防疫系统提示',
              content,
              '2477911988@qq.com',
              [email])
