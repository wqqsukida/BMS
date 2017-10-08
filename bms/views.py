from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.db.models import Q
from bms.models import Asset,AssetDetail,UserInfo,Env,BussinessLine
import json
import paramiko
from utils.md5 import encrypt
from utils.pagination import Page
from django.forms import Form,fields,widgets
from django.views import View
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
# Create your views here.

# def index(request):
#     '''
#     index页面函数
#     '''
#     print(request.POST.get("search_str"))
#     all_asset_list=Asset.objects.all()
#     page_num=request.GET.get("page_num") #获取前端点击页码
#     p=Paginator(all_asset_list,10) #分页器对象
#
#     try:
#         all_asset_list=p.page(page_num) #当前页码的主机条目对象
#         now_page_range = p.page_range[int(page_num)-1:int(page_num)+8] #最多显示9条记录
#     except PageNotAnInteger:
#         all_asset_list=p.page(1) #访问/bms/index/页面时page_num=""传入p.page()会报错,所以让显示的主机条目为第一页
#         now_page_range=p.page_range[0:9] #最多显示9条记录
#     except EmptyPage:
#         all_asset_list=p.page(p.num_pages) #超过页码总数，则显示最后一页
#
#     print(p.page_range) #range(1, 12)
#     print(all_asset_list) #<Page 1 of 11>
#
#     return render(request,'index.html',locals())

def auth(func):
    '''
    验证session装饰器函数
    '''
    def wrapper(request,*args,**kwargs):
        user_dict = request.session.get('is_login', None)  # 获取会话保存到数据库的字典
        if user_dict:
            res=func(request,user_dict,*args,**kwargs)
            return res
        else:
            return redirect('/bms/login/')
    return wrapper

class RegisterForm(Form):
    username = fields.CharField(
        required=True,
        error_messages={'required':'*用户名不能为空'},
        widget=widgets.TextInput()
    )
    password = fields.CharField(
        required=True,
        error_messages={'required': '*密码不能为空'},
        widget = widgets.PasswordInput()
    )
    email = fields.EmailField(
        required=True,
        error_messages={'required': '*邮箱不能为空', 'invalid': '*邮箱格式错误'},
        widget=widgets.TextInput()
    )

def register(request):
    '''
    负责用户注册函数
    '''
    # u1 = UserInfo.objects.create(username='Elaine',password='123',addr='Beijing')
    # u2 = UserInfo.objects.create(username='Dylan',password='123',addr='Beijing')
    # u3 = UserInfo.objects.create(username='admin',password='admin',addr='Beijing')
    # e1 = Env.objects.create(name='Centos7.1')
    # e2 = Env.objects.create(name='RedHat7.1')
    # e3 = Env.objects.create(name='Windows2012')
    # e4 = Env.objects.create(name='Ubuntu16.04')
    # e5 = Env.objects.create(name='Debian9.1')
    # e6 = Env.objects.create(name='Suse12')
    if request.method == "GET":

        form = RegisterForm()
        return render(request,'register.html',{'form':form})
    else:
        response = {'status': True, 'data': None, 'msg': None}
        form = RegisterForm(request.POST)
        if form.is_valid():
            username=request.POST.get("username")
            print(UserInfo.objects.values_list("username"))
            if (username,) in UserInfo.objects.values_list("username"):
                response['status'] = False
                response['msg'] = {'username':['*用户名已存在']}
            else:
                pwd=request.POST.get("password")
                pwd=encrypt(pwd)
                email=request.POST.get("email",None)
                UserInfo.objects.create(username=username,password=pwd,email=email)
        else:
            response['status'] = False
            response['msg'] = form.errors
        return HttpResponse(json.dumps(response))

def bulk_create_models(request):
    Assetlist = []
    for i in range(20):
        Assetlist.append(Asset(id=i+40,
                               hostname="www.chejia" + str(i)+".com",
                               ip="172.16.153."+str(i),
                               port=8000+i,
                               model="web_server",
                               env_id=1,
                               hardware="4cpu",
                               bussiness_id=3,
                               ))
    Asset.objects.bulk_create(Assetlist)

    # dylan_asset = Asset.objects.filter(hostname__icontains="Elaine")
    # user_obj = UserInfo.objects.get(username="Elaine")
    # all_users = UserInfo.objects.all()
    # #将所有hostname包含Elaine的主机的管理员设置为Elaine
    # for one_asset in dylan_asset:
    #     one_asset.users.remove(*all_users)
    #     one_asset.users.add(user_obj)

    return HttpResponse('Async database finished!')

