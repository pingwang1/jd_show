# -*- coding: utf-8 -*-
import scrapy
import time
import re
import json
from jd.items import JdItem
from scrapy_redis.spiders import RedisSpider


class JdPhoneSpider(RedisSpider):
    page = 0
    name = 'jd_phone'
    allowed_domains = ['jd.com','p.3.cn']
    # start_urls = ['https://list.jd.com/list.html?cat=9987,653,655&page=1&sort=sort_rank_asc']
    redis_key = 'jd_phone:start_urls'

    def parse(self, response):
        print("正在抓取%s的页面内容"%(response.url))
        self.page +=1
        #获取包含商品的ul
        ul = response.xpath('//ul[contains(@class, "gl-warp")]/li')
        for li in ul:
            items = JdItem()
            items['shop_name'] = li.xpath('./div/div[@class="p-shop"]/@data-shop_name').extract_first()
            items['product_name'] = li.xpath('./div[1]/div[4]/a/em/text()').extract_first().strip()
            items['product_id'] = li.xpath('./div[@class="gl-i-wrap j-sku-item"]/@data-sku').extract_first()
            items['product_url'] = li.xpath('./div//div[@class="p-img"]/a/@href').extract_first()
            #获取价格，进入价格页面
            url = 'https://p.3.cn/prices/mgets?callback=jQuery1493916&skuIds=J_'+items['product_id'] +'&pduid=%s'%(time.time())
            yield scrapy.Request(url=url,callback=self.parse_price,meta={"item":items})
        #获取下一页(只抓取１０页)
        if self.page<10:
            try:
                next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()
                yield scrapy.Request(url ='https://list.jd.com'+next_url,callback=self.parse)
            except Exception as e:
                print("获取下一页链接失败>>%s"%e)
        else:
            print("抓取%s页数据结束！"%self.page)

    #解析价格
    def parse_price(self,response):
        items = response.meta['item']
        # print(items)
        try:
            #获得价格
            reg =re.compile(r'\"p\":\"(.*?)\"}',re.S)
            items['product_price'] = float(reg.search(response.text).group(1))
            #进入页
            url ='http://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=5&page=0&pageSize=10'%items['product_id']
            yield scrapy.Request(url=url,callback=self.parse_comment,meta={"item":items})
        except Exception as e:
            print("获取价格失败原因%s"%e)

    #解析评论数量以及信息
    def parse_comment(self,response):
        # 进入评论信息的接口页面
        items = response.meta['item']
        items['comment_num'] = re.compile(r'\"commentCount\":(.*?),',re.S).search(response.text).group(1)
        items['good_commt_num'] = re.compile(r'\"goodCount\":(.*?),', re.S).search(response.text).group(1)
        items['gen_commt_num'] = re.compile(r'\"generalCount\":(.*?),', re.S).search(response.text).group(1)
        items['bad_commt_num'] = re.compile(r'\"poorCount\":(.*?),', re.S).search(response.text).group(1)
        items['add_commt_num'] = re.compile(r'\"afterCount\":(.*?),', re.S).search(response.text).group(1)

        #抓product_commentinfo列表
        items['product_commentinfo']=[]
        comments = re.compile(r'\"comments\":(.*)\}',re.S).search(response.text).group().replace('"comments":','{"comments":')
        # 把json格式字符串转换成python对象
        commentsinfos = json.loads(comments)
        #循环遍历
        for commentinfo in commentsinfos['comments']:
            commentsinfo_dict = {}
            # print(commentinfo)
            commentsinfo_dict['user_name'] = commentinfo["nickname"]
            commentsinfo_dict['jd_level'] =commentinfo["userLevelName"]
            commentsinfo_dict['content'] =commentinfo["content"]
            commentsinfo_dict['comment_star'] =commentinfo["score"]
            commentsinfo_dict['push_date'] =commentinfo["creationTime"]
            commentsinfo_dict['comment_good'] = commentinfo["usefulVoteCount"]
            commentsinfo_dict['product_color'] = commentinfo["productColor"]
            print(commentsinfo_dict['product_color'])
            items['product_commentinfo'].append(commentsinfo_dict)
        print(items)
        return items

