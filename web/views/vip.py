from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from common.models import Users,Types,Goods,Orders,Detail

# 公共信息加载
def loadinfo(request):
    '''公共信息加载'''
    context = {}
    lists = Types.objects.filter(pid=0)
    context['typelist'] = lists
    return context

# 我的订单
def viporders(request):
    '''当前用户订单'''
    context = loadinfo(request)
    # 获取当前用户的所有订单信息
    odlist = Orders.objects.filter(uid=request.session['vipuser']['id'])
    # 遍历当前用户的所有订单，添加他的订单详情
    for od in odlist:
        delist = Detail.objects.filter(orderid=od.id)
        # 遍历每个商品详情，从Goods中获取对应的图片
        for og in delist:
            og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname
        od.detaillist = delist
    # 将整理好的订单信息放置到模板遍历中
    context['orderslist'] = odlist
    return render(request,"web/viporders.html",context)

def odstate(request):
    ''' 修改订单状态 '''
    try:
        oid = request.GET.get("oid",'0')
        ob = Orders.objects.get(id=oid)
        ob.state = request.GET['state']
        ob.save()
        return redirect(reverse('vip_orders'))
    except Exception as err:
        print(err)
        return HttpResponse("订单处理失败！")


def vipcenter(request):
    '''会员个人中心信息'''
    try:
        ob = Users.objects.get(id=request.session['vipuser']['id'])
        context = {"vp":ob}
        return render(request,"web/vipcenter.html",context)
    except Exception as err:
        print(err)
        context = {"info":"错误:未找到您的相关信息!"}
    return render(request,"web/vip/info.html",context)

def update(request):
    '''执行更新会员个人信息的保存'''
    try:
        #获取编辑对象
        ob = Users.objects.get(id=request.session['vipuser']['id'])
        #从表单中获取信息并保存
        ob.name = request.POST['name']
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.save()
        context = {"info":"您的个人信息编辑成功！"}
    except Exception as err:
        print(err)
        context = {"info":"您的个人信息编辑失败！"}
    return render(request,"web/vip/info.html",context)

def resetps(request):
    '''用户修改密码'''
    try:
        #获取修改对象
        vp = Users.objects.get(id=request.session['vipuser']['id'])
        context = {"user":vp}
        return render(request,"web/resetps.html",context)
    except Exception as err:
        print(err)
        context = {"info":"错误:未找到您的相关信息!"}
        return render(request,"web/vip/info.html",context)


def doresetps(request):
    '''执行密码更改'''
    try:
        #获取修改对象
        ob = Users.objects.get(id=request.session['vipuser']['id'])
        #获取密码并进行MD5加密操作
        import hashlib
        m = hashlib.md5()
        m.update(bytes(request.POST['oldpassword'],encoding="utf8"))
        #判断原密码是否正确
        if ob.password == m.hexdigest():
            #判断新密码的两次输入是否一致
            newpassword = request.POST['newpassword']
            if newpassword == request.POST['repassword']:
                m = hashlib.md5()
                m.update(bytes(newpassword,encoding="utf8"))
                ob.password = m.hexdigest()
                ob.save()
                context = {"info":"您的密码已修改成功!"}
            else:
                context = {"info":"两次输入的新密码不一致，请重新输入！"}
                return render(request,"web/resetps.html",context)
        else:
            context = {"info":"您输入的原密码不正确，请重新输入！"}
            return render(request,"web/resetps.html",context)
    except Exception as err:
        print(err)
        context = {"info":"密码修改失败！"}
    return render(request,"web/vip/info.html",context)
