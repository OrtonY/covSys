from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from personalinfo.models import Users, Admin, Classes, Dormitory


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
                classinfo.save()
                dormitoryinfo.save()
                value = {"id": r_id}
                # return HttpResponse("注册成功,你的id为{}".format(r_id))
                return render(request, 'u_login.html', context=value)
            else:
                return HttpResponse("该用户已存在，请重新注册")
        else:
            return HttpResponse("请输入完整信息")
    except:
        return HttpResponse("系统目前出现故障，请稍后重试")


def u_return(request, u_id):
    data = Users.objects.get(u_id=u_id)
    value = {"id": data.u_id, "name": data.u_name, "identity": data.identity}
    return render(request, 'u_navigation.html', context=value)


def a_return(request):
    value = {"id": 'admin'}
    return render(request, 'a_navigation.html', context=value)


def logout(request):
    return render(request, 'before_login.html')


def u_info(request, u_id):
    data = Users.objects.get(u_id=u_id)
    cla = Classes.objects.get(u__u_id=u_id)
    dor = Dormitory.objects.get(u__u_id=u_id)
    value = {'id': u_id, 'name': data.u_name, 'identity': data.identity, 'phone': data.phone, 'email': data.email,
             'year': u_id[:4], 'class': cla.classes, 'dor': str(dor.department) + dor.room_id}
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


def a_bed_check(request):
    return render(request, 'a_bed_check.html')


def a_day_clock(request):
    return render(request, 'a_day_clock.html')


def a_health_query(request):
    return render(request, 'a_health_query.html')


def a_inout_query(request):
    return render(request, 'a_inout_query.html')
