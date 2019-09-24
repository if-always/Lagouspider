import time
import math
import requests


class Lagouspider(object):
	"""docstring for Lagouspider"""
	def __init__(self, city, keyword):
		
		self.city = city
		self.keyword = keyword
		self.url = f"https://www.lagou.com/jobs/list_{keyword}?px=default&city={city}#filterBox"
		
	def get_response(self):
		
		headers ={
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            		'Host': 'www.lagou.com',
            		'Upgrade-Insecure-Requests': '1',
				 }
		response = requests.get(url=self.url,headers=headers)
		return response

	def get_json(self,num):

		response = self.get_response()
		my_headers = {
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                		'Referer': f'https://www.lagou.com/jobs/list_{self.keyword}?px=default&city=',
                		'Origin': 'https://www.lagou.com',
                		'Host': 'www.lagou.com',
                		'X-Anit-Forge-Code': '0',
                		'X-Anit-Forge-Token': 'None',
                		'X-Requested-With': 'XMLHttpRequest',
		}

		my_param = {
					'needAddtionalResult': 'false',
                	'city': self.city
            
		}

		my_data = {
					'kd': self.keyword, 
                	'first': 'true',
                	'pn': str(num),
		}

		r = requests.utils.dict_from_cookiejar(response.cookies)
		
		#print(r)
		r['X_HTTP_TOKEN'] = r['X_HTTP_TOKEN']
		r['user_trace_token'] = r['user_trace_token']
		r['JSESSIONID'] = r['JSESSIONID']
		r['SEARCH_ID'] = r['SEARCH_ID']
		#print(r)


		cookies = {
		'_gat': '1',
		'PRE_UTM': '',
		'hasDeliver': '0',
		'showExpriedMyPublish': '1',
		'showExpriedCompanyHome': '1',
		'showExpriedIndex': '1',
		'login': 'true',
		'sajssdk_2015_cross_new_user': '1',
		'PRE_HOST': 'blog.csdn.net',
		'TG-TRACK-CODE': 'search_code',
		'LGRID': '20190324213839-21d2ecda-4e3a-11e9-b493-5254005c3644',
		'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1553434719',
		'SEARCH_ID': '6ad9250f920c43d3a6145d14253f4c79',
		'X_MIDDLE_TOKEN': 'ea516bb77285d71a3f70c60654f86a6a',
		'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1553427486,1553429096,1553434584,1553434601',
		'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D%3FlabelWords%3Dhot',
		'JSESSIONID': 'ABAAABAAADEAAFIA7A0A6CE93C3B7F272ABD8DC5BC6DAA8',
		'_ga': 'GA1.2.161595218.1553427486',
		'_gid': 'GA1.2.1268872210.1553427486',
		'user_trace_token': '20190324193806-4aaf56a0-4e29-11e9-8ac8-525400f775ce',
		'LGUID': '20190324193806-4aaf59b0-4e29-11e9-8ac8-525400f775ce',
		'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22169afb5765410c-00ad34089f8264-3c604504-2073600-169afb576551bf%22%2C%22%24device_id%22%3A%22169afb5765410c-00ad34089f8264-3c604504-2073600-169afb576551bf%22%7D',
		'LG_LOGIN_USER_ID': '96d26cc9a60fb19d8f1c8ffff5f9068b92c1d8f3c024b59b817b841c0c3a5bff',
		'PRE_SITE': 'https%3A%2F%2Fblog.csdn.net%2Fqq_37462361%2Farticle%2Fdetails%2F87856659',
		'LGSID': '20190324213624-d177e32c-4e39-11e9-8af2-525400f775ce',
		'_putrc': 'C4C6A5FE2C61AA92123F89F2B170EADC',
		'unick': '%E5%8F%B6%E7%90%86%E4%BD%A9',
		'gate_login_token': 'd0a8a428cd39437390e15e201294324c466e65461414742cd90eaadddfb52e3f',
		'index_location_city': '%E5%B9%BF%E5%B7%9E',
		}
		cookies.update(r)


		html=requests.post('https://www.lagou.com/jobs/positionAjax.json'
		,headers=my_headers,cookies=cookies,data=my_data,params=my_param)   #职位所在的异步网页是post请求

		# print(r)  #此时的cookie不显示！
		html=html.json()

		result = html['content']['positionResult']
		
		return result

	def get_pages(self):
		totalcounts = self.get_json(1)['totalCount']
		#print(totalcounts)
		res = math.ceil(int(totalcounts)/15)
		print(res)
a = Lagouspider("全国", "Java")
a.get_pages()
