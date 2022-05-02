from personalinfo.views import *


def toUlogin(request):
    return render(request, 'u_login.html')


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


def u_return(request, u_id):
    data = Users.objects.get(u_id=u_id)
    value = {"id": data.u_id, "name": data.u_name, "identity": data.identity}
    return render(request, 'u_navigation.html', context=value)


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
             'j2': l_time, 'j3': situation, 'interfacciami': interfacciami, 'code': code, 'q1': q1, 'q2': str(q2)[:10],
             'passphrase': passphrase.passphrase}
    return render(request, 'u_information.html', context=value)


def to_u_schedul(request, u_id):
    time = get_now_time()
    data = Users.objects.get(u_id=u_id)
    value = {'id': u_id, 'name': data.u_name, 'identity': data.identity, 'time': str(time)}
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
    data = Users.objects.get(u_id=u_id)
    value = {'id': u_id, "name": data.u_name, "identity": data.identity}
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
    data = Users.objects.get(u_id=u_id)
    value = {'id': u_id, "name": data.u_name, "identity": data.identity}
    return render(request, 'u_covid_test.html', context=value)


def u_covid_test(request, u_id):
    result = request.POST.get('value', '')
    time = get_now_time()
    cov_test = NucleicAcid(u_id=u_id, t_time=time, result=result)
    cov_test.save()
    if result == "1":
        Healthcode.objects.filter(u_id=u_id).update(healthcode="red")
        Passphrase.objects.filter(u_id=u_id).update(passphrase="no")
        if Quarantine.objects.filter(u_id=u_id).count() == 1:
            Quarantine.objects.filter(u_id=u_id).delete()
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
    data = Users.objects.get(u_id=u_id)
    value = {'id': u_id, "name": data.u_name, "identity": data.identity, 'time': str(time), 'code': code, 'b_time': str(be_time)[:-6]}
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
    value = {"id": data.u_id, "name": data.u_name, "identity": data.identity, 'time': str(time), 'code': code,
             'b_time': str(be_time)[:-6]}
    if str(time)[:10] == str(be_time)[:10]:
        messages.error(request, "您今天已完成打卡，请勿重复打卡")
        return render(request, 'u_daycard.html', context=value)
    else:
        data = Healthcode.objects.get(u_id=u_id)
        code = data.healthcode
        daycard = DailyClock(u_id=u_id, temperature=float(temperature), emergency_person=emergency_person,
                             emergency_phone=emergency_phone, c_time=time, qrcode=code)
        daycard.save()

    return render(request, 'u_navigation.html', context=value)


def to_u_inout_door(request, u_id):
    data = Users.objects.get(u_id=u_id)
    time = get_now_time()
    value = {'id': u_id, "name": data.u_name, "identity": data.identity, 'time': str(time)}
    return render(request, 'u_inout_door.html', context=value)


def u_inout_door(request, u_id):
    io = request.POST.get('i_o', '')
    door = request.POST.get('door')
    time = get_now_time()
    data = Users.objects.get(u_id=u_id)
    value = {"id": data.u_id, "name": data.u_name, "identity": data.identity, "time": str(time)}
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
                Judge.objects.filter(state=1, situation=0, u_id=u_id).update(situation=1)
                return render(request, 'u_navigation.html', context=value)
    else:
        messages.error(request, "您目前没有通行码，无法出入校门")
        return render(request, 'u_inout_door.html', context=value)


def u_interfacciami(request, u_id):
    t_info = []
    data = Interfacciami.objects.filter(u_id=u_id).order_by('-id')
    for line in data:
        l_info = [line.reason, str(line.time)[:-6]]
        t_info.append(l_info)
    data = Users.objects.get(u_id=u_id)
    return render(request, 'u_interfacciami.html', {'data': t_info, 'id': u_id, "name": data.u_name, "identity": data.identity})


def u_my_schedule(request, u_id):
    t_info = []
    data = USchedule.objects.filter(u_id=u_id).order_by('-id')
    for line in data:
        l_info = [line.location, str(line.o_time)[:-6]]
        t_info.append(l_info)
    data = Users.objects.get(u_id=u_id)
    return render(request, 'u_my_schedule.html', {'data': t_info, 'id': u_id, "name": data.u_name, "identity": data.identity})
