from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


browser = webdriver.Chrome(r"C:\Users\saifc\Downloads\chromedriver_win32\chromedriver.exe")
browser.get('https://www.oyorooms.com/')      
time.sleep(2)                                             
search = browser.find_element_by_xpath('//*[@id="autoComplete__home"]') #//*[@id="autoComplete__home"]
# find_element will give us the element having Xpath as subjectInput 
search.send_keys('delhi')                        
time.sleep(2)       
#browser.find_elements_by_class_name('js_ripple search-btn search-flights-btn eventTrackable js-prodSpecEvtCat').click()                                  # 5 
search.send_keys(Keys.ENTER)
time.sleep(2)
#search.send_keys(Keys.ENTER)   
browser.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/div[3]/div/div[1]/div/div[4]/button').click()  #u-textCenter searchButton searchButton--home
#data = browser.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/section/div/div[2]/div[1]/div/div[2]/div/div[1]/div[2]/div/a')[0] 
elements = browser.find_elements(By.CLASS_NAME,'listingPrice__finalPrice').get_text()
print(elements)

#browser.quit()