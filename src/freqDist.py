import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import FrenchStemmer


topics_en = ['Physics','Chemistry']
corpus_en = {}
stop_en = stopwords.words('english')
stop_en = [unicode(i) for i in stop_en ]
st_en = LancasterStemmer()
freqDist_en={}
for topic in topics_en:
    f=open(topic+'.txt','r')
    content=f.read()
    f.close()
    print "Loaded",topic
    corpus_en[topic] = [(st_en.stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content)) if unicode(i) not in stop_en]
    freqDist_en[topic]={x:corpus_en[topic].count(x)/(0.001*len(corpus_en[topic])) for x in corpus_en[topic] if corpus_en[topic].count(x) > 1}# and corpus_en[topic].count(x) < 20}
#/(1.0*len(corpus_en[topic]))

topics_fr = ['Physique','chimie']
corpus_fr = {}
stop_fr = stopwords.words('french')
stop_fr = [unicode(i) for i in stop_fr ]
st_fr = FrenchStemmer()
freqDist_fr={}
for topic in topics_fr:
    f=open(topic+'.txt','r')
    content=f.read()#content.encode('utf8'))
    f.close()
    print "Loaded",topic
    corpus_fr[topic] = [(st_fr.stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content)) if unicode(i) not in stop_fr]
    freqDist_fr[topic]={x:corpus_fr[topic].count(x)/(0.001 * len(corpus_fr[topic])) for x in corpus_fr[topic] if corpus_fr[topic].count(x) > 1}# and corpus_fr[topic].count(x) < 20}
