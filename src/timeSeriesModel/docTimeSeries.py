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
        self.topicSeries = {}
    def gen(self,k):
        #This part for English
        for topic in self.wv.topics_en:
            topic_series = []
            f=open('files/'+topic+'.txt','r')
            content=f.read()
            f.close()
            print "Loaded",topic
            sentences = content.split('. ')
            self.topicSeries[topic]=np.array(topic_series)

        #This part for french
        for topic in self.wv.topics_fr:
            topic_series = []
            for word in self.wv.corpus_fr[topic]:
                topic_series.append(self.Model.predict([self.wv.word_vectors[word]])[0])
            self.topicSeries[topic]=np.array(topic_series)
