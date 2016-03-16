from freqDist import *
from sklearn.cluster import KMeans
import math
import numpy as np
class docVector:
    def __init__(self,k):
        self.gen(k)
    def gen(self,k):
        wv = vectorGen() # Generator Word Vectors
        wv.gen()
        Model = KMeans(k) #
        Model.fit(wv.words_vectors.values())
        topics_en = ['India','Adele','Pakistan_en','Baboon']
        topics_fr = ['Inde','Adele_fr','Pakistan_fr','Babouin']
        self.topicVectors={}
        for topic in topics_en:
            vector = [0 for x in range(k)]
            for word in wv.corpus_en[topic]:
                vector[Model.predict([wv.words_vectors[word]])[0]]+=1
            vector = [math.exp((1+vector[x])/(1.0+1.0*max(vector))) for x in range(k)]
            self.topicVectors[topic]=np.array(vector)
        for topic in topics_fr:
            vector = [0 for x in range(k)]
            for word in wv.corpus_fr[topic]:
                vector[Model.predict([wv.words_vectors[word]])[0]]+=1
            vector = [math.exp((1+vector[x])/(1.0+1.0*max(vector))) for x in range(k)]
            self.topicVectors[topic]=np.array(vector)

d=docVector(20)
n = np.linalg.norm
v=d.topicVectors
topics_en = ['India','Adele','Pakistan_en','Baboon']
topics_fr = ['Inde','Adele_fr','Pakistan_fr','Babouin']
# for topic in topics_en:
#     for t in topics_fr:
#         print t,topic,n(v[t]-v[topic],1)
#
f=open('res2.txt','w')
for topic in topics_en+topics_fr:
    for t in topics_en+topics_fr:
        f.write(str(t)+','+str(topic)+','+str(n(v[t]-v[topic],1))+'\n')
#w=self.words_vectors.values()
