import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import FrenchStemmer
import math
class vectorGen:
    def gen(self):
        topics_en = ['Physics','Chemistry','Politics','Adele','Pakistan_en','India','Baboon']#,'Leonardo Di Caprio','Academy Awards','India','Naruto','Pakistan','pikachu','pokemon']
        self.corpus_en = {}
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
            self.corpus_en[topic]  = [(st_en.stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content)) if unicode(i) not in stop_en]
            freqDist_en[topic]={x:self.corpus_en[topic].count(x) for x in self.corpus_en[topic] if self.corpus_en[topic].count(x) > 1}# and self.corpus_en[topic].count(x) < 20}
            maxval = max(freqDist_en[topic].values())
            freqDist_en[topic]={x:math.exp(freqDist_en[topic][x]/(1.0+1.0*maxval)) for x in freqDist_en[topic].keys()}
            words_en += freqDist_en[topic].keys()
            self.corpus_en[topic] = freqDist_en[topic].keys()
        words_en = list(set(words_en))
        #/(0.001*len(self.corpus_en[topic]))


        topics_fr = ['Physique','chimie','Politique','Adele_fr','Pakistan_fr','Inde','Babouin']
        self.corpus_fr = {}
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
            self.corpus_fr[topic] = [(st_fr.stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content)) if unicode(i) not in stop_fr]
            freqDist_fr[topic]={x:self.corpus_fr[topic].count(x) for x in self.corpus_fr[topic] if self.corpus_fr[topic].count(x) > 1}
            maxval = max(freqDist_fr[topic].values())
            freqDist_fr[topic]={x:math.exp(freqDist_fr[topic][x]/(1.0+1.0*maxval)) for x in freqDist_fr[topic].keys()}
            words_fr += freqDist_fr[topic].keys()
            self.corpus_fr[topic] = freqDist_fr[topic].keys()
        words_fr = list(set(words_fr))

        self.words_vectors = {}

        print "Generating vectors for english words"
        for word in words_en:
            vec=[]
            for topic in topics_en:
                if topic == 'Baboon':#== 'India' or topic == 'Adele' or topic=='Pakistan':
                    pass
                try:
                    vec.append(freqDist_en[topic][unicode(word)])
                except:
                    vec.append(0)
            self.words_vectors[word]=vec

        print "Generating vectors for french words"
        for word in words_fr:
            vec=[]
            for topic in topics_fr:
                if topic=='Babouin':#topic == 'Inde' or topic == 'Adele_fr' or topic=='Pakistan_fr':
                    pass
                try:
                    vec.append(freqDist_fr[topic][word])
                except:
                    vec.append(0)
            self.words_vectors[word]=vec

        print "Hurray"
        # w=self.words_vectors.values()
        # from mpl_toolkits.mplot3d import Axes3D
        # import matplotlib.pyplot as plt
        # fig = plt.figure()
        # ay = fig.add_subplot(111, projection='3d')
        # ay.scatter(zip(*w)[0],zip(*w)[1],zip(*w)[2])
        # fig.show()
