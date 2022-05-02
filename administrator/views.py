import xlrd
from django.db import transaction
from dateutil.relativedelta import relativedelta
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
            # date = u_count()
            # value = {"id": user, 'date': date}
            # return render(request, 'a_navigation.html', context=value)
            return HttpResponseRedirect(reverse('a_return'))
        else:
            messages.error(request, "管理员账号或密码有误")
            return HttpResponseRedirect(reverse('a_Login'))
            # return render(request, 'before_login.html')
    else:
        messages.error(request, "管理员账号或密码不能为空")
        # return render(request, 'before_login.html')
        return HttpResponseRedirect(reverse('a_Login'))


def a_return(request):
    data = []
    num = []
    t_id = Users.objects.all()
    for i in range(7):
        c_date = (datetime.date.today() - relativedelta(days=i)).strftime("%Y-%m-%d")
        d_id = DailyClock.objects.raw("select * from daily_clock where c_time like %s", [c_date+"%%"])
        a_count = 0
        for line in t_id:
            yes = 0
            for line1 in d_id:
                if line.u_id == line1.u_id:
                    yes = 1
                    a_count = a_count + 1
                    print(line1.u_id)
                    break
        data.append(c_date)
        num.append(a_count)
    date = list(data)
    num = list(num)
    return render(request, 'a_navigation.html', {"id": 'admin', 'date': date, 'num': num})


def to_batch(request):
    return render(request, "a_navigation.html")


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

                        Users.objects.create(u_id=str(rowValues[0])[:-2], u_name=str(rowValues[1]),
                                             u_password=str(rowValues[2])[:-2], identity=str(rowValues[3]),
                                             phone=str(rowValues[6])[:-2],
                                             email=str(rowValues[7]))
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
                messages.error(request, "数据已存在或是存在错误....")
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
                clock_time = str(i.c_time)[:-6]
                yes = 1
                break
        if yes == 0:
            situation = "未打卡"
            clock_time = " "
        name = Users.objects.get(u_id=line.u_id).u_name
        l_info = {"u_id": line.u_id, "name": name, "situation": situation, "c_time": clock_time}
        t_info.append(l_info)
    return render(request, "a_dayclock_info.html", {'data': t_info})


def a_day_clock(request, u_id):
    t_info = []
    data = DailyClock.objects.filter(u_id=u_id).order_by('-id')
    for line in data:
        name = Users.objects.get(u_id=line.u_id).u_name
        l_info = [line.u_id, name, line.temperature, line.qrcode, line.emergency_phone, str(line.c_time)[:-6]]
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
        name = Users.objects.get(u_id=line.u_id).u_name
        l_info = {"id": line.id, "u_id": line.u_id, "name": name, "l_time": line.l_time, "reason": line.reason,
                  "states": state,
                  "situation": situation}
        t_info.append(l_info)
    return render(request, 'a_examine.html', {'data': t_info})


def to_a_f_examine(request, l_id):
    return render(request, 'a_f_examine.html', {'l_id': l_id})


def a_f_examine(request, l_id):
    state = request.POST.get('value')
    print(state)
    Judge.objects.filter(id=l_id).update(state=state)
    return HttpResponseRedirect(reverse('a_examine'))


def a_t_quarantine(request):
    u_id = request.POST.get('id', '')
    t_info = []
    if u_id:
        data = TQuarantine.objects.filter(u_id=u_id).order_by('-id')
    else:
        data = TQuarantine.objects.all().order_by('-id')
    for line in data:
        name = Users.objects.get(u_id=line.u_id).u_name
        l_info = {"u_id": line.u_id, "name": name, "q_location": line.q_location, "i_time": str(line.i_time)[:10],
                  "o_time": str(line.o_time)[:10]}
        t_info.append(l_info)
    return render(request, 'a_t_quarantine.html', {'data': t_info})


def to_a_quarantine_up(request, u_id):
    date = Quarantine.objects.get(u_id=u_id)
    value = {'id': u_id, 'location': date.q_location, 'time': str(date.cancel_time)[:10]}
    return render(request, 'a_quarantine_up.html', context=value)


def to_a_quarantine_list_up(request):
    u = request.POST.get('id', '')
    date = Healthcode.objects.filter(healthcode='yellow')
    t_info = []
    if u:
        t_date = Quarantine.objects.filter(u_id=u).order_by('-id')
        for l_line in t_date:
            name = Users.objects.get(u_id=l_line.u_id).u_name
            l_info = {'id': l_line.u_id, 'name': name, 'location': l_line.q_location,
                      'time': str(l_line.cancel_time)[:10]}
            t_info.append(l_info)
    else:
        for line in date:
            t_date = Quarantine.objects.filter(u_id=line.u_id)
            for l_line in t_date:
                name = Users.objects.get(u_id=l_line.u_id).u_name
                l_info = {'id': l_line.u_id, 'name': name, 'location': l_line.q_location,
                          'time': str(l_line.cancel_time)[:10]}
                t_info.append(l_info)
    return render(request, 'a_quarantine_list_up.html', {'data': t_info})