class LoginForm(Form):
    username = fields.CharField(
        required=True,
        error_messages={'required':'*用户名不能为空'},
        widget=widgets.TextInput(attrs={'class':'form-control',
                                        'type':'text',
                                        'id':'inputUsername3',
                                        'placeholder':'Username',
                                        'name':'username'
                                        })
    )
    password = fields.CharField(
        required=True,
        error_messages={'required': '*密码不能为空'},
        widget = widgets.PasswordInput(attrs={'class':'form-control',
                                        'id':'inputPassword3',
                                        'placeholder':'Password',
                                        'name':'password'
                                        })
    )

# class LoginView(View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(LoginView,self).dispatch(request, *args, **kwargs)
#
#     def get(self, request, *args,**kwargs):
#         return render(request,'login.html')
#
#     def post(self,request, *args,**kwargs):
#         user = request.POST.get('user')
#         pwd = request.POST.get('pwd')
#         obj = models.UserInfo.objects.filter(username=user,password=pwd).first()
#         if obj:
#             request.session['user_info'] = {'id':obj.id,'username': obj.username}
#             return redirect('/users.html')
#         return render(request, 'login.html',{'msg': '去你的'})

def login(request):
    '''
    login登录验证函数
    '''
    if request.method == "GET":
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    else:
        response = {'status': True, 'data': None, 'msg': None}
        form = LoginForm(request.POST)
        if form.is_valid():
            user = request.POST.get('username',None)  #获取input标签里的username的值 None：获取不到不会报错
            pwd = request.POST.get('password',None)
            pwd = encrypt(pwd) #md5加密密码字符串
            if UserInfo.objects.filter(username=user,password=pwd).count() == 1:
                request.session['is_login'] = {'user': user}
                response['data']={}
            else:
                response['status'] = False
                response['msg']={'password':['*用户名或者密码错误']}
        else:
            response['status']=False
            response['msg']=form.errors
        print(response)
        return HttpResponse(json.dumps(response))

    # ret = {'status':''}
    # if request.method == 'POST':
    #     user = request.POST.get('username',None)  #获取input标签里的username的值 None：获取不到不会报错
    #     pwd = request.POST.get('password',None)
    #     pwd = encrypt(pwd) #md5加密密码字符串
    #     print(pwd)
    #     is_empty = all([user,pwd])
    #     if is_empty:
    #         count = UserInfo.objects.filter(username=user,password=pwd).count() #获取数据库UserInfo里满足username=user,password=pwd的数据条数
    #
    #         if count == 1:
    #             # 生成随机字符串
    #             # 随机字符串作为cookie发送给客户端
    #             # 服务端随机字符串作为key, 自己设置一些values{}，这里的values就是{'is_login':{'user':user}}
    #             request.session['is_login'] = {'user':user}  #会话保持，将该字典存到服务器端数据库的django_session
    #             return redirect('/bms/index/')
    #         else:
    #             ret['status'] = '用户名或密码错误'
    #     else:
    #         ret['status'] = '用户名和密码不能为空'
    #
    # return render(request,'login.html',ret,)

# def index(request):
#     user_dict = request.session.get('is_login',None) #获取会话保存到数据库的字典
#     if user_dict:
#         return render('index.html',{'username':user_dict['user'],})
#     else:
#         return redirect('/app01/login/')

def logout(request):
    '''
    logout删除session函数
    '''

    request.session['is_login'].clear() #删除session
    return redirect('/bms/login/')

