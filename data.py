from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
def crawling_data(enddate=date(2023,3,1),months=37):
    Columns=['日期','白天/晚上','高温','低温','AQI','风向','降水量']
    data=pd.DataFrame(columns=Columns)
    driver=webdriver.Edge()
    driver.wait=WebDriverWait(driver,10,1)
    for i in range(months):
        thedate=enddate-relativedelta(months=i)
        url='https://www.tianqi24.com/zhengzhou/history{}.html'.format(thedate.strftime('%Y%m'))
        driver.get(url)
        dt=pd.DataFrame(dict(zip(
            Columns,[[
                elm.text for elm in driver.find_elements(
                    By.XPATH,'//*[@id="main"]/section/article[2]/section/ul/li/div[{}]'.format(i+1)
                )[1:]
            ] for i in range(len(Columns))]
        )))
        dt['日期']=dt['日期'].apply(lambda x:thedate.strftime('%Y')+'-'+x)
        data=pd.concat((data,dt))
    data.reset_index(drop=True,inplace=True)
    return data
data=crawling_data()
data.to_excel('data.xlsx',index=False)