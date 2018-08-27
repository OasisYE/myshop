#!/usr/bin/env python
# -*-coding:utf-8 -*-
# ** author:Oasis
# *****************************
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

from common.models import Users
from datetime import datetime

# Create your views here.
# 浏览会员
def index(request,pIndex):
    # 执行数据查询，并放置到模板中
    # list = Users.objects.all()
    # context = {"userslist":list}
    # #return HttpResponse(list)
    # return render(request,'myadmin/users/index.html',context)


    # 获取用户信息查询对象
    mod = Users.objects  # 获取所有的记录
    mywhere = []  # 定义一个用于存放搜索条件列表

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword", None)
    if kw:
        # 查询账号中只要含有关键字
        list = mod.filter(username__contains=kw)
        # 查询姓名中只要含有关键字
        #list = mod.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)
    else:
        list = mod.filter()

    # 获取、判断并封装用户性别搜索条件
    set = request.GET.get('set', '')
    print ("性别为",set)
    if set != '':
        list = list.filter(sex=set)
        mywhere.append("sex=" + set)

    # set = request.GET.get('set', '')
    # print ('状态: ',set)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 5)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    # 遍历商品信息，并获取对应的商品类别名称，以typename名封装
    # for vo in list2:
    #     ty = Types.objects.get(id=vo.typeid)
    #     vo.typename = ty.name

    # 封装信息加载模板输出
    # context = {'typelist': tlist, "goodslist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages,
    #            'mywhere': mywhere, 'typeid': int(typeid)}
    # return render(request, "myadmin/goods/index.html", context)

    context = {'userslist': list2, 'plist': plist, 'mywhere': mywhere, 'pIndex': pIndex, 'maxpages': maxpages, 'plist_len': len(plist)}
    return render(request, "myadmin/users/index.html", context)

def add(request):
    '''
    添加会员信息表单页
    :param request:
    :return:
    '''
    return render(request,'myadmin/users/add.html')


def insert(request):
    '''
    添加会员信息
    :param request:
    :return:
    '''
    try:
        ob = Users()
        ob.username = request.POST['username']
        ob.name = request.POST['name']
        # 获取密码并md5
        import hashlib
        m = hashlib.md5()
        m.update(bytes(request.POST['password'], encoding="utf8"))
        ob.password = m.hexdigest()
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = 1
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '添加成功！'}
    except Exception as err:
        print(err)
        context = {'info': '添加失败！'}

    return render(request, "myadmin/info.html", context)

def delete(request,uid):
    '''
    删除用户信息
    :param request:
    :return:
    '''
    try:
        # uid = Users.request.POST['id']
        ob = Users.objects.get(id=uid)
        ob.delete()
        context = {'info': '删除成功！'}
    except:
        context = {'info': '删除失败！'}
    return render(request, "myadmin/info.html", context)

def edit(request,uid):
    '''
    加载编辑页面信息
    :param request:
    :param uid:
    :return:
    '''
    try:
        # uid = Users.request.POST['id']
        ob = Users.objects.get(id=uid)
        context = {"user":ob}

        return render(request,'myadmin/users/edit.html',context)
    except:
        context = {'info': '没有找到要修改的信息！'}
        return render(request, "myadmin/info.html", context)


def update(request,uid):
    '''
    修改用户信息
    :param request:
    :param uid:
    :return:
    '''
    try:
        ob = Users.objects.get(id=uid)
        ob.name = request.POST['name']
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = request.POST['state']
        ob.save()
        context = {'info': '修改成功！'}
    except Exception as err:
        print(err)
        context = {'info': '修改失败！'}

    return render(request, "myadmin/info.html", context)

def editpawd(request,uid):
	#编辑密码
	ulist=Users.objects.get(id=uid)
	context={"list":ulist}
	return render(request,"myadmin/users/editpawd.html",context)

def updatepawd(request):
	try:
		#新增会员信息
		list=Users.objects.get(id=request.POST['txt_id'])
		#获取密码并md5
		import hashlib
		m = hashlib.md5()
		m.update(bytes(request.POST['password'],encoding="utf8"))
		list.password = m.hexdigest()
		list.save()
		info="密码重置成功！"
		context={"info":info}
		return render(request,"myadmin/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"myadmin/info.html",context)





