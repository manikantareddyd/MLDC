from WordToVec import *
from sklearn.cluster import KMeans
import math
import numpy as np
from hmmlearn import hmm
class docTimeSeries:
    def __init__(self,  k):
        self.wordVecGen = wordVecGen()
        self.Model      = KMeans(k)
        self.Model.fit(self.wordVecGen.word_vectors.values())
        self.hmmModels = {}
        self.topicSeries = {}
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

            # This Part now stems every word in the document loaded and copies it into corpus_en.
            words_in_topic  = [(st_en.stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content)) if unicode(i) not in stop_en]

            docSeries = []
            for word in words_in_topic:
                try:
                    docSeries.append([self.Model.predict([self.wordVecGen.word_vectors[word]])[0]])
                except:
                    pass
            self.hmmModels[topic] = self.getModel(docSeries)
            self.topicSeries[topic] = docSeries

        #This part is french
        print "Working on French"
        stop_fr = stopwords.words('french')
        stop_fr = [unicode(i) for i in stop_fr ]
        st_fr = FrenchStemmer()
        freqDist_fr={}
        for topic in self.wordVecGen.topics_fr:
            # Just the Laborious File Loading tasks
            f=open('files/'+topic+'.txt','r')
            content=f.read()#content.encode('utf8'))
            f.close()
            print "Loaded",topic

            # This Part now stems every word in the document loaded and copies it.
            words_in_topic = [(st_fr.stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content)) if unicode(i) not in stop_fr]

            docSeries = []
            for word in words_in_topic:
                try:
                    docSeries.append([self.Model.predict([self.wordVecGen.word_vectors[word]])[0]])
                except:
                    pass
            self.hmmModels[topic] = self.getModel(docSeries)
            self.topicSeries[topic] = docSeries
    def getModel(self,series):
        model = hmm.GaussianHMM(n_components=3, covariance_type="full")
        model.fit(series)
        return model
