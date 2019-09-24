import os
import re
import json
import time
from pyquery import PyQuery 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC





class Lagouspider:
	"""docstring for Lagouspider"""
	def __init__(self):
		
		self.url = "https://www.lagou.com/"
		self.driver = webdriver.Chrome(executable_path="F:/chromedriver.exe",options=webdriver.ChromeOptions())

	def run(self):
		self.driver.get(self.url)

		try:
			WebDriverWait(self.driver,timeout = 3).until(
                    EC.presence_of_element_located((By.ID,'cboxClose'))
                )
			self.driver.find_element_by_id("cboxClose").click()
		except:
			self.driver.find_element_by_id("cboxClose").click()
		time.sleep(1)

		self.driver.find_element_by_id("search_input").send_keys("Python")
		self.driver.find_element_by_id("search_button").click()
		try:
		#print(self.driver.current_url)
			WebDriverWait(self.driver,timeout = 3).until(
	                EC.presence_of_element_located((By.ID,'tab_pos'))
	            )
			self.driver.find_element_by_link_text("苏州").click()
		except Exception as e:
			print("error:"+ str(e))
			self.driver.close()
			os._exit(0)
		try:
			WebDriverWait(self.driver,timeout = 3).until(
	                EC.presence_of_element_located((By.LINK_TEXT,'工业园区'))
	            )
			
		except Exception as e:
			print("error:"+ str(e))
			self.driver.close()
			os._exit(0)
		
		
		html = self.driver.page_source
		
		
		#self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[@action="next"]').click()
		
		while True:
			
			time.sleep(1)
			self.get_infos(html)
			try:

				WebDriverWait(self.driver,timeout = 3).until(
                        EC.presence_of_element_located((By.XPATH,'//div[@class="pager_container"]/span[@action="next"]'))
                    )
				sumbmitBtn = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[@action="next"]')
				if "pager_next pager_next_disabled" in sumbmitBtn.get_attribute("class"):
				    print("break")
				    break
				else:
					sumbmitBtn.click() # 点击下一页
					break
			except Exception as e:
				print("error:"+ str(e))
				self.driver.close()
				os._exit(0)
		self.driver.close()
	def get_infos(self,html):

		doc = PyQuery(html)

		infos = doc("li.con_list_item").items()

		for info in infos:
			position = info.find("div.list_item_top div.position a h3").text()
			district = re.sub(r'\W','',info.find("div.list_item_top div.position a span").text())
			posihref = info.find("div.list_item_top div.position a").attr("href")
			positaid = info.find("div.list_item_top div.position a").attr("data-lg-tj-cid")
			posalary = info.find("div.list_item_top div.position div.li_b_l span").text()
			prequire = info.find("div.list_item_top div.position div.li_b_l").text()
			
			compname = info.find("div.list_item_top div.company div.company_name a").text()
			comphref = info.find("div.list_item_top div.company div.company_name a").attr("href")
			compacid = info.find("div.list_item_top div.company div.company_name a").attr("data-lg-tj-cid")
			complogo = info.find("div.list_item_top div.com_logo a img").attr("src")
			industry = info.find("div.list_item_top div.company div.industry").text()
			
			comptype = info.find("div.list_item_bot div.li_b_l").text()
			comwalre = info.find("div.list_item_bot div.li_b_r").text()
			print(comwalre)
l = Lagouspider()
l.run()
