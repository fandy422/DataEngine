import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame as df
import time
def get_page_content(request_url):
    # 得到页面的内容
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(url,headers=headers,timeout=10)
    content = html.text
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup
#分析当前页面的投诉信息
def analysis(soup):
    df_data = df(columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
    #完整的投诉信息框
    temp=soup.find('div',class_='tslb_b')
    # 找出所有的tr,即行
    tr_list=temp.find_all('tr')
    for tr in tr_list:
        td_list=tr.find_all('td')
        #如果没有表头，就是表头th
        if len(td_list)>0:
            temp_list=[]
            #投诉编号,投诉品牌,投诉车系,投诉车型,问题简述,典型问题,投诉时间,投诉状态
            '''
            #老师讲的方法为使用字典添加
            id,brand,car_model,type,desc,problem,datetime,status=\
                td_list[0].text,td_list[1].text,td_list[2].text,td_list[3].text,\
                td_list[4].text,td_list[5].text,td_list[6].text,td_list[7].text
            temp={}
            temp['id']=id
            temp['brand'] = brand
            temp['car_model'] = car_model
            temp['type'] = type
            temp['desc'] = desc
            temp['problem'] = problem
            temp['datetime'] = datetime
            temp['status'] = status
            df_data=df_data.append(temp,ignore_index=True)
           '''
            # print(id,brand,car_model,type,desc,problem,datetime,status)
            #此处使用list循环添加,相对简洁一些
            for i in range(8):
                temp_list.append(td_list[i].text)
            df_data.loc[len(df_data)] = temp_list
    return df_data
#开始计时
time1=time.time()
result_df=df(columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
# 请求URL
base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-'
#设定网页遍历的页码数
page_num=20
for i in range(page_num):
    #拼接页面url
    url=base_url+str(i+1)+'.shtml'
    #soup解析
    soup=get_page_content(url)
    #通过解析，得到当前页面dataframe
    df_data=analysis(soup)
    result_df=result_df.append(df_data)
result_df.to_excel("car_complain_20210209.xlsx",index=False)
result_df.to_csv("car_complain_20210209.csv",index=False)
print("共用时%s秒."%(time.time()-time1))