@auth
def index(request,user_dict):
    '''
    index页面函数
    '''
    form = CreatAssetForm()
    search_str = request.GET.get("search_string","") #得到按主机名过滤条件，默认为""
    print(search_str)
    if request.method=="GET" and user_dict['user']=='admin': #如果登录用户是admin，则显示所有主机条目信息
        all_asset_list=Asset.objects.all().filter(hostname__icontains=search_str)
    elif request.method=="GET" and user_dict['user']!='admin':  #如果不是，则显示当前登录用户所属业务线的主机条目信息
        all_asset_list=Asset.objects.filter(bussiness__userinfo__username=user_dict['user'],hostname__icontains=search_str)
        print(all_asset_list.count())
    # all_users = UserInfo.objects.values_list("username") #所有用户名称
    # all_env = Env.objects.values_list("name") #所有主机环境名称
    username=user_dict['user'] #当前登录用户
    # page_num=request.GET.get("page_num") #获取前端点击页码

    try:
        current_page = int(request.GET.get('page_num'))
    except TypeError:
        current_page = 1
    all_count = all_asset_list.count()
    # page_obj = Page(current_page,all_count,'/hosts.html')
    page_obj = Page(current_page, all_count, request.path_info,search_str)
    all_asset_list = all_asset_list[page_obj.start:page_obj.end]
    page_str = page_obj.page_html()

    # p=Paginator(all_asset_list,10) #分页器对象
    #
    # try:
    #     all_asset_list=p.page(page_num) #当前页码的主机条目对象
    #     now_page_range = p.page_range[int(page_num)-1:int(page_num)+8] #最多显示9条记录
    # except PageNotAnInteger:
    #     all_asset_list=p.page(1) #访问/bms/index/页面时page_num=""传入p.page()会报错,所以让显示的主机条目为第一页
    #     now_page_range=p.page_range[0:9] #最多显示9条记录
    # except EmptyPage:
    #     all_asset_list=p.page(p.num_pages) #超过页码总数，则显示最后一页

    # print(p.page_range)
    #
    # print(all_asset_list)
    # print(request.GET, type(request.GET))
    # print(request.GET.urlencode())

    from django.http.request import QueryDict

    url_obj = QueryDict(mutable=True)
    url_obj['_getarg'] = request.GET.urlencode()

    # print(url_obj.urlencode())
    url_param = url_obj.urlencode()
    
    return render(request,'index.html',locals())

#locals包含以下参数：
# {'username': user_dict['user'],
#  "all_asset_list": all_asset_list,
#  'all_users': all_users,
#  'p': p,
#  'now_page_range': now_page_range,
#  'all_env': all_env,}

class CreatAssetForm(Form):
    hostname = fields.CharField(
        required=True,
        min_length=1,
        max_length=20,
        error_messages={'required': '*主机名不能为空'},
        widget=widgets.TextInput(attrs={'name': 'hostname'})
    )
    ip = fields.GenericIPAddressField(
        required=True,
        error_messages={'required': '*IP不能为空', 'invalid': '*IP格式错误'},
        widget=widgets.TextInput(attrs={'name': 'ip'})
    )
    port = fields.CharField(
        required=True,
        min_length=1,
        max_length=5,
        error_messages={'required': '*端口不能为空'},
        widget=widgets.TextInput(attrs={'name': 'port'})
    )
    model = fields.CharField(
        required=True,
        min_length=1,
        max_length=20,
        error_messages={'required': '*类型不能为空'},
        widget=widgets.TextInput(attrs={'name': 'model'})
    )
    # fields.EmailField()
    # fields.GenericIPAddressField(protocol='ipv4')

    env_id = fields.ChoiceField(
        choices=[],
        widget=widgets.Select(attrs={'name': 'env_id'})
    )
    hardware = fields.CharField(
        required=True,
        min_length=1,
        max_length=20,
        error_messages={'required': '*硬件配置不能为空'},
        widget=widgets.TextInput(attrs={'name': 'hardware'})
    )
    bussiness_id = fields.ChoiceField(
        required=True,
        choices=[],
        error_messages={'required': '*主机所属业务线不能为空'},
        widget=widgets.Select(attrs={'name': 'bl_id'})
    )

    def __init__(self, *args, **kwargs):
        super(CreatAssetForm, self).__init__(*args, **kwargs)
        # self.fields已经有所有拷贝的字段
        # print(Env.objects.values_list('id', 'name'))
        # print(UserInfo.objects.values_list('id', 'username'))
        self.fields['env_id'].choices = Env.objects.values_list('id', 'name')
        self.fields['bussiness_id'].choices = BussinessLine.objects.values_list('id', 'name')

