from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
from tabulate import tabulate
import os
from pandas import ExcelWriter
from pandas import ExcelFile
import time
import requests
from selenium.webdriver.chrome.options import Options



#launch url
url = "https://twitter.com/Govsia/followers"
chrome_options = webdriver.ChromeOptions()
# create a new Firefox session
#driver = webdriver.Firefox()
chrome_options.add_argument('--ignore-ssl-errors=true')
chrome_options.add_argument('--ssl-protocol=any')
chrome_options.add_argument('--web-security=false')
chrome_options.add_extension(r'C:\Users\Femi\Downloads\chrome-csp-disable-master')
#chrome_options.add_extension(r"C:\Users\Femi\Downloads\campaign_pic\disableCSP")
driver = webdriver.Chrome(executable_path=r"C:\Users\Femi\Downloads\chromedriver_win32\chromedriver.exe", chrome_options=chrome_options)
#driver = webdriver.Ie(executable_path=r"C:\Users\Femi\Downloads\chromedriver_win32\IEDriverServer.exe")
driver.implicitly_wait(90)
driver.get(url)

#After opening the url above, Selenium clicks the specific agency link

#python_button = driver.find_elements_by_class_name('u-linkComplex-target') #FHSU
#python_button.click() #click fhsu link

#Selenium hands the page source to Beautiful Soup
##t_end = time.time() + 30 * 40
##time.sleep(1)
##while time.time() < t_end:
##    time.sleep(2)
##    driver.find_element_by_tag_name('body').send_keys(Keys.END)
##    
##    print('scrolling...')
time.sleep(300)
def check_connection(url='http://www.google.com/', timeout=600):
    try:
        req = requests.get(url, timeout=timeout, headers={"Content-Security-Policy":"script-src 'https://ssl.google-analytics.com' 'self' 'unsafe-inline' 'unsafe-eval'"})
        # HTTP errors are not raised by default, this statement does that
        req.raise_for_status()
        return True
    except requests.HTTPError as e:
        print("Checking internet connection failed, status code {0}.".format(
        e.response.status_code))
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

def scroll():
    time.sleep(30)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(30)
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        conn = check_connection()
        while conn == False:
            time.sleep(10)
            print ("waiting for internet to resume..............")
            conn = check_connection() 
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        print('scrolling...')
        time.sleep(5)
        if lastCount==lenOfPage:
            match=True
            print('end of scrolling...')
            time.sleep(10)
i = 0
while i<30:
    scroll()
    i+=1


soup_level1=BeautifulSoup(driver.page_source, 'html.parser')

datalist = [] #empty list
x = 0 #counter

#Beautiful Soup finds all Job Title links on the agency page and the loop begins
for link in soup_level1.find_all('b', attrs={'class':'u-linkComplex-target'}):
    
    #Selenium visits each Job Title page
#    python_button = driver.find_element_by_class_name('u-linkComplex-target' + str(x))
   # python_button.click() #click link
##    target = driver.find_element_by_class_name('ProfileCard-content')
##    driver.execute_script('arguments[0].scrollIntoView(true);', target)
##    target.location_once_scrolled_into_view

    
    #Selenium hands of the source of the specific job page to Beautiful Soup
##    soup_level2=BeautifulSoup(driver.page_source, 'html.parser')
##
##    #Beautiful Soup grabs the HTML table on the page
##    table = soup_level2.find_all('b', attrs={'class':'u-linkComplex-target'})
##    first_result = table[x]
##    print(first_result)
    
    #Giving the HTML table to pandas to put in a dataframe object
    #df = pd.read_html(str(b),header=0)
    df = link.string
    
    #Store the dataframe in a list
    datalist.append(df)
    
    #Ask Selenium to click the back button
##    driver.execute_script("window.history.go(-1)") 
    
    #increment the counter variable before starting the loop over
    x += 1
    
    #end loop block
    
#loop has completed

#end the Selenium browser session
#driver.quit()
    
print(datalist)
df2 = pd.DataFrame(datalist)
#combine all pandas dataframes in the list into one big dataframe
#result = pd.concat([pd.DataFrame(datalist[i]) for i in range(len(datalist))],ignore_index=True)

writer = pd.ExcelWriter('target_users3.xlsx')
df2.to_excel(writer, sheet_name = 'Sheet1')
writer.save()
print('Successful...')
