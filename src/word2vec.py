import wikipedia
import gensim
import re
import numpy as np
from sklearn.cluster import KMeans
k=10
topics = ['President','India','Dhoni']
corpus = {}
for topic in topics:
	page	= wikipedia.page(topic)
	content = page.content.lower()
	f=open(topic+'.txt','w')
	f.write(content.encode('utf8'))
	f.close()
	print "Loaded",topic
	rx	  = re.compile('\W+')
	content = rx.sub(' ',content).strip().split()
	corpus[topic]=content


print "created corpus"
model   = gensim.models.Word2Vec(corpus.values(),min_count=0)
print "Word Vectors created, vocab size:",len(model.vocab)
vectors=[]

for word in model.vocab.keys():
	vectors.append(model[word])

KMModel = KMeans(n_clusters = k)
KMModel.fit(vectors)
print "KMM done"
centers = KMModel.cluster_centers_
topicvec = {}
for topic in topics:
	vec = [0 for  i in range(k)]
	content = corpus[topic]
	labels = KMModel.predict(model[content])
	labels = np.array(labels)
	for label in labels:
		vec[label]+=1
	topicvec[topic]=vec
	print topic,vec
