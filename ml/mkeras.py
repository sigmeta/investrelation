import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation  
from keras.optimizers import RMSprop,SGD  
import numpy as np

ar=np.load('data/rel.npy')
np.random.shuffle(ar)
ar[:,124]=0;ar[:,449]=0
m=int(ar.shape[0]*0.7)
traindata=np.array(ar[:m,:-1],dtype=np.float32)
trainlabel=ar[:m,-1:]
testdata=ar[m:,:-1]
testlabel=ar[m:,-1:]

trainlabel= keras.utils.to_categorical(trainlabel,2)
testlabel= keras.utils.to_categorical(testlabel,2) 

model = Sequential()
model.add(Dense(500,input_dim=650)) # 输入层
model.add(Activation('relu')) # 激活函数是relu
model.add(Dropout(0.5)) # 采用50%的dropout

model.add(Dense(300,input_dim=650)) # 输入层
model.add(Activation('relu')) # 激活函数是relu
model.add(Dropout(0.5)) # 采用50%的dropout

model.add(Dense(30)) # 隐藏层节点500个  
model.add(Activation('relu'))  
model.add(Dropout(0.5))

model.add(Dense(2)) # 输出结果是10个类别，所以维度是10  
model.add(Activation('softmax')) # 最后一层用softmax作为激活函数

model.summary() #打印出模型概况
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True) # 优化函数，设定学习率（lr）等参数  
model.compile(loss='categorical_crossentropy', optimizer=sgd) # 使用交叉熵作为loss函数

model.fit(traindata,trainlabel,batch_size=1000,epochs=10,validation_data=(testdata,testlabel),shuffle=True,verbose=1)

tr=model.predict(traindata).argmax(axis=1)
te=trainlabel.argmax(axis=1)
print("训练准确率",(1-np.abs(tr-te)).sum()/len(tr))

tr=model.predict(testdata).argmax(axis=1)
te=testlabel.argmax(axis=1)
print("测试准确率",(1-np.abs(tr-te)).sum()/len(tr))

