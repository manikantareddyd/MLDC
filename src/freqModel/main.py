from doc2vec import *
# Declarations
languages = ['en','fr','es']
topics_list = ['Adele','Baboon','Chemistry','Energy','pokemon','English_language','French_language','India','Pakistan','Politics','Tennis','The_Beatles','Wikipedia']
test_list = ['India_test','Pokemon_test']
loo = len(topics_list)
topics_list = topics_list[:loo]

# All the generation
# wordVecGen = wordVecGen(topics_list,languages,loo)
# This is load wordVecGen directly. We don't compute it again and again
import pickle


f=open('word2vec-sum-norm.pkl','rb')
wordVecGen = pickle.load(f)
# pickle.dump(wordVecGen,f,protocol=pickle.HIGHEST_PROTOCOL)
f.close()
Test = Test(wordVecGen, test_list)
d=docVector(wordVecGen,topics_list,Test,test_list,40)

#Empty lists
X_train=[]
y_train=[]

for x in d.topicVectorsTrain:
    X_train.append(d.topicVectorsTrain[x])
    y_train.append(x)

#NearestNeighbors finder
neigh = NearestNeighbors(5,p=1)
neigh.fit(X_train,y_train)

test_docs = []
for l in languages:
    for doc in test_list:
        test_docs.append(doc+'_'+l)

# Test Set
X = []
y = []
for topic in test_docs:
    X.append(d.topicVectors[topic])
    y.append(topic)

#gives distance and indices in X_train, y_train of 5 NearestNeighbors of every element in X
dist, ind = neigh.kneighbors(X,n_neighbors=5,return_distance=True)

table = PrettyTable(['Topic','N1','N2'])
for i in range(len(X)):
    table.add_row([y[int(i)],y_train[ind[i][1]],y_train[ind[i][2]]])

print table
