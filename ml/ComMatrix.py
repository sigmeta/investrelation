from gensim.models import Word2Vec
import pymysql
import jieba
import re
import numpy as np
import json

def get_cominfo():
    #连接数据库
    conn = pymysql.connect('localhost','root','9432','companyb',charset='utf8')
    cursor=conn.cursor()

    #选取所有企业经营范围文本
    cursor.execute("select * from pre_com")
    com=cursor.fetchall()
    return com

def get_array(tup,model):
    #省份30，行业93，注册时间1，注册资本1，经营范围200
    #stopwords = ['、', ',', '.', '，', '。', '；', '：', '〓', '（', '）', '《', '》', '*', '#', '&', '(', ')', ';', '“', '”']
    arr=np.zeros((325))
    if tup[2]!=None:
        arr[tup[2]-1]=1.0
    if tup[4]!=None:
        arr[tup[4]-1+30]=1.0
    if tup[6]!=None:
        arr[123]=tup[6]/30
        if arr[123]>1:
            arr[123]=1.0
    if tup[7]!=None:
        cap=0
        if re.search('\d+',tup[7]):
            cap=re.search('\d+',tup[7]).group()
        if re.search('美|欧',tup[7]):
            cap*=7
        arr[124]=cap
    if tup[8] != None:
        count=0
        st = re.sub('【依法须经批准的项目，经相关部门批准后方可开展经营活动】', '', tup[8])
        st = re.sub('(依法须经批准的项目，经相关部门批准后方可开展经营活动)', '', st)
        st = re.sub('（依法须经批准的项目，经相关部门批准后方可开展经营活动）', '', st)
        arrn=np.zeros((200))
        for w in jieba.cut(st):
            try:
                arrn+=model[w]
            except:
                pass
            else:
                count+=1
        if count>0:
            arr[125:]=arrn/count
    return arr

if __name__=='__main__':
    dic={}
    model=Word2Vec.load('model/model')

    print('模型加载完成')
    cominfo=get_cominfo()
    ar=np.zeros((len(cominfo),325))
    print('数据库读取完成') 
    for i,item in enumerate(cominfo):
        dic[item[0]]=i
    json.dump(dic,open('data/comnum.json','w'))
    print('企业序号完成')
    for i,item in enumerate(cominfo):
    	print(i)
    	ar[i]=get_array(item,model)
    np.save('data/commatrix',ar)
    print('完成')