from WordToVec import *
from sklearn.cluster import KMeans
import math
import numpy as np
from scipy.spatial.distance import *
from sklearn.neighbors import NearestNeighbors
# from multithreading.Threading import threading.Thread
class docVector:
    def __init__(self,wordVecGen, topics_list,Test,test_list,k):
        self.wv = wordVecGen # Generator for Word Vectors
        self.Test = Test
        for j in self.wv.languages:
            self.wv.topics[j]=[topic+'_'+j for topic in topics_list]
        self.Model = KMeans(k)
        self.Model.fit(self.wv.word_vectors_all.values())
        self.languages = self.wv.languages
        self.topicVectors={}
        self.topicVectorsTrain={}
        threads = {}

        for j in self.languages:
            threads[j+'Train']=threading.Thread(target=self.genTrain, args=(k,j,))
            threads[j+'Train'].start()
        for j in self.languages:
            threads[j+'Train'].join()
        print "\nTraining Set Done\n"

        if test_list != None :
            for j in self.languages:
                threads[j+'Test']=threading.Thread( target=self.genTest, args=(k,j,))
                threads[j+'Test'].start()
                # self.gen(k,j)
            for j in self.languages:
                threads[j+'Test'].join()
            print "All docs vectorized"

    def genTrain(self,k,j):
        threadTopic = {}
        for topic in self.wv.topics[j]:
            threadTopic[topic] = threading.Thread(target = self.vectorGenTrain, args = (topic,k,j))
            threadTopic[topic].start()

        for topic in self.wv.topics[j]:
            threadTopic[topic].join()
            print "Loaded", topic

    def vectorGenTrain(self,topic,k,j):
        vector = [0 for x in range(k)]
        for word in self.wv.corpus[j][topic]:
            vector[self.Model.predict([self.wv.word_vectors[j][word]])[0]]+=1.0*self.wv.freqDist[j][topic][word]
        vector = [math.exp((1+vector[x])/(1.0+1.0*max(vector))) for x in range(k)]
        self.topicVectorsTrain[topic]=np.array(vector)

    def genTest(self,k,j):
        threadTopic = {}
        for topic in self.Test.test_topics[j]:
            # self.vectorGen(topic,k,j)
            threadTopic[topic] =  threading.Thread(target = self.vectorGenTest, args = (topic,k,j,))
            threadTopic[topic].start()

        for topic in self.Test.test_topics[j]:
            threadTopic[topic].join()
            print "Loaded", topic

    def vectorGenTest(self,topic,k,j):
        vector = [0 for x in range(k)]
        for word in self.Test.corpus[j][topic]:
            vector[self.Model.predict([self.Test.word_vectors[j][word]])[0]]+=1.0*self.Test.freqDist[j][topic][word]
        vector = [math.exp((1+vector[x])/(1.0+1.0*max(vector))) for x in range(k)]
        self.topicVectors[topic]=np.array(vector)
