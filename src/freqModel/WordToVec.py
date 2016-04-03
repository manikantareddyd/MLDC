import numpy as np
from prettytable import PrettyTable
import re
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import FrenchStemmer
from nltk.stem import *
import math
import threading

class wordVecGen:
    def __init__(self,topics_list,languages,tmp):
        # Initializations...
        print "Initializing..."
        self.languages = languages
        self.topics_all = topics_list
        self.topics_all = self.topics_all[:tmp]
        self.corpus = {}
        self.topics = {}
        self.word_vectors = {}

        for k in self.languages:
            self.topics[k] = [i +'_'+ k for i in self.topics_all]#+self.topics[k+'_test']
            self.word_vectors[k] = {}
            self.corpus[k] = {}

        self.word_vectors_all = {}

        print "Topics Chosen"
        t = PrettyTable(self.languages)
        for i in range(len(self.topics['en'])):
            t.add_row([self.topics[k][i] for k in self.languages])
        print t

        self.words = {}
        # self.shortlang = {'en':['english',SnowballStemmer("english", ignore_stopwords=True)] , 'fr':['french',SnowballStemmer("french", ignore_stopwords=True)],'es':['spanish',SnowballStemmer("spanish", ignore_stopwords=True)]}
        self.language = {'en':'english','fr':'french','es':'spanish'}
        self.stop = {}
        for k in self.languages:
            self.stop[k] = stopwords.words(self.language[k])
        self.freqDist = {}

        threads={}
        # Now lets Generate
        for k in self.languages:
            threads[k]=threading.Thread( target=self.gen, args=(k,))
            print "Working on", k
            threads[k].start()
            # self.gen(k)
        for k in self.languages:
            threads[k].join()

        print "All tasks Done... Exiting Now\n"

    def gen(self,k):
        # threading.Thread.gen(self,k)
        # This Part for English

        self.words[k] = []
        stop = self.stop[k]
        stop = [unicode(i) for i in stop ]

        self.freqDist[k]={}

        threadTopic = {}
        for topic in self.topics[k]:
            # self.load(topic,k,stop)
            threadTopic[topic] = threading.Thread(target = self.load, args=(topic,k,stop,))
            threadTopic[topic].start()

        for topic in self.topics[k]:
            threadTopic[topic].join()
            print "Loaded",topic

        self.words[k] = list(set(self.words[k]))

        for word in self.words[k]:
            self.vectorGen(k,word)

    def vectorGen(self,k,word):
        vec=[]
        for topic in self.topics[k]:
            try:
                vec.append(self.freqDist[k][topic][unicode(word)])
            except:
                vec.append(0)
        self.word_vectors_all[word]=vec
        self.word_vectors[k][word]=vec

    def load(self,topic,k,stop):
        # Just the Laborious File Loading tasks
        f=open('files/'+topic+'.txt','r')
        content=f.read()
        f.close()

        # This Part now stems every word in the document loaded and copies it into corpus['en'].
        words_in_topic  = [(SnowballStemmer(self.language[k], ignore_stopwords=True).stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content))]

        # Generate a histogram of words in the current document
        self.freqDist[k][topic]={x:words_in_topic.count(x) for x in words_in_topic}
        for word in self.freqDist[k][topic].keys()[:]:
            if word in stop:
                del self.freqDist[k][topic][word]

        # Applying a term frequency function... A factor to be experimented on...
        # Current Function: exp(frequency/(1+max(frequencies)))
        maxval = max(self.freqDist[k][topic].values())
        sumval = sum(self.freqDist[k][topic].values())
        self.freqDist[k][topic]={x:math.exp(self.freqDist[k][topic][x]/(1.0+1.0*maxval)) for x in self.freqDist[k][topic].keys()}

        # Add all the words in the current document to all words list
        self.words[k] += self.freqDist[k][topic].keys()

        # Copy all words in the topic to corpus['en']
        self.corpus[k][topic] = ((self.freqDist[k][topic].keys()))


class Test:
    def __init__(self,wordVecGen, test_topics_list):
        self.wordVecGen = wordVecGen
        self.languages = self.wordVecGen.languages
        self.test_topics_all = test_topics_list
        self.corpus = {}
        self.test_topics = {}
        self.word_vectors = {}
        for k in self.languages:
            self.test_topics[k] =  [i +'_'+ k for i in self.test_topics_all]
            self.word_vectors[k] = {}
            self.corpus[k] = {}

        self.word_vectors_all = {}

        print "Test Topics Chosen"
        t = PrettyTable(self.languages)
        for i in range(len(self.test_topics['en'])):
            t.add_row([self.test_topics[k][i] for k in self.languages])
        print t

        self.words = {}

        # self.shortlang = {'en':['english',LancasterStemmer] , 'fr':['french',FrenchStemmer]}
        self.language = {'en':'english','fr':'french','es':'spanish'}
        self.stop = {}
        for k in self.languages:
            self.stop[k] = stopwords.words(self.language[k])
        # Now lets Generate

        threads = {}
        for k in self.languages:
            threads[k]=threading.Thread( target=self.gen, args=(k,))
            threads[k].start()
            # self.gen(k)
        for k in self.languages:
            threads[k].join()

        print "Loaded Topics in Test set\n"

    def gen(self,k):
        self.words[k] = []
        stop = self.stop[k]
        stop = [unicode(i) for i in stop ]

        threadTopic = {}
        for topic in self.test_topics[k]:
            # self.load(topic,k,stop)
            threadTopic[topic] = threading.Thread(target = self.load, args=(topic,k,stop,))
            threadTopic[topic].start()
        for topic in self.test_topics[k]:
            threadTopic[topic].join()
            print "Loaded",topic

        self.words[k] = list(set(self.words[k]))

        wordThreads = {}
        for word in self.words[k]:
            self.vectorGen(k,word)
        #     wordThreads[word] = threading.Thread(target = self.vectorGen, args=(k,word,))
        #     wordThreads[word].start()
        #
        # for word in self.words[k]:
        #     wordThreads[word].join()


    def vectorGen(self,k,word):
        vec=[]
        for topic in self.wordVecGen.topics[k]:
            try:
                vec.append(self.wordVecGen(self.wordVecGen.freqDist[k][topic][unicode(word)]))
            except:
                vec.append(0)
        self.word_vectors[k][word] = vec

    def load(self,test_topic,k, stop):
        f=open('files/'+test_topic+'.txt','r')
        content=f.read()
        f.close()


        # This Part now stems every word in the document loaded and copies it into corpus['en'].
        words_in_test_topic  = [(SnowballStemmer(self.language[k], ignore_stopwords=True).stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content)) if i not in stop]
        self.corpus[k][test_topic] = list(set(words_in_test_topic))
        self.words[k] += self.corpus[k][test_topic]
