from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from common.models import Users,Types,Goods

# 公共信息加载
def loadinfo(request):
    '''公共信息加载'''
    context = {}
    lists = Types.objects.filter(pid=0)
    context['typelist'] = lists
    return context

# Create your views here.
def index(request):
    '''项目前台首页'''
    context = loadinfo(request)
    # 获取点击量前5名的商品
    hotgoods = Goods.objects.all().order_by('-clicknum')[:5]
    # 封装信息加载模板输出
    context['hotlist'] = hotgoods
    return render(request,"web/index.html",context)

def lists(request,pIndex=1):
    '''商品列表页'''
    context = loadinfo(request)
    # 获取商品信息查询对象
    mod = Goods.objects
    mywhere = []  # 定义一个用于存放搜索条件列表

    # 判断添加搜索条件
    tid = int(request.GET.get('tid', 0))
    if tid > 0:
        list = mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid))
        mywhere.append("tid=" + str(tid))
    else:
        list = mod.filter()

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword", None)
    if kw:
        # 查询商品名中只要含有关键字的都可以
        list = list.filter(goods__contains=kw)
        mywhere.append("keyword=" + kw)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 3)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    # 封装信息加载模板输出
    context['goodslist'] = list2
    context['plist'] = plist
    context['pIndex'] = pIndex
    context['maxpages'] = maxpages
    context['mywhere'] = mywhere
    context['tid'] = int(tid)
    return render(request, "web/list.html", context)

def detail(request,gid):
    '''商品详情页'''
    context = loadinfo(request)
    # 加载商品详情信息
    ob = Goods.objects.get(id=gid)
    ob.clicknum += 1  # 点击量加1
    ob.save()
    context['goods'] = ob
    return render(request, "web/detail.html", context)

# ==============前台会员登录====================
def login(request):
    '''会员登录表单'''
    return render(request,'web/login.html')

def dologin(request):
    '''会员执行登录'''
    # 校验验证码
    verifycode = request.session['verifycode']
    code = request.POST['code']
    if verifycode != code:
        context = {'info':'验证码错误！'}
        return render(request,"web/login.html",context)

    try:
        #根据账号获取登录者信息
        user = Users.objects.get(username=request.POST['username'])
        #判断当前用户是否是后台管理员用户
        if user.state == 0 or user.state == 1:
            # 验证密码
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'],encoding="utf8"))
            if user.password == m.hexdigest():
                # 此处登录成功，将当前登录信息放入到session中，并跳转页面
                request.session['vipuser'] = user.toDict()
                return redirect(reverse('index'))
            else:
                context = {'info':'登录密码错误！'}
        else:
            context = {'info':'此用户为非法用户！'}
    except:
        context = {'info':'登录账号错误！'}
    return render(request,"web/login.html",context)

def logout(request):
    '''会员退出'''
    # 清除登录的session信息
    del request.session['vipuser']
    # 跳转登录页面（url地址改变）
    return redirect(reverse('login'))

def register(request):
	'''会员注册页面'''
	return render(request,"web/register.html")

def doregister(request):
	'''执行会员注册操作'''
	#获取并判断用户名是否为空
	username = request.POST['username']
	if len(username) == 0:
		context = {"info":"用户名不能为空！"}
		return render(request,"web/register.html",context)
	#获取并判断两次输入的密码是否一致
	password = request.POST['password']
	repassword = request.POST['repassword']
	if password != repassword:
		context = {"info":"两次输入的密码不一致！"}
		return render(request,"web/register.html",context)
	try:
		#实例化对象
		ob = Users()
		#用ob进行封装
		ob.username = request.POST['username']
		#获取密码并进行MD5加密操作
		import hashlib
		m = hashlib.md5()
		m.update(bytes(request.POST['password'],encoding="utf8"))
		ob.password = m.hexdigest()
		ob.state = 1
		ob.save()
		context = {"info":"注册成功，请点击登录！"}
	except Exception as err:
		print(err)
		context = {"info":"用户名已存在，请重新输入!"}
	return render(request,"web/register.html",context)
