import wikipedia
import gensim
import re
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
k=10
topics = ['Chemistry','Physics','Kanhaiya Kumar','India','Pakistan','Naruto','pikachu','pokemon','Academy Awards','Leonardo Di Caprio']
corpus = {}
stop = stopwords.words('english')
lemmatizer=WordNetLemmatizer()
for topic in topics:
    #page    = wikipedia.page(topic)
    #content = page.content.lower()
    f=open(topic+'.txt','r')
    content=f.read()#content.encode('utf8'))
    f.close()
    print "Loaded",topic
    rx      = re.compile('\W+')
    content = rx.sub(' ',content).strip()
    corpus[topic] = [lemmatizer.lemmatize(i) for i in re.split('\W+',content) if i not in stop]

# wikipedia.set_lang('fr')
# for topic in ['Autocar','Physique','chimie']:
#     #page    = wikipedia.page(topic)
#     #content = page.content.lower()
#     f=open(topic+'.txt','r')
#     content=f.read()#content.encode('utf8'))
#     f.close()
#     print "Loaded",topic
#     rx      = re.compile('\W+')
#     content = rx.sub(' ',content).strip().split()
#     corpus[topic]=content
#
# topics=topics+['Autocar','Physique','chimie']
print "created corpus"
model   = gensim.models.Word2Vec(corpus.values(),min_count=0)
print "Word Vectors created, vocab size:",len(model.vocab)
vectors=[]
words = []
for word in model.vocab.keys():
    vectors.append(model[word])
    words.append(word)

KMModel = KMeans(n_clusters = k)
KMModel.fit(vectors)
closest, _ = pairwise_distances_argmin_min(KMModel.cluster_centers_, vectors)
for i in closest:
    print words[i]
print "KMM done"
centers = KMModel.cluster_centers_
topicvec = {}
for topic in topics:
    vec = [0 for  i in range(k)]
    content = corpus[topic]
    labels = KMModel.predict(model[content])
    labels = np.array(labels)
    for label in labels:
        vec[label]+=1#/(1.0*(len(content)))
    topicvec[topic]=np.array(vec)/np.linalg.norm(vec,2)

    print topic,topicvec[topic]

nnn = np.linalg.norm
print nnn(topicvec['Physics']-topicvec['Chemistry'])
print nnn(topicvec['Physics']-topicvec['Naruto'])
