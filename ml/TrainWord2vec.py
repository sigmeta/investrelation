#训练word2vec
from gensim.models import word2vec
#from gensim.Word2Vec import LineSentence
sentences=word2vec.Text8Corpus('jingyingfanwei.txt')
model=word2vec.Word2Vec(sentences, size=200)
model.save('model/model')