@auth
def creat_asset(request,user_dict):
    url_param = request.GET.get('_getarg')
    # print(url_param)
    if request.method == "GET":
        form = CreatAssetForm()
        return render(request, 'creat_asset.html', {'form': form,'username':user_dict['user'],'url_param':url_param})
    else:
        form = CreatAssetForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # 把所有正确数据获取到
            # {'username': 'xxxxx', 'password': 'xxxxx', 'ut_id': '1'}
            # print(form.cleaned_data)
            # {'username': 'xxxxx', 'password': 'xxxxx', 'ut_id': '1',role_id:}
            # user_id_list = form.cleaned_data.pop('user_id')  # [1,2,3]
            obj = Asset.objects.create(**form.cleaned_data)
            # obj.users.add(*user_id_list)


            return redirect('/bms/index/?'+url_param)
        else:
            print(form.errors)
            return render(request, 'creat_asset.html', {'form': form,'username':user_dict['user'],'url_param':url_param})

# @auth
# def creat_asset(request,user_dict):
#     '''
#     创建主机条目页面函数
#     '''
#     if request.method == "POST":
#         hostname=request.POST.get("hostname")
#         ip=request.POST.get("ip")
#         port=request.POST.get("port")
#         model=request.POST.get("model")
#         hardware=request.POST.get("hardware")
#         #获取一对多env_obj
#         env=request.POST.get("env")
#         env_obj=Env.objects.get(name=env)
#         print(env_obj)
#         asset_obj=Asset.objects.create(hostname=hostname, ip=ip, port=port, model=model,env=env_obj,hardware=hardware)
#         #获取多对多users_obj
#         admin = request.POST.getlist("admin")
#         print(admin)
#         users_obj = []
#         if user_dict['user'] == 'admin': #如果登录用户是admin，则将选中的用户作为用户对象添加到users_obj
#             for user in admin:
#                 users_obj.append(UserInfo.objects.get(username=user))
#             print(users_obj)
#         else : #否则，将当前登录用户添加到users_obj
#             users_obj.append(UserInfo.objects.get(username=user_dict['user']))
#         # 将得到的users_obj和当前创建的主机条目绑定多对多关系
#         asset_obj.users.add(*users_obj)
#         return redirect("/bms/index/")
#     all_users=UserInfo.objects.values_list("username")
#     all_env=Env.objects.values_list("name")
#
#     return render(request,"creat_asset.html",{'username':user_dict['user'],
#                                               'all_users':all_users,
#                                               'all_env':all_env
#                                               })

@auth
def del_asset(request,user_dict):
    '''
    删除主机条目函数
    '''
    id = request.GET.get("id")
    checked = request.GET.get("checked")
    print(checked)
    if checked == "true":
        Asset.objects.filter(id=id).delete()
    return redirect("/bms/index/")

@auth
def del_user(request,user_dict):
    '''
    删除用户条目函数
    :param request:
    :param user_dict:
    :return:
    '''
    response = {'status': True, 'data': None, 'msg': None}
    if user_dict['user'] == 'admin':
        id = request.POST.get("id")
        checked = request.POST.get("checked")
        print(checked)
        if checked == "true":
            UserInfo.objects.filter(id=id).delete()
            response['msg'] = "成功删除用户id=%s的信息"%id
    else:
        response['status'] = False
        response['msg'] = "非admin用户无法删除用户信息！"
    return HttpResponse(json.dumps(response))

@auth
def batch_del(request,user_dict):
    id_list=json.loads(request.POST.get("del_list"))
    for id in id_list:
        print(Asset.objects.filter(id=id).values("hostname"))
        Asset.objects.filter(id=id).delete()
    return HttpResponse("成功删除%s条主机信息"%len(id_list))


@auth
def mod_asset(request,user_dict,id):
    # if request.method=="GET":
    #     obj = Asset.objects.filter(id=id).first()
    #     # user_id_list = obj.users.values_list('id')
    #     # v = list(zip(*user_id_list))[0] if user_id_list else []
    #     form = CreatAssetForm(initial={'hostname': obj.hostname, 'ip': obj.ip,'port':obj.port,
    #                                    'model':obj.model,'env_id': obj.env_id,'hardware':obj.hardware,
    #                                    'bussiness_id': obj.bussiness_id})
    #     return HttpResponse(json.dumps(form))
    if request.method == "POST":
        response = {'status': True, 'data': None, 'msg': None}
        form = CreatAssetForm(data=request.POST)
        # print(form)
        if form.is_valid():
            print(form.cleaned_data)
            # {'hostname': 'www.shop0.com', 'port': '8000', 'bussiness_id': '1', 'ip': '172.16.151.0', 'model': 'web_server', 'hardware': '4cpu', 'env_id': '1'}
            bussiness_id = form.cleaned_data.pop('bussiness_id')
            # # 用户表更新
            query = Asset.objects.filter(id=id)
            query.update(**form.cleaned_data)
            # obj = query.first()
            if user_dict['user'] == 'admin':
                query.update(bussiness_id=bussiness_id) #admin用户才能更改业务线字段
                # obj.users.set(user_id)
            #     # return redirect('/bms/index/')
        else:
            print(form.errors)
            response['status'] = False
            response['msg'] = form.errors
        return HttpResponse(json.dumps(response))

