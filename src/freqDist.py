import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import FrenchStemmer


topics_en = ['Physics','Chemistry','Politics']
corpus_en = {}
words_en  = []
stop_en = stopwords.words('english')
stop_en = [unicode(i) for i in stop_en ]
st_en = LancasterStemmer()
freqDist_en={}
for topic in topics_en:
    f=open('files/'+topic+'.txt','r')
    content=f.read()
    f.close()
    print "Loaded",topic
    corpus_en[topic] = [(st_en.stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content)) if unicode(i) not in stop_en]
    freqDist_en[topic]={x:corpus_en[topic].count(x)/(0.001*len(corpus_en[topic])) for x in corpus_en[topic] if corpus_en[topic].count(x) > 10}# and corpus_en[topic].count(x) < 20}
    words_en += freqDist_en[topic].keys()
words_en = list(set(words_en))

topics_fr = ['Physique','chimie','Politique']
corpus_fr = {}
words_fr  = []
stop_fr = stopwords.words('french')
stop_fr = [unicode(i) for i in stop_fr ]
st_fr = FrenchStemmer()
freqDist_fr={}
for topic in topics_fr:
    f=open('files/'+topic+'.txt','r')
    content=f.read()#content.encode('utf8'))
    f.close()
    print "Loaded",topic
    corpus_fr[topic] = [(st_fr.stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content)) if unicode(i) not in stop_fr]
    freqDist_fr[topic]={x:corpus_fr[topic].count(x)/(0.001 * len(corpus_fr[topic])) for x in corpus_fr[topic] if corpus_fr[topic].count(x) > 10}
    words_fr += freqDist_fr[topic].keys()
words_fr = list(set(words_fr))

print "Generating vectors for english words"
words_en_vectors = {}
for word in words_en:
    vec=[]
    for topic in topics_en:
        # if word==unicode('sci'):
        #     print word,topic
        # print word
        try:
            vec.append(freqDist_en[topic][unicode(word)])
        except:
            vec.append(0)
    words_en_vectors[word]=vec

print "Generating vectors for french words"
words_fr_vectors = {}
for word in words_fr:
    vec=[]
    for topic in topics_fr:
        try:
            vec.append(freqDist_fr[topic][word])
        except:
            vec.append(0)
    words_fr_vectors[word]=vec

w=words_en_vectors.values()+words_fr_vectors.values()
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
fig = plt.figure()
ay = fig.add_subplot(111, projection='3d')
ay.scatter(zip(*w)[0],zip(*w)[1],zip(*w)[2])
fig.show()
