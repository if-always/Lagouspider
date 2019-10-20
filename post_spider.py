import re
import json
import time
import math
import Mysql
import requests
from contextlib import closing


class CrawlLaGou:

    def __init__(self,keyword):
        
        
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }

        self.origin_url = "https://www.lagou.com/jobs/list_/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput="
        self.keyword = keyword
        self.session = requests.session()
        self.results = []
    
    def get_reponse(self,method,url,data=None,info=None):
        while True:

            if method == "GET":
                with closing(self.session.get(url=url,headers=self.header)) as response:
                    response.encoding = "utf8"
                    return response.text
            else :
                with closing(self.session.post(url=url, headers=self.header, data=data)) as response:
                    response.encoding = "utf8"

                    if '频繁' in response.text:
                        
                        self.session.cookies.clear()
                        first_request_url = f"https://www.lagou.com/jobs/list_{self.keyword}?city={info}&cl=false&fromSearch=true&labelWords=&suginput="
                        self.get_reponse(method="GET", url=first_request_url)
                        time.sleep(10)
                        continue
                    return response.text



    def get_hotcity(self):
        
        search = re.compile(r'class="more-city-name">(.*?)</a>')
        result = self.get_reponse(method="GET", url=self.origin_url)
        self.city_list = search.findall(result)
        self.session.cookies.clear()

    
    def get_sumpage(self,city):
        data = {
                "pn":1,
                "kd":f"{self.keyword}"
            }

        jobsurl = f"https://www.lagou.com/jobs/positionAjax.json?city={city}&needAddtionalResult=false"
        
        referers = f"https://www.lagou.com/jobs/list_{self.keyword}?city={self.keyword}&cl=false&fromSearch=true&labelWords=&suginput="
        self.header['Referer'] = referers.encode()
        response = self.get_reponse(method="POST",url=jobsurl,data=data,info=city)
        lagou_data = json.loads(response)
        
        numbers = lagou_data['content']['positionResult']['totalCount']
        sumpage = math.ceil(numbers/15)
        
        return sumpage
    
    def get_cityjobs(self,city):
        
        
        for page in range(1,self.get_sumpage(city)+1):
                
            data = {
                "pn":page,
                "kd":f"{self.keyword}"
            }

            jobsurl = f"https://www.lagou.com/jobs/positionAjax.json?city={city}&needAddtionalResult=false"
            referers = f"https://www.lagou.com/jobs/list_{self.keyword}?city={self.keyword}&cl=false&fromSearch=true&labelWords=&suginput="
            self.header['Referer'] = referers.encode()
            response = self.get_reponse(method="POST",url=jobsurl,data=data,info=city)
            
            lagou_data = json.loads(response)
            
            result_list = lagou_data['content']['positionResult']['result']
            
            for result in result_list:
                yield {
                    'city':result.get('city'),
                    'salary':result.get('salary'),
                    'district':result.get('district'),
                    'workYear':result.get('workYear'),
                    'latitude':result.get('latitude'),
                    'longitude':result.get('longitude'),
                    'companyId':result.get('companyId'),
                    'jobNature':result.get('jobNature'),
                    'education':result.get('education'),
                    'firstType':result.get('firstType'),
                    'secondType':result.get('secondType'),
                    'linestaion':result.get('linestaion'),
                    'positionId':result.get('positionId'),
                    'createTime':result.get('createTime'),
                    'companySize':result.get('companySize'),
                    'skillLables':''.join(result.get('skillLables')) if isinstance(result.get('skillLables'),list) else result.get('skillLables'),
                    'positionName':result.get('positionName'),
                    'financeStage':result.get('financeStage'),
                    'businessZones':''.join(result.get('businessZones')) if isinstance(result.get('businessZones'),list) else result.get('businessZones'),
                    'positionLables':''.join(result.get('positionLables')) if isinstance(result.get('positionLables'),list) else result.get('positionLables'),
                    'companyFullName':result.get('companyFullName'),
                    'positionAdvantage':result.get('positionAdvantage'),
                    
                }
            time.sleep(1)
            
                    


    
    
if __name__ == '__main__':
    lagou = CrawlLaGou("数据")
    lagou.get_hotcity()
    city = "北京"
    datas = lagou.get_cityjobs(city)

    jobs_data = []
    for data in datas:
        print(data)
        jobs_data.append(data)
        #break
    args_list = []
    for k,v in jobs_data[0].items():
      args_list.append(k)
    Mysql.Insert_args("Lagou","datajobs",jobs_data,args_list)
    
    