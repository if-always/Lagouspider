import time
import math
import requests


class Lagouspider(object):
	"""docstring for Lagouspider"""
	def __init__(self, city, keyword):
		
		self.city = city
		self.keyword = keyword
		self.code = self.get_code()
		self.url = f"https://www.lagou.com/jobs/list_{self.keyword}?px=default&city=" + str("{}#filterBox".format(self.code))
		
	def get_code(self):
		
		codes = {
			'苏州':'%E8%8B%8F%E5%B7%9E',
			'上海':'%E4%B8%8A%E6%B5%B7',
			'北京':'%E5%8C%97%E4%BA%AC'
		}
		return codes.get(self.city)

	def get_response(self):
		
		headers ={
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            		'Host': 'www.lagou.com',
            		'Upgrade-Insecure-Requests': '1',
				 }
		response = requests.get(url=self.url,headers=headers)
		return response

	def get_json(self,page,response):

		
		my_headers = {
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                		'Referer': f'https://www.lagou.com/jobs/list_{self.keyword}?labelWords=sug&fromSearch=true&suginput={self.keyword}',
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
		#print(my_param)
		my_data = {
					'kd': self.keyword, 
                	'first': 'true',
                	'pn': str(page),
		}
		#print(my_data)
		r = requests.utils.dict_from_cookiejar(response.cookies)
		
		
		# r['X_HTTP_TOKEN'] = r['X_HTTP_TOKEN']
		# r['user_trace_token'] = r['user_trace_token']
		# r['JSESSIONID'] = r['JSESSIONID']
		# r['SEARCH_ID'] = r['SEARCH_ID']
		#print(r)


		cookies = {
		'_gat': '1',
		'PRE_UTM': '',
		'hasDeliver': '2',
		'showExpriedMyPublish': '1',
		'showExpriedCompanyHome': '1',
		'showExpriedIndex': '1',
		'login': 'true',
		'TG-TRACK-CODE': 'index_search',
		'LGRID': '20190925194842-6c3be980-df8a-11e9-a52b-5254005c3644',
		'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1569412123',
		'SEARCH_ID': '71f8a5ed0c9444059ca1c1c3ce024d99',
		'X_MIDDLE_TOKEN': 'ed61c2cff752f343f9886c12b551bb77',
		'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1569326148,1569326748,1569372165,1569408080',
		'JSESSIONID': 'ABAAABAABEEAAJA47BA0A17FF50B026D37D336F9E5360C0',
		'_ga': 'GA1.2.818763548.1537266900',
		'_gid': 'GA1.2.1034959748.1569197306',
		'user_trace_token': '20180918183502-8034fe66-bb2e-11e8-a1f7-525400f775ce',
		'LGUID': '20180918183502-8035040e-bb2e-11e8-a1f7-525400f775ce',
		'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221665cccef065ba-0601059e1962eb-43480420-1049088-1665cccef07362%22%2C%22%24device_id%22%3A%221665cccef065ba-0601059e1962eb-43480420-1049088-1665cccef07362%22%2C%22props%22%3A%7B%22%24latest_utm_source%22%3A%22m_cf_cpt_baidu_pc%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
		'PRE_SITE': 'https%3A%2F%2Fblog.csdn.net%2Fqq_37462361%2Farticle%2Fdetails%2F87856659',
		'LGSID': '20190925184119-0227fc89-df81-11e9-a52b-5254005c3644',
		'_putrc': '145F731F90C7833B123F89F2B170EADC',
		'unick': '%E8%96%84%E5%A0%89%E6%9E%97',
		'gate_login_token': '16e4ccf9950391a253be0a82133e94feb912a209b818b01f1491cd0f36d492ac',
		'index_location_city': '%E5%85%A8%E5%9B%BD',
		}
		cookies.update(r)


		html=requests.post('https://www.lagou.com/jobs/positionAjax.json'
		,headers=my_headers,cookies=cookies,data=my_data,params=my_param)   #职位所在的异步网页是post请求

		# print(r)  #此时的cookie不显示！
		html=html.json()

		result = html['content']['positionResult']
		
		return result

	def get_pages(self,response):
		totalcounts = self.get_json(1,response)['totalCount']
		#print(totalcounts)
		pages = math.ceil(int(totalcounts)/15)
		print(f"******职位总个数为{totalcounts}个 , 共{pages}页******")
		return pages



	def get_infos(self,pages,response):
		for i in range(1,pages+1):
			print(f"******正在获取第{i}页数据******")
			result = self.get_json(i,response)

			infos = result.get('result')
			for info in infos:
				city = info.get('city')
				salary = info.get('salary')
				latitude = info.get('latitude')
				district = info.get('district')
				workYear = info.get('workYear')
				longitude = info.get('longitude')
				jobNature = info.get('jobNature')
				firstType = info.get('firstType')
				education = info.get('education')
				companyId = info.get('companyId')
				createTime = info.get('createTime')
				companySize = info.get('companySize')
				positionId = info.get('positionId')
				skillLables = info.get('skillLables')
				industryField = info.get('industryField')
				positionName = info.get('positionName')
				companyFullName = info.get('companyFullName')
				companyLabelList = info.get('companyLabelList')
				positionAdvantage = info.get('positionAdvantage')

				print(positionName)
			time.sleep(2)


	def main(self):

		response = self.get_response()

		pages = self.get_pages(response)
		#print(pages)
		result = self.get_infos(pages,response)
		
a = Lagouspider("北京", "nlp")

a.main()

# pages = a.get_pages()

# a.get_infos(pages)
