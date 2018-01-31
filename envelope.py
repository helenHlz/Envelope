#python3.6颜文字抓取

import urllib.request
import re
import csv
import sqlite3

TheHeader = {
    'Connection': 'Keep-Alive',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,\
zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0)\
Gecko/20100101 Firefox/57.0',
    'Host': 'www.yanwenzi.com',
    'DNT': '1'
    }

def GetOnePageResult(TheUrl):
    req = urllib.request.Request(url = TheUrl, headers = TheHeader)
    ThePage = urllib.request.urlopen(req)
    data = ThePage.read().decode('UTF-8')
    Emoticons = re.compile('<li>\s*<p>(.+)</p>\s*<div>(.*)</div>')    
    result = re.findall(Emoticons,data)
    return result

def GetPageUrlList(TheUrl):
    req = urllib.request.Request(url = TheUrl, headers = TheHeader)
    ThePage = urllib.request.urlopen(req)
    data = ThePage.read().decode('UTF-8')
    OtherPage = re.compile( '<a href="(.*?)">\d</a>')
    result = re.findall(OtherPage,data)
    return result

def GetTypeList(TheUrl):
    req = urllib.request.Request(url=TheUrl, headers=TheHeader)
    ThePage = urllib.request.urlopen(req)
    data = ThePage.read().decode('UTF-8')
    Type = re.compile( '<li><a href="(/.+?/)"(?: class="active)?>([\u4e00-\u9fa5]*)</a></li>')
    result = re.findall(Type,data)
    return result
        
if __name__ =='__main__':
    
    MainUrl='http://www.yanwenzi.com'
    count = 0  ;list1 = [];   list2 = [];
    TypeList = GetTypeList(MainUrl)
    for item in TypeList:
        TypeUrl = MainUrl+item[0]
        PageList = GetPageUrlList(TypeUrl)
        PageList.insert(0,'')        
        for item in PageList:
            PageResult = GetOnePageResult(TypeUrl+item)
            count += len(PageResult)
            list1 += PageResult
    
    with open('envelop.csv','w',encoding='UTF-8') as file:
        file_csv = csv.writer(file)
        file_csv.writerow(['Emoticons','Directions'])
        file_csv.writerows(list1)
        list2=[i for i in range(count)]
        zipped = list(zip(list2,list(zip(*list1))[0],list(zip(*list1))[1]))
        consql = sqlite3.connect('envelope2.db')
        cursql = consql.cursor()
        cursql.execute('CREATE TABLE atable(id integrate,emoticons varchar(50),directions varchar(20))')
        cursql.executemany('INSERT INTO atable VALUES(?,?,?)',zipped)
        consql.commit()
        consql.close()
    print(count)
