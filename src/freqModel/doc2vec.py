from WordToVec import *
from sklearn.cluster import KMeans
import math
import numpy as np
class docVector:
    def __init__(self,k):
        self.wv = wordVecGen() # Generator for Word Vectors
        self.Model = KMeans(k)
        self.Model.fit(self.wv.word_vectors.values())
        self.gen(k)

    def gen(self,k):
        topics_en_test = self.wv.topics_en_test
        topics_fr_test = self.wv.topics_fr_test
        self.topicVectors={}

        #This part for English
        for topic in topics_en_test:
            vector = [0 for x in range(k)]
            for word in self.wv.corpus_en[topic]:
                vector[self.Model.predict([self.wv.word_vectors[word]])[0]]+=1
            vector = [math.exp((1+vector[x])/(1.0+1.0*max(vector))) for x in range(k)]
            self.topicVectors[topic]=np.array(vector)

        #This part for French
        for topic in topics_fr_test:
            vector = [0 for x in range(k)]
            for word in self.wv.corpus_fr[topic]:
                vector[self.Model.predict([self.wv.word_vectors[word]])[0]]+=1
            vector = [math.exp((1+vector[x])/(1.0+1.0*max(vector))) for x in range(k)]
            self.topicVectors[topic]=np.array(vector)

d=docVector(20)
n = np.linalg.norm
v=d.topicVectors
for topic in d.wv.topics_en_test:
    for t in d.wv.topics_fr_test:
        print t,topic,n(v[t]-v[topic],1)
#
# f=open('res2.txt','w')
# for topic in topics_en+topics_fr:
#     for t in topics_en+topics_fr:
#         f.write(str(t)+','+str(topic)+','+str(n(v[t]-v[topic],1))+'\n')
#w=self.word_vectors.values()
