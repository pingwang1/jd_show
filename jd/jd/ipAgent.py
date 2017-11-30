import requests
from lxml import etree
import random
import re
import time


#ip代理类:只抓取http/https类型ip
class IPAgency(object):

	def __init__(self):
		self.url = "" #初始抓取西刺网站
		self.ipList = []
		self.content = ""

	def get_page(self):
		#设置代理ｉｐ地址
		# proxy = {"http":"124.65.195.162:8080"}
		proxy = {"http":"123.57.85.224:80"}
		#设置请求头
		headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.8',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3107.4 Safari/537.36',
			'Referer':'http://www.xicidaili.com/',
			'Host':'www.xicidaili.com',
			'If-None-Match':'W/"4b2a9f317920e16e4df6f3b6bcce8eee"',
			'Connection':'keep-alive',
		}
		while True:
			try:
				#获取网页源码
				self.content = requests.get(self.url,proxies=proxy,headers=headers).text
				break
			except Exception as e:
				print("网页打开失败." + str(e))
				time.sleep(1)


	#获取ｉｐ地址
	def get_iplist(self):
		self.get_page()
		html = etree.HTML(self.content)
		# print(etree.tostring(html,encoding="unicode"))
		tr_list = html.xpath("//table[@id='ip_list']/tr[position()>1]")
		ip_list = []
		for tr in tr_list:
			#剔除链接时间大于１ｓ的代理ｉｐ地址
			if tr.xpath(".//td[@class='country']/div/@title")[0].split("秒")[0] < "1":
				ip = tr.xpath("td[2]")[0].text
				port = tr.xpath("td[3]")[0].text
				ip_list.append(ip+":"+port)

		self.ipList = ip_list


	def get_http_random_ip(self):
		self.url = "http://www.xicidaili.com/wt/"
		return self.get_ip()

	#根据ｈｔｔｐ/ｈｔｔｐｓ获取Ｉｐ
	def get_ip(self):
		self.get_iplist()
		# 获取ｉｐ列表的长度
		ip_len = len(self.ipList)
		if ip_len > 0:
			num = random.randint(0, ip_len)
			if len(self.ipList) == 0:
				return ""
			return self.ipList[num]
		else:
			self.get_iplist()
		return ""

	def get_https_random_ip(self):
		self.url = "http://www.xicidaili.com/wn/"
		return self.get_ip()

if __name__ == '__main__':
	ip = IPAgency()
	print(ip.get_http_random_ip())

