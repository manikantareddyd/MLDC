from WordToVec import *
from sklearn.cluster import KMeans
import math
import numpy as np
from scipy.spatial.distance import *

class docVector:
    def __init__(self,wordVecGen, test_list,k):
        self.wv = wordVecGen # Generator for Word Vectors
        self.Test = Test(wordVecGen, test_list)
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
            vector[self.Model.predict([self.wv.word_vectors[j][word]])[0]]+=1
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
            vector[self.Model.predict([self.Test.word_vectors[j][word]])[0]]+=1
        vector = [math.exp((1+vector[x])/(1.0+1.0*max(vector))) for x in range(k)]
        self.topicVectors[topic]=np.array(vector)


languages = ['en','fr','es']
topics_list = ['Adele','Baboon','Chemistry','Energy','pokemon','English_language','French_language','India','Pakistan','Politics','Tennis','The_Beatles','Wikipedia']
wordVecGen = wordVecGen(topics_list,languages,len(topics_list)/3)
test_list = ['pokemon','Energy','Tennis']
d=docVector(wordVecGen,test_list,40)
n = np.linalg.norm
v=d.topicVectors
table=PrettyTable(['Topic1','Topic2','Cosine','norm1','norm2'])
for t in [t for t in test_list]:
    for topic in [t for t in test_list]:
        table.add_row([topic,t,cosine(v[t],v[topic]),n(v[t]-v[topic],1),n(v[t]-v[topic],2)])
# for topic in d.Test.test_topics['en']:
#         table.add_row([topic,t,cosine(v[t],v[topic]),n(v[t]-v[topic],1),n(v[t]-v[topic],2)])
print table
