from django.db import models
from mongoengine import *

connect(db='jd2',host='127.0.0.1',port=27017)
# Create your models here.

class jd_phone_info(Document):
	# id = IntField(primary_key=True)
	# 店铺名
	shop_name = StringField()
	# 商品名
	product_name = StringField()
	# 商品id
	product_id = StringField(required=True)
	# 商品id
	product_url = StringField()
	# 商品价格
	product_price = FloatField()
	# 评论总数
	comment_num = StringField()
	# 好评
	good_commt_num = StringField()
	# color
	product_color =  StringField()
	# 中评
	gen_commt_num = StringField()
	# 差评
	bad_commt_num = StringField()
	# 追加评论
	add_commt_num = StringField()
	# 商品评论信息
	product_commentinfo = ListField()

	meta = {
		"collection":"jd_phone_info",
		"ordering":['-product_price'],
	}

class user_info(Document):
	#用户名
	user_name = StringField(required=True)
	#密码
	password = StringField(required=True)
	phone_num = StringField(max_length=11)
	meta = {
		"collection":"user_info",
	}
