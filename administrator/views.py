from personalinfo.views import *


def toAlogin(request):
    return render(request, 'a_login.html')


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


def a_return(request):
    value = {"id": 'admin'}
    return render(request, 'a_navigation.html', context=value)


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
    t_year = str(datetime.date.today().year).zfill(4)
    t_month = str(datetime.date.today().month).zfill(2)
    t_day = str(datetime.date.today().day).zfill(2)
    now_date = "{}-{}-{}%%".format(t_year, t_month, t_day)
    d_id = DailyClock.objects.raw("select * from daily_clock where c_time like %s", [now_date])
    if u_id:
        t_id = Users.objects.filter(u_id=u_id)
    else:
        t_id = Users.objects.all()
    situation = ""
    clock_time = ""
    for line in t_id:
        yes = 0
        for i in d_id:
            if line.u_id == i.u_id:
                situation = "已打卡"
                clock_time = i.c_time
                yes = 1
                break
        if yes == 0:
            situation = "未打卡"
            clock_time = " "
        l_info = {"u_id": line.u_id, "situation": situation, "c_time": clock_time}
        t_info.append(l_info)
    return render(request, "a_dayclock_info.html", {'data': t_info})


def a_day_clock(request, u_id):
    t_info = []
    if u_id:
        data = DailyClock.objects.filter(u_id=u_id).order_by('id')
        for line in data:
            l_info = [line.u_id, line.temperature, line.qrcode, line.emergency_phone, line.c_time]
            t_info.append(l_info)
    else:
        data = DailyClock.objects.all()
        for line in data:
            l_info = [line.u_id, line.temperature, line.qrcode, line.emergency_phone, line.c_time]
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
        l_info = {"u_id": line.u_id, "q_location": line.q_location, "cancel_time": line.cancel_time, }
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
        l_info = {"u_id": line.u_id, "q_location": line.q_location, "i_time": line.i_time, "o_time": line.o_time}
        t_info.append(l_info)
    return render(request, 'a_t_quarantine.html', {'data': t_info})


def to_a_quarantine_up(request):
    return render(request, 'a_quarantine_up.html')


def a_quarantine_up(request):
    u_id = request.POST.get('u_id')
    q_location = request.POST.get('q_location')
    cancel_time = request.POST.get('cancel_time')
    Quarantine.objects.create(u_id=u_id, q_location=q_location, cancel_time=cancel_time)
    return HttpResponseRedirect(reverse('to_a_quarantine_up'))


def to_a_passphrase_up(request):
    t_info = []
    data = Passphrase.objects.all().order_by('passphrase')
    for line in data:
        if line.passphrase == 'no':
            passphrase = '无效'
        else:
            passphrase = '有效'
        l_info = {"u_id": line.u_id, "passphrase": passphrase}
        t_info.append(l_info)
    return render(request, 'a_passphrase_up.html', {'data': t_info})


def a_passphrase_up(request, l_id):
    Passphrase.objects.filter(u_id=l_id).update(passphrase='yes')
    return HttpResponseRedirect(reverse('to_a_passphrase_up'))


def to_a_healthcode_up(request):
    t_info = []
    data = Healthcode.objects.all().order_by('healthcode')
    for line in data:
        if line.healthcode == 'red':
            healthcode = '红色'
        elif line.healthcode == 'green':
            healthcode = '绿色'
        else:
            healthcode = '黄色'
        l_info = {"u_id": line.u_id, "healthcode": healthcode}
        t_info.append(l_info)
    return render(request, 'a_healthcode_up.html', {'data': t_info})


def a_healthcode_up(request, l_id):
    Passphrase.objects.filter(u_id=l_id).update(passphrase='yes')
    Healthcode.objects.filter(u_id=l_id).update(healthcode='green')
    return HttpResponseRedirect(reverse('to_a_healthcode_up'))


def to_a_covlocation_up(request):
    p = request.POST.get('province', '')
    c = request.POST.get('city', '')
    d = request.POST.get('district', '')
    covlocation = p + c + d
    t_info = []

    c_year = request.POST.get('year')
    c_month = request.POST.get('month')
    c_day = request.POST.get('day')
    data = USchedule.objects.filter(location=covlocation)
    for line in data:
        o_year = int(line.o_time.year)
        o_month = int(line.o_time.month)
        o_day = int(line.o_time.day)
        print(type(line.o_time.year))
        if int(c_year) == o_year and int(c_month) == o_month and int(c_day) == o_day:
            l_info = {"u_id": line.u_id, "covlocation": line.location, "o_time": line.o_time}
            t_info.append(l_info)
    return render(request, 'a_covlocation_up.html', {'data': t_info})


def a_covlocation_up(request, l_id):
    Passphrase.objects.filter(u_id=l_id).update(passphrase='no')
    Healthcode.objects.filter(u_id=l_id).update(healthcode='red')
    return HttpResponseRedirect(reverse('to_a_covlocation_up'))


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
