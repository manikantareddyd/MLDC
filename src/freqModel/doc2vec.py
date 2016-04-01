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
        # print "Size of Vocabulary: "+str(len(self.wv.word_vectors_all))
        self.languages = ['en','fr']
        self.gen(k)

    def gen(self,k):

        topics_test = {}
        self.topicVectors={}
        for j in self.languages:

            topics_test[j] = self.Test.test_topics[j]

            #This part for English
            print "Vectorizing English docs"
            for topic in topics_test[j]:
                vector = [0 for x in range(k)]
                print "Generating vector for ",topic
                for word in self.Test.corpus[j][topic]:
                    vector[self.Model.predict([self.Test.word_vectors[j][word]])[0]]+=1
                vector = [math.exp((1+vector[x])/(1.0+1.0*max(vector))) for x in range(k)]
                self.topicVectors[topic]=np.array(vector)


        print "All docs vectorized"

topics_list = ['Adele','Baboon','Chemistry','pokemon','Energy','English_language','French_language','India','Pakistan','Politics','Tennis','The_Beatles','Wikipedia']
wordVecGen = wordVecGen(topics_list,len(topics_list))
test_list = ['pokemon','Energy','India']
d=docVector(wordVecGen,test_list,40)
n = np.linalg.norm
v=d.topicVectors
table=PrettyTable(['en','fr','Cosine','norm1','norm2'])
for topic in d.Test.test_topics['en']:
    for t in d.Test.test_topics['fr']:
        #print t,topic,1,n(v[t]-v[topic],2)
        # print t,topic,2,n(v[t]-v[topic],2)
        # print t,topic,"cosine\n",cosine(v[t],v[topic])
        table.add_row([topic,t,cosine(v[t],v[topic]),n(v[t]-v[topic],1),n(v[t]-v[topic],2)])
print table
# f=open('res2.txt','w')
# for topic in topics_en+topics_fr:
#     for t in topics_en+topics_fr:
#         f.write(str(t)+','+str(topic)+','+str(n(v[t]-v[topic],1))+'\n')
#w=self.word_vectors.values()
