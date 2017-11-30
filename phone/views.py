import math
import re
import json
from collections import Counter
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import jd_phone_info,user_info
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.

#首页
def index(request):
	price_list = jd_phone_info.objects[:200]
	#获取手机品牌
	#name price
	reg =re.compile(r'(.*?)\s',re.S)
	#此处找出手机购买次数排名前十的列表
	names=[]
	prices=[]
	for i in jd_phone_info.objects.all():
		#用正则获取手机品牌的前几个字
		pn = reg.findall(i.product_name)
		prices.append(i.product_price)
		try:
			p_name=pn[0]
			names.append(p_name)
		except:
			pass
	c=Counter(names)
	m=c.most_common(10)#list,显示前十
	count =len(price_list)#一共多少
	per_pages=10#定义每一页多少条
	paginator = Paginator(price_list,per_pages)#一页10条
	paginator.num_pages =math.ceil(count/per_pages)#向上取整，取最近的一个整数
	page = request.GET.get('page')
	try:
		rows = paginator.page(page)
	except PageNotAnInteger:
		rows = paginator.page(1)#不是整数的时候就设置为１
	except EmptyPage:
		rows = paginator.page(paginator.num_pages)#
	return render(request,'phone/index.html',context={"count":count,"rows":rows,"names":names,"prices":prices,"pn":m})

#商品详情页
def details(request,product_id):
	#获取商品的详情以及评论
	product_infos = jd_phone_info.objects(product_id=product_id)
	i=product_infos.first()
	infos = i.product_commentinfo
	per_pages = 5  # 定义每一页多少条
	paginator = Paginator(infos, per_pages)  # 一页１０条
	page = request.GET.get('page')
	try:
		rows = paginator.page(page)
	except PageNotAnInteger:
		rows = paginator.page(1)  # 不是整数的时候就设置为１
	except EmptyPage:
		rows = paginator.page(paginator.num_pages)  #

	return render(request,'phone/details.html',context={"infos":infos,"i":i,"rows":rows})

#显示所有的
def manager(request):
	alls = jd_phone_info.objects.all()

	return render(request,'phone/manager.html',context={"alls":alls})

@csrf_exempt
def delete(request):
	# if request.method=="POST":
	product_obj = json.loads(request.body.decode())['obj']
	# print(product_obj)
	#删除数据
	# product = jd_phone_info.objects.filter(product_id=product_obj).delete()
	alls = jd_phone_info.objects.all()
	a=[]
	for all in alls:
		a.append([all.product_id,all.shop_name,all.product_name,all.product_price,all.comment_num])
	return JsonResponse({"data":a})

#登录
def login(request):
	if request.method=="POST":
		user_name = request.POST.get('user_name')
		password = request.POST.get('password')
		l_flag = user_info.objects.filter(user_name=user_name,password=password)
		if l_flag:
			#表示通过验证了，跳转至首页
			return HttpResponseRedirect('/phone/index')
		else:
			cont="用户名或密码错误，请重新输入！"
			return render(request,'phone/login.html',context={"cont":cont})
	return render(request,'phone/login.html')

#注册
def register(request):
	if request.method=="POST":
		print(request.POST)
		# 获取发送过来的数据
		user_name=request.POST.get('user_name')
		password = request.POST.get('password')
		phone_num = request.POST.get('phone_num')
		#添加到数据库,首先进行判断是否已经被注册用户名
		r_flag = user_info.objects.filter(user_name=user_name)
		#没有时才创建
		if not r_flag:
			user_info.objects.create(user_name=user_name, password=password, phone_num=phone_num)
			# 跳转到login页面
			return HttpResponseRedirect('login')
		else:
			context = {"info": "该用户名已经被注册了，请重新注册，谢谢！"}
		return render(request, 'phone/register.html', context=context)
	else:
		return render(request,'phone/register.html')

#注销
def logout(request):

	return HttpResponseRedirect('/phone/login')