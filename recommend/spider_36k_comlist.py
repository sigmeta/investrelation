#获得所有创业项目的列表，并保存基础信息
import requests
import json
import time
import random

def get_cookies():
    cookie="MEIQIA_EXTRA_TRACK_ID=0vLskrXjYhcSdi2BElXfzdTMzNc; acw_tc=AQAAAG3pw0dEdwgAhu9pov3SvdqMnSlp; kr_stat_uuid=QhfXK25432517;" \
        " Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3=1525950867,1525950968; Hm_lpvt_e8ec47088ed7458ec32cde3617b23ee3=1525951039; " \
        "download_animation=1; _kr_p_se=aed02698-eca5-4073-ba79-029a309a20dc; krid_user_id=633917108; krid_user_version=4; " \
        "kr_plus_id=633917108; kr_plus_token=1xZ3_1oXfuJhf9Tbth9wBlJZqKlMVQ9b246_2___; kr_plus_utype=0; " \
        "Z-XSRF-TOKEN=eyJpdiI6IjlNXC83Y1h0bUhwXC9Ub1dPT0FadG9QUT09IiwidmFsdWUiOiJcLzhcLys0c2xpUDRQdlVURDVVUjVPWUNlbG9WbTk0T" \
        "lpzcWNUSVwvc3ZYS1dzTk5HbkFZUmdvMnBjZ0lRXC9FeWlKRHFtczZ1MUhyeitQb1pqQVlrK0NOYXc9PSIsIm1hYyI6IjAxODI0YjBlZjc1YzNjMmMw" \
        "MzYwODhlY2QwODk1NjE1NjM2NWFjNDRjZmUxYThiYjQ2ZGZhOTUyNTkzNWY4ZTUifQ%3D%3D;" \
        " krchoasss=eyJpdiI6IlVkZVJtNzdhenJJOU02V0ZEVEZXbnc9PSIsInZhbHVlIjoiVTV1c0Z2eTRQWFBNK3FVSnA1YlpGSVV3R0tiYVo0OVdZc2pye" \
        "UZ4QWMzRG00WFwvYjFcL2gwZk5wNWpOV0ErdnRGbkdrc2p2TDVmTWIyUGx4cXdwZ2ttUT09IiwibWFjIjoiY2FmMDAwMjNkNmFjNTZhZWFmZDVmYWM3MD" \
        "M2Yzg5YTFjMDI3MzNjZWVhZjAxZDAwZWZlOThhNTIxMDRlZWE0NyJ9"
    cookies={}
    for c in cookie.split(';'):
        k,v=c.split('=',1)
        cookies[k]=v
    return cookies

def get_info(page,cookies):
    print(page)
    res = requests.get('https://rong.36kr.com/n/api/column/0/company?p='+str(page), cookies=cookies)
    return json.loads(res.text)['data']['pageData']['data']

if __name__=='__main__':
    cookies=get_cookies()
    res = requests.get('https://rong.36kr.com/n/api/column/0/company', cookies=cookies)
    page_num=json.loads(res.text)['data']['pageData']['totalPages']
    print(page_num)
    cominfolist=[]

    p=1
    while p<page_num+1:
        try:
            nowlist=get_info(p,cookies)
        except Exception as e:
            print(e)
            print('爬取出错，暂停一下')
            time.sleep(100)
        else:
            cominfolist+=nowlist
            p+=1
            time.sleep(random.uniform(0,2))

    #保存
    print('爬取完成')
    with open('data/cominfolist.json','w',encoding='utf8') as f:
        f.write(json.dumps(cominfolist,ensure_ascii=False))
    print('保存完成')
    comlist=[c['id'] for c in cominfolist]
    with open('data/comlist.json','w',encoding='utf8') as f:
        f.write(json.dumps(sorted(comlist),ensure_ascii=False))

