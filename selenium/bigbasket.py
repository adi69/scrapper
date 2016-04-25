from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

cities = ['Delhi-Noida', 'Gurgaon', 'Kolkata', 'Mumbai', 'Pune', 'Ahmedabad-Gandhinagar', 'Bangalore', 'Hyderabad', 'Chennai']

def get_cookie(city):
    driver = webdriver.Firefox()
    driver.get("http://www.bigbasket.com/choose-city/?next=/cl/fruits-vegetables/")
    select = Select(driver.find_element_by_id("ftv-city-selectboxdiv"))
    select.select_by_visible_text(city)
    driver.add_cookie(driver.get_cookies())
    driver.find_element_by_id("skip_explore").click()
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['name'] == '_bb_vid':
            print "cookie['%s'] = {'_bb_vid' : %s,}" % (city, cookie['value'])


for city in cities: 
    try:
        get_cookie(city)
    except Exception as e:
        print "[%s]: %s" % (city, e)