def a_quarantine_up(request, u_id):
    q_location = request.POST.get('q_location')
    cancel_time = request.POST.get('cancel_time')
    now = get_now_time()
    Quarantine.objects.filter(u_id=u_id).update(q_location=q_location, cancel_time=cancel_time)
    t_id = Quarantine.objects.get(u_id=u_id).id
    count = TQuarantine.objects.filter(id=t_id).count()
    if count == 0:
        TQuarantine.objects.create(u_id=u_id, q_location=q_location, i_time=now, o_time=cancel_time, id=t_id)
    else:
        TQuarantine.objects.filter(u_id=u_id, id=t_id).update(q_location=q_location, o_time=cancel_time)
    return HttpResponseRedirect(reverse('a_quarantine_list_up'))


def to_a_passphrase_up(request):
    t_info = []
    data = Passphrase.objects.all().order_by('passphrase')
    for line in data:
        if line.passphrase == 'no':
            passphrase = '无效'
        else:
            passphrase = '有效'
        name = Users.objects.get(u_id=line.u_id).u_name
        l_info = {"u_id": line.u_id, "name": name, "passphrase": passphrase}
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
        name = Users.objects.get(u_id=line.u_id).u_name
        l_info = {"u_id": line.u_id, "name": name, "healthcode": healthcode}
        t_info.append(l_info)
    return render(request, 'a_healthcode_up.html', {'data': t_info})


def a_healthcode_up(request, l_id):
    Passphrase.objects.filter(u_id=l_id).update(passphrase='yes')
    Healthcode.objects.filter(u_id=l_id).update(healthcode='green')
    return HttpResponseRedirect(reverse('to_a_healthcode_up'))


def to_a_covlocation_up(request):
    return render(request, 'a_covlocation_up.html')


def a_covlocation_up(request):
    p = request.POST.get('province', '')
    c = request.POST.get('city', '')
    d = request.POST.get('district', '')
    covlocation = p + c + d + "%%"
    c_year = request.POST.get('year', '')
    c_month = request.POST.get('month', '')
    c_day = request.POST.get('day', '')
    c_time = int(request.POST.get('time', ''))
    c_location = request.POST.get('location', '')
    s_d = datetime.date(int(c_year), int(c_month), int(c_day))
    s_dt = datetime.datetime.strptime(str(s_d), '%Y-%m-%d')
    data = USchedule.objects.raw("select * from u_schedule where location like %s", [covlocation])
    Covarea.objects.create(location=p + c + d, s_time=s_dt, e_time=datetime.datetime.now())

    for line in data:
        o_year = int(line.o_time.year)
        o_month = int(line.o_time.month)
        o_day = int(line.o_time.day)
        s_d = datetime.date(int(c_year), int(c_month), int(c_day))
        s_dt = datetime.datetime.strptime(str(s_d), '%Y-%m-%d')
        o_d = datetime.date(int(o_year), int(o_month), int(o_day))
        o_dt = datetime.datetime.strptime(str(o_d), '%Y-%m-%d')
        today = datetime.datetime.now()
        if s_dt < o_dt < today:
            Passphrase.objects.filter(u_id=line.u_id).update(passphrase='no')
            Healthcode.objects.filter(u_id=line.u_id).update(healthcode='yellow')
            count = Quarantine.objects.filter(u_id=line.u_id).count()
            now = get_now_time()
            if count == 0:
                c_date = (datetime.date.today() + relativedelta(days=c_time)).strftime("%Y-%m-%d")
                Quarantine.objects.create(u_id=line.u_id, q_location=c_location, cancel_time=c_date)
                t_id = Quarantine.objects.get(u_id=line.u_id).id
                TQuarantine.objects.create(u_id=line.u_id, q_location=c_location, i_time=now, o_time=c_date, t_id=t_id)
            classes = Classes.objects.get(u_id=line.u_id).classes
            dep = Dormitory.objects.get(u_id=line.u_id).department
            r_id = Dormitory.objects.get(u_id=line.u_id).room_id
            for i in Classes.objects.filter(classes=classes):
                Passphrase.objects.filter(u_id=i.u_id).update(passphrase='no')
                Healthcode.objects.filter(u_id=i.u_id).update(healthcode='yellow')
                count = Quarantine.objects.filter(u_id=i.u_id).count()
                if count == 0:
                    c_date = (datetime.date.today() + relativedelta(days=c_time)).strftime("%Y-%m-%d")
                    Quarantine.objects.create(u_id=i.u_id, q_location=c_location, cancel_time=c_date)
                    t_id = Quarantine.objects.get(u_id=i.u_id).id
                    TQuarantine.objects.create(u_id=i.u_id, q_location=c_location, i_time=now, o_time=c_date, t_id=t_id)
            for i in Dormitory.objects.filter(department=dep, room_id=r_id):
                Passphrase.objects.filter(u_id=i.u_id).update(passphrase='no')
                Healthcode.objects.filter(u_id=i.u_id).update(healthcode='yellow')
                count = Quarantine.objects.filter(u_id=i.u_id).count()
                if count == 0:
                    c_date = (datetime.date.today() + relativedelta(days=c_time)).strftime("%Y-%m-%d")
                    Quarantine.objects.create(u_id=i.u_id, q_location=c_location, cancel_time=c_date)
                    t_id = Quarantine.objects.get(u_id=i.u_id).id
                    TQuarantine.objects.create(u_id=i.u_id, q_location=c_location, i_time=now, o_time=c_date, t_id=t_id)

    return HttpResponseRedirect(reverse('to_a_covlocation_up'))


