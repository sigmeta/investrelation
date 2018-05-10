#获取投资机构的投资项目
import requests
import json
import time

def getinfo(i):#爬取36kr api
    print(i)
    try:
        res=requests.get("https://rong.36kr.com/n/api/org/"+str(i)+"/investment")
    except:
        return False
    dic = json.loads(res.text)
    if dic['code']==1:
        print('该序号无对应信息')
        return True
    pagenum=dic["data"]["investments"]['totalPages']
    projects={}
    projects["org"]=dic["data"]["org"]
    projects["investments"]=dic["data"]["investments"]['data']
    for j in range(2,pagenum+1):
        res=requests.get("https://rong.36kr.com/n/api/org/"+str(i)+"/investment"+"?page="+str(j))
        dic = json.loads(res.text)
        projects["investments"]+=dic["data"]["investments"]['data']
    with open('data/projects/'+str(i)+'.json','w',encoding='utf8') as f:
        f.write(json.dumps(projects,ensure_ascii=False))
        print('写入成功')
    return True

if __name__=='__main__':
    n=0
    while n<53000:
        if getinfo(n):
            n+=1
        else:
            print('爬取太快，暂停一会儿')
            time.sleep(100)

