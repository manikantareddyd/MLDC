from doc2vec import *
from sklearn.decomposition import RandomizedPCA
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
d=docVector(wordVecGen,topics_list,Test,test_list,50)

#Empty lists
X_train=[]
y_train=[]

for x in d.topicVectorsTrain:
    X_train.append(d.topicVectorsTrain[x])
    y_train.append(x)

y_train = [('_').join(i.split('_')[:-1]) for i in y_train]

X_train_pca = X_train
#NearestNeighbors finder
neigh = NearestNeighbors(5,p=2)
neigh.fit(X_train_pca,y_train)

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
X_pca = X
#gives distance and indices in X_train, y_train of 5 NearestNeighbors of every element in X
dist, ind = neigh.kneighbors(X_pca,n_neighbors=5,return_distance=True)
y = [('_').join(i.split('_')[:-2]) for i in y]
print y
table = PrettyTable(['Topic','N1','N2','N3','N4','score'])
for i in range(len(X_pca)):
    score = 0
    for j in range(0,4):
        if y[int(i)].lower() == y_train[ind[i][j]].lower() :
            score += (1/(1.0*dist[i][j]))*(4-j)
    score = score/(sum([(4-j)/(1.0*dist[i][j]) for j in range(0,4)]))
    table.add_row( [ y[int(i)] , y_train[ind[i][1]] , y_train[ind[i][2]] , y_train[ind[i][3]] , y_train[ind[i][4]], score ])

print table