def to_a_alter_quarantine(request):
    return render(request, "a_quarantine_loadup.html")


def a_alter_quarantine(request):
    p = request.POST.get('province', '')
    c = request.POST.get('city', '')
    d = request.POST.get('district', '')
    covlocation = p + c + d + "%%"
    c_time = int(request.POST.get('time', ''))
    c_location = request.POST.get('location', '')
    data = USchedule.objects.raw("select * from u_schedule where location like %s", [covlocation])
    for line in data:
        if_exit = Quarantine.objects.filter(u_id=line.u_id).count()
        if if_exit > 0:
            start_id = Quarantine.objects.get(u_id=line.u_id).id
            start_time = TQuarantine.objects.get(t_id=start_id).i_time
            c_date = (start_time + relativedelta(days=c_time)).strftime("%Y-%m-%d")
            date01 = TQuarantine.objects.filter(i_time=start_time)
            date01.update(o_time=c_date, q_location=c_location)
            for line01 in date01:
                Quarantine.objects.filter(id=line01.t_id).update(cancel_time=c_date, q_location=c_location)
    return HttpResponseRedirect(reverse('a_quarantine_list_up'))


def a_inout_query(request):
    u_id = request.POST.get('id', '')
    t_info = []
    if u_id:
        data = Iotable.objects.filter(u_id=u_id).order_by('-io_time')
    else:
        data = Iotable.objects.all().order_by('-io_time')
    for line in data:
        name = Users.objects.get(u_id=line.u_id).u_name
        if line.in_out == 1:
            in_out = "进"
        else:
            in_out = "出"
        if line.door_id == '1':
            door_id = '东门'
        elif line.door_id == '2':
            door_id = '南门'
        elif line.door_id == '3':
            door_id = '小北门'
        else:
            door_id = '大北门'
        l_info = [line.u_id, name, in_out, str(line.io_time)[:-6], door_id]
        t_info.append(l_info)
    return render(request, 'a_inout_query.html', {'data': t_info})


def a_t_schedule(request):
    u_id = request.POST.get('id', '')
    t_info = []
    if u_id:
        data = USchedule.objects.filter(u_id=u_id).order_by('-id')
    else:
        data = USchedule.objects.all().order_by('-id')
    for line in data:
        name = Users.objects.get(u_id=line.u_id).u_name
        l_info = [line.u_id, name, line.location, str(line.o_time)[:-6]]
        t_info.append(l_info)
    return render(request, 'a_total_schedule.html', {'data': t_info})


def a_t_interfacciami(request):
    u_id = request.POST.get('id', '')
    t_info = []
    if u_id:
        data = Interfacciami.objects.filter(u_id=u_id).order_by('-id')
    else:
        data = Interfacciami.objects.all().order_by('-id')
    for line in data:
        name = Users.objects.get(u_id=line.u_id).u_name
        l_info = [line.u_id, name, line.reason, str(line.time)[:-6]]
        t_info.append(l_info)
    return render(request, 'a_total_interfacciami.html', {'data': t_info})


def updatemap(request):
    from pyecharts import options as opts
    from pyecharts.charts import Map

    city_list = ["上城区", "下城区", "拱墅区", "西湖区", "滨江区", "萧山区", "余杭区", "富阳区", "临安市", "江干区", "建德市", "桐庐县", "淳安县"]
    todaydate = []
    now_time = get_now_time()
    now = str(now_time)[:10]
    date = Covarea.objects.raw("select * from covarea where s_time < %s and e_time > %s", [now, now])
    for i in city_list:
        for line in date:
            if i in line.location:
                todaydate.append(1)
                break
        todaydate.append(0)

    c_today = (
        Map()
            .add("杭州疫情区域",
                 [list(z) for z in zip(city_list, todaydate)],
                 maptype="杭州")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="杭州疫情区域   {}".format(now)),
            visualmap_opts=opts.VisualMapOpts(max_=1, range_text=['风险地区', '暂无风险地区'], border_color="#000")
        )
            .render("templates/map.html")
    )

    # return render(request, 'map.html', locals())
    return HttpResponseRedirect(reverse('a_return'))
