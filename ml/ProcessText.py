
import pymysql
import jieba
import re

#整理文本，分词
#连接数据库
conn = pymysql.connect('localhost','root','9432','companyb',charset='utf8')
cursor=conn.cursor()

#选取所有企业经营范围文本
cursor.execute("select 经营范围 from company")
fw=cursor.fetchall()

stopwords=['、',',','.','，','。','；','：','〓','（','）','《','》','*','#','&','(',')',';','“','”']
f=open('jingyingfanwei.txt','w',encoding='utf8')
for i in range(len(fw)):
    print('\r'+str(i),end='')
    st=re.sub('【依法须经批准的项目，经相关部门批准后方可开展经营活动】','',fw[i][0])
    st=re.sub('(依法须经批准的项目，经相关部门批准后方可开展经营活动)','',st)
    st=re.sub('（依法须经批准的项目，经相关部门批准后方可开展经营活动）','',st)
    wlist=[]
    for w in jieba.lcut(st):
        if w not in stopwords:
            wlist.append(w)
    if len(wlist)>0:
        f.write(' '.join(wlist)+'\n')
f.close()