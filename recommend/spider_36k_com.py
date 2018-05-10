#爬取所有创业项目的详细信息
import requests
import json
import time
import random
from recommend.spider_36k_comlist import get_cookies

def get_info(cid,cookies):
    dic={}
    contents=['','/finance','/member','/product','/funds']
    keys=['company','finance','member','product','funds']
    def get_page(con):
        company=json.loads(requests.get('https://rong.36kr.com/n/api/company/'+str(cid)+con, cookies=cookies).text)
        if company['code']==0:
            return company['data']
        else:
            raise Exception(company['msg'])
    for i in range(len(contents)):
        dic[keys[i]]=get_page(contents[i])
    return dic

if __name__=='__main__':
    #整理出所有的cid
    with open("data/comlist.json",encoding='utf8') as f:
        comlist=json.loads(f.read())
    print(len(comlist))
    cookies=get_cookies()
    cominfos={}
    n=0
    while n<len(comlist):
        try:
            infonow=get_info(comlist[n],cookies)
        except Exception as e:
            print(e)
            time.sleep(100)
        else:
            cominfos[comlist[n]]=infonow
            n+=1
            time.sleep(random.uniform(0,2))
    # 保存
    print('爬取完成')
    with open('data/cominfos.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(cominfos, ensure_ascii=False))
    print('保存完成')