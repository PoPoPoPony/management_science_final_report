from selenium import webdriver
import requests
import bs4
from time import sleep


def driver_settings() : 
	options = webdriver.ChromeOptions()
	options.add_argument("user-agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'")
	prefs = {"profile.managed_default_content_settings.images": 2}
	options.add_experimental_option('prefs' , prefs)

	return options

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


def CCU_dpt_page(driver , home_page_url) : 
	add_course_btn = driver.find_element_by_xpath("//*[@id='itemTextLink4']")
	dpt_page_url = add_course_btn.get_attribute(name = "href")
	driver.get(dpt_page_url)
	sleep(3)



def req_test(url) : 
	req = requests.get(url)
	req.encoding = "utf-8"
	soup = bs4.BeautifulSoup(req.text , 'lxml')
	print(soup.prettify())
