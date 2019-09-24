import time
import requests

position = "python"
city = "苏州"

url = f"https://www.lagou.com/jobs/list_{position}?px=default&city={city}#filterBox"


 
def get_content():
    city = "苏州"
    for p in range(3):
        # 构造第一个请求头
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Host': 'www.lagou.com',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers1)  #获取不同城市的源码
        
 
 
        for i in range(1,4):#最多页数的深圳也只有3页！
            # ajax网页的请求头，和之前的不一样！
            headers = {
                # 不加cookie就可以出现真实源码,请求头添加原则：添加和其他网页不同的部分
                # 拉钩网的反爬虫比较强，添加Cookie要添加登录后的Cookie
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=python',
    
                'Origin': 'https://www.lagou.com',
                'Host': 'www.lagou.com',
                'X-Anit-Forge-Code': '0',
                'X-Anit-Forge-Token': 'None',
                'X-Requested-With': 'XMLHttpRequest',
            }
 
            # 网址参数
            params = {
                'needAddtionalResult': 'false',
                'city': city  # 城市转换编码后的结果
            }
            data = {
                'kd': position,  # Python爬虫转换编码后的结果，关键字
                'first': 'true',  # 转码网址：http://tool.chinaz.com/tools/unicode.aspx
                'pn': str(i),  # 页数
            }
 
 
            r = requests.utils.dict_from_cookiejar(response.cookies)  # 获取cookies
            print(r)
            # 构造cookie参数
            r['user_trace_token'] = r['user_trace_token']
            r['JSESSIONID'] = r['JSESSIONID']
            r['SEARCH_ID'] = r['SEARCH_ID']
 
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
            cookies.update(r)  # 更新接口的cookie
 
            html=requests.post('https://www.lagou.com/jobs/positionAjax.json'
                               ,headers=headers,cookies=cookies,data=data,params=params)   #职位所在的异步网页是post请求
 
            # print(r)  #此时的cookie不显示！
            html=html.json()   #在一些网页中下载json可能会出现16进制码，可以导入json包，使用dump方法
            # print(html)
 
        #新问题！通过在https://www.json.cn/中格式化json数据，发现拉勾网识别出爬虫并且返回假数据！！！
        #但是我们加上formdata中的data后，再次请求就可以了
            result=html['content']['positionResult']['result']  #此时是列表了，列表里面是字典
 
            #由于列太多，所以把数据导入到数据库
            for i in result:
                city=i['city']  #城市
                positionName=i['positionName']   #职位名称
                workYear=i['workYear']   #工作年限
                education=i['education']  #学历
                salary=i['salary']  #薪资
                industryField=i['industryField'] #公司领域
                companyFullName=i['companyFullName']  #公司全名
                companyLabelList=','.join(i['companyLabelList'])  #列表是公司福利，转为字符串
                district=i['district']  #详细地址
                print(salary)
            time.sleep(2)
 
get_content()
