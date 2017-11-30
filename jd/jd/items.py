# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #店铺名
    shop_name=scrapy.Field()
    #商品名
    product_name = scrapy.Field()
    #商品id
    product_id = scrapy.Field()
    # 商品id
    product_url = scrapy.Field()
    #商品价格
    product_price = scrapy.Field()
    #评论总数
    comment_num = scrapy.Field()
    #好评
    good_commt_num = scrapy.Field()
    #color
    product_color =scrapy.Field()
    #中评
    gen_commt_num = scrapy.Field()
    #差评
    bad_commt_num = scrapy.Field()
    #追加评论
    add_commt_num = scrapy.Field()
    #商品评论信息
    product_commentinfo = scrapy.Field()
    #评论用户名
    user_name = scrapy.Field()
    #jd等级
    jd_level = scrapy.Field()
    #内容
    content = scrapy.Field()
    #评论星级
    comment_star = scrapy.Field()
    #时间
    push_date = scrapy.Field()
    #评论的点赞数
    comment_good = scrapy.Field()

