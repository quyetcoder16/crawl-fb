from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get("https://www.facebook.com/CeceFoodOnline")
time.sleep(2);

data_post = pd.DataFrame({"title":[],"time":[],"like":[],"share":[],"url":[]});
numPost = 20
try:
    btnClose = driver.find_elements(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div')
    btnClose[0].click()
    
    for i in range(numPost):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1);
        
    container = driver.find_elements(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div");
  
    for _count in range(1,numPost+1):
        _time = container[0].find_element(By.XPATH,f".//div[{_count}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span/a/span");
        postTime  = _time.text;
        postTitle = container[0].find_element(By.XPATH,f".//div[{_count}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div").get_attribute("outerHTML");
        postLike = container[0].find_element(By.XPATH,f".//div[{_count}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/span[2]/span/span").text;
        try:
            postShare = container[0].find_element(By.XPATH,f".//div[{_count}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[2]/span/div/div/div[1]/span").text;
        except Exception as ex:
            postShare = 0
        postUrl=""
        try:
            # img basic
            postUrl = container[0].find_element(By.XPATH,f".//div[{_count}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div[1]/a/div[1]/div/div/div/img").get_attribute("src");
        except Exception as e1:
            try:
                # block img
                divImages = container[0].find_element(By.XPATH,f".//div[{_count}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div[1]/div/div/div");
                img_elements = divImages.find_elements(By.TAG_NAME, 'img');
                img_urls = [img.get_attribute('src') for img in img_elements]
                postUrl = " | ".join(img_urls);
            except Exception as e2:
                try:
                    # video
                    postUrl=container[0].find_element(By.XPATH,f".//div[{_count}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div/div/div/video").get_attribute("src");
                except Exception as e3:
                    pass
        finally:
            data_post.loc[len(data_post)]=[postTitle,postTime,postLike,postShare,postUrl]
        # time.sleep(1);
        
    # for link in list_link:
    #     driver.get(link);
    #     time.sleep(2);
    #     btnClose1 = driver.find_elements(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div');
    #     btnClose1[0].click();
    #     _time = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span/a/span").text
    #     _image = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div[1]/a/div[1]/div/div/div/img").get_attribute("src")
    #     eleTitle=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div/div");
    #     title = eleTitle.get_attribute("outerHTML");
        
    #     data_post.loc[len(data_post)]=[title,_time,_image]
    
    data_post.to_csv("data_post.csv");
    
    time.sleep(10);

finally:
    driver.quit()
    
data_post