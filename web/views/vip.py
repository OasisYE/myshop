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