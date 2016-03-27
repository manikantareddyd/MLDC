from WordToVec import *
from sklearn.cluster import KMeans
import math
import numpy as np
class docTimeSeries:
    def __init__(self, wordVecGen, k):
        self.wordVecGen = wordVecGen
        self.Model      = KMeans(k)
        self.Model.fit(self.wordVecGen.word_vectors.values())
        self.genSeries()

    def genSeries(self):

        #This part for english
        print "Working on English"
        stop_en = stopwords.words('english')
        stop_en = [unicode(i) for i in stop_en ]
        st_en = LancasterStemmer()
        for topic in self.wordVecGen.topics_en:
            f = open('files/'+topic+'.txt','r')
            content = f.read()
            f.close()
            print "Loaded",topic
            
