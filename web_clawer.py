from selenium import webdriver
import requests
import bs4
from time import sleep
import pandas as pd
import os
import preprocessing

#設定driver屬性
def driver_settings() : 
	options = webdriver.ChromeOptions()
	options.add_argument("user-agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'")
	prefs = {"profile.managed_default_content_settings.images": 2}
	options.add_experimental_option('prefs' , prefs)

	return options

#登入選課系統，回傳driver物件和選課的側邊欄位
def CCU_login(options) : 
	
	driver = webdriver.Chrome(chrome_options = options)

	login_url = "https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/login.php?m=0"
	res = driver.get(login_url)
	driver.maximize_window()

	user_name_input = driver.find_element_by_xpath(u"/html/body/font/center/form/table/tbody/tr[2]/td[2]/input")
	user_name_input.send_keys(u"406530031")
	password_input = driver.find_element_by_xpath(u"/html/body/font/center/form/table/tbody/tr[3]/td[2]/input")
	password_input.send_keys(u"123456789")

	enter_btn = driver.find_element_by_xpath("/html/body/font/center/form/table/tbody/tr[6]/td/input[1]")
	enter_btn.click()
	
	home_page_url = driver.current_url
	
	return driver , home_page_url

#點擊側邊欄位的"加選"按鈕，進入所有系所的頁面
def CCU_get_dpt_page(driver , home_page_url) : 
	add_course_btn = driver.find_element_by_xpath("//*[@id='itemTextLink4']")
	dpt_page_url = add_course_btn.get_attribute(name = "href")
	
	return driver , dpt_page_url

#從所有系所的頁面進入資管系的頁面，並爬取所有年級的開課檔案
#pd.read_html 好像抓不到= =
def CCU_get_mis_df(driver , dpt_page_url) : 
	mis_df_lst = []
	
	driver.get(dpt_page_url)
	mis_btn = driver.find_element_by_xpath("//*[@id='form1']/table/tbody/tr[2]/td/table/tbody/tr[2]/td[5]/font/input[11]")
	mis_btn.click()
	search_class_btn = driver.find_element_by_xpath("//*[@id='form1']/input[6]")
	search_class_btn.click()
	
	mis_df_lst.append(process_tables(driver.page_source))

	page_lst = CCU_get_other_grades_page_source(driver)
	for i in range(len(page_lst)) : 
		mis_df_lst.append(process_tables(page_lst[i]))

	df = preprocessing.concat_inlist_df(mis_df_lst)
	print(df)


	
#爬取2 ~ 4年級的page_source
def CCU_get_other_grades_page_source(driver) : 
	page_lst = []

	for i in range(2 , 5) :
		#等等確認其他系是不是也是這個模式 
		grade_btn = driver.find_element_by_xpath("/html/body/center/form/table/tbody/tr[3]/th[1]/form/a[" + str(i) + "]")
		grade_btn.click()
		page_lst.append(driver.page_source)
	
	return page_lst


def process_tables(page) : 
	
	'''
	page = ""
	path = os.getcwd()
	with open(path + "/data/src.txt" , "r" , encoding = "utf-8") as file : 
		for i in file.readlines() : 
			page += i
	'''


	soup = bs4.BeautifulSoup(page , 'lxml')

	tbody_tag = soup.select_one("body > center > form > table > tbody > tr:nth-child(1) > th > table > tbody")
	tags = list(tbody_tag.find_all("th"))

	#暫放一堆資料的，等等會把裡面的資料做成df
	source_lst = []

	for j in tags : 
		if j.string : 
			source_lst.append(j.text.strip())
		else : 
			s = j.find("font")
			if s : 
				temp = s.text.strip()
				temp = temp.replace("\n" , "")
				temp = temp.replace(" " , "")
				source_lst.append(temp)

	#將第一個項("標記")刪除，因為爬不到他下面的東西，所以先在這裡直接刪除，以免妨礙後面的切片
	source_lst.pop(0)
	
	#暫存成等等df可以接受的格式的list，ct用於計數，temp用於暫存list
	pre_df_lst = []
	ct = 0
	temp = []

	for j in range(len(source_lst)) : 
		temp.append(source_lst[j])
		ct += 1
		if ct % 12 == 0 : 
			pre_df_lst.append(temp)
			temp = []
		
	df = pd.DataFrame(pre_df_lst[1:] , columns = pre_df_lst[0])
		
	return df













def req_test(url) : 
	req = requests.get(url)
	req.encoding = "utf-8"
	soup = bs4.BeautifulSoup(req.text , 'lxml')
	print(soup.prettify())