# @auth #mod_asset=auth(mod_asset)
# def mod_asset(request,user_dict,id):
#     '''
#     更改主机条目内容函数
#     '''
#     if request.method=="POST":
#         hostname = request.POST.get("hostname")
#         ip = request.POST.get("ip")
#         port = request.POST.get("port")
#         model = request.POST.get("model")
#         env = request.POST.get("env")
#         env_obj = Env.objects.get(name=env)
#         hardware = request.POST.get("hardware")
#         asset_obj=Asset.objects.filter(id=id) # 获取要修改的主机条目
#         asset_obj.update(hostname=hostname, ip=ip, port=port, model=model,env=env_obj,hardware=hardware)
#         if user_dict['user'] == 'admin': #如果登录用户是admin，才能进行的操作
#             # 得到所选择的用户名列表对象(前端ajax发送过来的数组对象，需要反序列化)
#             admin = json.loads(request.POST.get("admin"))
#             print(admin)
#             users_obj = []
#             for user in admin:
#                 users_obj.append(UserInfo.objects.get(username=user)) #根据admin.得到选中的用户对象
#             # print(users_obj)
#             all_users=UserInfo.objects.all() # 得到UserInfo下所有对象
#             # rm_users=all_users-users_obj
#             asset_obj[0].users.remove(*all_users) # 先删除被修改主机条目对应的用户关系
#             asset_obj[0].users.add(*users_obj) # 再添加所选的用户对象，创建新的多对多关系
#         return redirect("/bms/index/")

class UserForm(Form):
    username = fields.CharField(
        required=True,
        error_messages={'required':'*用户名不能为空'},
        widget=widgets.TextInput(attrs={})
    )
    email = fields.EmailField(
        required=True,
        error_messages={'required': '*邮箱不能为空', 'invalid': '*邮箱格式错误'},
        widget=widgets.TextInput()
    )

    bussinesslines = fields.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(attrs={})
    )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # self.fields已经有所有拷贝的字段
        self.fields['bussinesslines'].choices = BussinessLine.objects.values_list('id', 'name')

@auth
def users(request,user_dict,id):
    search_str = request.GET.get("search_string", "")
    username = user_dict['user']
    if request.method == "GET" and user_dict['user'] == 'admin': #admin用户登录(get)时
        user_form = UserForm()
        all_user_list = UserInfo.objects.all().filter(username__icontains=search_str)
        # 分页功能：
        try:
            current_page = int(request.GET.get('page_num'))
        except TypeError:
            current_page = 1
        all_count = all_user_list.count()
        # page_obj = Page(current_page,all_count,'/hosts.html')
        page_obj = Page(current_page, all_count, request.path_info, search_str)
        all_user_list = all_user_list[page_obj.start:page_obj.end]
        page_str = page_obj.page_html()

        return render(request, 'users.html', locals())

    elif request.method == "POST" :
        response = {'status': True, 'data': None, 'msg': None}
        user_form = UserForm(data=request.POST)
        if user_form.is_valid(): #如果POST过来的数据有效
            print("得到有效字段：",user_form.cleaned_data)
            username = user_form.cleaned_data.pop("username") # 去掉 用户名字段
            bid_list = user_form.cleaned_data.pop("bussinesslines") #得到用户对应的业务线id
            UserInfo.objects.filter(id=id).update(**user_form.cleaned_data) # 更改除了用户名，业务线其他字段


            if user_dict['user'] == 'admin':
                print("要更新的业务线id:",bid_list)
                obj = UserInfo.objects.filter(id=id).first()  # 要修改的用户obj
                obj.bussinesslines.set(bid_list)  # 只有admin能修改用户对应的业务线
        else: #无效则返回False和错误的msg
            response['status'] = False
            response['msg'] = user_form.errors
        return  HttpResponse(json.dumps(response))
    else: #其他用户get时
        user_form = UserForm()
        all_user_list = UserInfo.objects.filter(username=username).filter(username__icontains=search_str)
        return render(request, 'users.html', locals())




