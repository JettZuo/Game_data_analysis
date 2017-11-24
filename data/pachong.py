# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:38:46 2017

@author: tanyu.mobi
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
#r.encoding = r.apparent_encoding
def GetHtmlText(url):
    try:
        ug = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url,headers = ug,timeout = 20)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
        print 'done'
    except:
        return ''
        print 'shibai'

#print a.encode('gb18030')
def parsepage(html):
    soup = BeautifulSoup(html,'html.parser')
    for i in range(len(soup.find_all('li',class_='taptap-review-item collapse in'))): 
        a = soup.find_all('li',class_='taptap-review-item collapse in')[i]
        user_id = a.find('span','taptap-user')['data-user-id']
        web = a.find('a')['href']
        sex = a.find('a')['class'][-1]
        user_name = a.find('span','taptap-user').find('a').string
        time =  a.find('a','text-header-time')('span')[0].string
        score = int(a.find('div','item-text-score').find('i')['style'][-4:-2])/14
        if a.find('div','item-text-score').find('span') is not None:
            p_time = a.find('div','item-text-score').find('span').string
            play_time = p_time[4:len(p_time)]
        else:
            play_time = ''
        comment = ''
        all_p = a.find(name = 'div',attrs={'class':'item-text-body'})('p')
        for j in range(len(all_p)):
            if all_p[j].text is not None:
                comment = comment + all_p[j].text
            else:
                comment = comment + str(all_p[j].text)
        if a.find('span','text-footer-device') is not None:
            phone = a.find('span','text-footer-device').string
        else:
            phone = ''
        huanle = a.find('ul',class_='list-unstyled text-footer-btns').find_all('span')[1].string
        dianzan = a.find('ul',class_='list-unstyled text-footer-btns').find_all('span')[2].string
        dianxia = a.find('ul',class_='list-unstyled text-footer-btns').find_all('span')[3].string
        list = []
        list.append(user_name)
        list.append(user_id)
        list.append(web)
        list.append(sex)
        list.append(time)
        list.append(play_time)
        list.append(score)
        list.append(comment)
        list.append(phone)
        list.append(huanle)
        list.append(dianzan)
        list.append(dianxia)
        all_data.append(list)

all_data = []
num = 100
for i in range(0,num):
    i = i+1
    url = 'https://www.taptap.com/app/52276/review?order=default&page=' + str(i) + '#review-list'
    html = GetHtmlText(url)
    parsepage(html)
    time.sleep(5)
data = pd.DataFrame(all_data,columns=['user_name','user_id','web','sex','time','play_time','score','comment','phone','huanle','dianzan','dianxia'])
data.to_csv('D:\\cjhwy/taptap/taptap_52776.csv',encoding='gb18030',index=False)

#时间处理，分钟小时统一转化为分钟
#不同星级词云分布
#用户情感分析
#男女性别分布、机型分析
