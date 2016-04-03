from WordToVec import *
from sklearn.cluster import KMeans
import math
import numpy as np
from scipy.spatial.distance import *
from sklearn.neighbors import NearestNeighbors
from multiprocessing import Process
class docVector:
    def __init__(self,wordVecGen, Test,test_list,k):
        self.wv = wordVecGen # Generator for Word Vectors
        self.Test = Test
        self.Model = KMeans(k)
        self.Model.fit(self.wv.word_vectors_all.values())
        self.languages = self.wv.languages
        self.topicVectors={}
        self.topicVectorsTrain={}
        threads = {}
        for j in self.languages:
            threads[j+'Train']=Process(target=self.genTrain, args=(k,j,))
            threads[j+'Train'].start()
        for j in self.languages:
            threads[j+'Train'].join()
        print "\nTraining Set Done\n"
        if test_list != None :
            for j in self.languages:
                threads[j+'Test']=Process( target=self.genTest, args=(k,j,))
                threads[j+'Test'].start()
                # self.gen(k,j)
            for j in self.languages:
                threads[j+'Test'].join()
            print "All docs vectorized"

    def genTrain(self,k,j):
        threadTopic = {}
        for topic in self.wv.topics[j]:
            threadTopic[topic] = Process(target = self.vectorGenTrain, args = (topic,k,j))
            threadTopic[topic].start()
            print "Process Id: "

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
            threadTopic[topic] =  Process(target = self.vectorGenTest, args = (topic,k,j,))
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
wordVecGen = wordVecGen(topics_list,languages,len(topics_list))
test_list = None# ['pokemon','Energy','Tennis']

Test = Test(wordVecGen, test_list)
d=docVector(wordVecGen,Test,test_list,40)
n = np.linalg.norm
v=d.topicVectors
# table=PrettyTable(['Topic1','Topic2','Cosine','norm1','norm2'])
# for t in [t for t in test_docs]:
#     for topic in [t for t in test_docs]:
#         table.add_row([topic,t,cosine(v[t],v[topic]),n(v[t]-v[topic],1),n(v[t]-v[topic],2)])
X = []
y = []
test_list = topics_list
test_docs = []
for l in languages:
    for doc in test_list:
        test_docs.append(doc+'_'+l)
for topic in test_docs:
    X.append(v[topic])
    y.append(topic)
neigh = NearestNeighbors(5,p=1)
neigh.fit(X,y)
dist, ind = neigh.kneighbors(X,n_neighbors=5,return_distance=True)
tabel = PrettyTable(['Topic','N1','N2'])
for i in range(len(X)):
    nind = ind[i]
    tabel.add_row([y[i],y[nind[1]],y[nind[2]]])

print tabel

# for topic in d.Test.test_topics['en']:
#         table.add_row([topic,t,cosine(v[t],v[topic]),n(v[t]-v[topic],1),n(v[t]-v[topic],2)])