def do_ajax(request):
    ret=request.POST.get("test")
    if ret:
        return HttpResponse("Ajax_test Successed!")

@auth
def web_terminal(request,user_dict):
    hostuser=request.POST.get("hostuser")
    hostpwd=request.POST.get("hostpwd")
    hostip=request.POST.get("hostip")
    cmd=request.POST.get("cmd")
    print(hostip,hostpwd,hostuser,cmd)
    # ssh_obj = paramiko.SSHClient()
    # ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh_obj.connect(hostip, 22, hostuser, hostpwd)
    # stdin, stdout, stderr = ssh_obj.exec_command("ifconfig -a")
    # # if stderr:
    # #     print(stderr.read().decode('utf-8'))
    # # else:
    # res = stdout.read().decode('utf-8')
    # print(res)
    # ssh_obj.close()
    return render(request,"terminal.html",locals())


class BussinessForm(Form):
    name = fields.CharField(
        required=True,
        error_messages={'required':'*业务线名不能为空'},
        widget=widgets.TextInput(attrs={})
    )
    description = fields.CharField(
        max_length=12,
        widget=widgets.Textarea(attrs={})
    )

@auth
def authorization(request,user_dict,id):
    search_str = request.GET.get("search_string", "")
    username = user_dict['user']
    if request.method == "GET" and user_dict['user'] == 'admin':  # admin用户登录(get)时
        b_form = BussinessForm()
        all_bussiness_list = BussinessLine.objects.all().filter(name__icontains=search_str)
        # 分页功能：
        print(all_bussiness_list)
        try:
            current_page = int(request.GET.get('page_num'))
        except TypeError:
            current_page = 1
        all_count = all_bussiness_list.count()
        # page_obj = Page(current_page,all_count,'/hosts.html')
        page_obj = Page(current_page, all_count, request.path_info, search_str)
        all_user_list = all_bussiness_list[page_obj.start:page_obj.end]
        page_str = page_obj.page_html()

        return render(request, 'authorization.html', locals())

    elif request.method == "POST":
        response = {'status': True, 'data': None, 'msg': None}
        b_form = BussinessForm(data=request.POST)
        if b_form.is_valid():
            print("得到有效字段：", b_form.cleaned_data)
            name = b_form.cleaned_data.pop("name")  # 去掉业务线名字段
            BussinessLine.objects.filter(id=id).update(**b_form.cleaned_data)  # 更改除了业务线名，其他字段

            if user_dict['user'] == 'admin':
                print("要更新的业务线名:", name)
                BussinessLine.objects.filter(id=id).update(name=name)# 只有admin能修改用户对应的业务线

        else:  # 无效则返回False和错误的msg
            response['status'] = False
            response['msg'] = b_form.errors
        return HttpResponse(json.dumps(response))
    else:
        return render(request, 'users.html', locals())

@auth
def asset_detail(request,user_dict):
    username = user_dict['user']
    asset_id = request.GET.get('AssetID')
    url_param = request.GET.get('_getarg')
    print(asset_id,url_param)

    asset_obj = AssetDetail.objects.filter(asset_id=asset_id).first()
    

    return render(request,'asset_detail.html',locals())

from django.views.decorators.csrf import csrf_exempt,csrf_protect

@csrf_exempt
def Get_AssetInfo(request):
    print(request.POST)
    print(request.body.decode('utf-8'))
    origin = request.body.decode('utf-8')
    dic = json.loads(origin)
    asset_obj = AssetDetail.objects.filter(ip=dic.get('ip'))
    asset_id = Asset.objects.filter(ip=dic.get('ip')).first().value('id')
    print(asset_id)
    if asset_obj:
        asset_obj.update(**dic)
    else:
        AssetDetail.objects.create(**dic,asset_id=asset_id)


    return HttpResponse('POST GET!')