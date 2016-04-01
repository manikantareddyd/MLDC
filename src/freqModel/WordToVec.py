import numpy as np
from prettytable import PrettyTable
import re
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import FrenchStemmer
import math


class wordVecGen:
    def __init__(self,topics_list,l):
        # Initializations...
        print "Initializing..."
        self.languages = ['en','fr']
        self.topics_all = topics_list
        self.topics_all = self.topics_all[:l]
        self.corpus = {}
        self.topics = {}
        # self.topics_train = {}
        self.word_vectors = {}
        # self.topics['en_test'] = ['Pokemon_en_test','Chemistry_en']
        # self.topics['fr_test'] = ['Pokemon_fr_test','Chemistry_fr']

        for k in self.languages:
            self.topics[k] = [i +'_'+ k for i in self.topics_all]#+self.topics[k+'_test']
            #self.topics_train[k] = [i +'_'+ k for i in self.topics_all]
            self.word_vectors[k] = {}
            self.corpus[k] = {}

        self.word_vectors_all = {}

        print "Topics Chosen"
        t = PrettyTable(self.languages)
        for i in range(len(self.topics['en'])):
            t.add_row([self.topics[k][i] for k in self.languages])
        print t
        # Now lets Generate
        self.gen()

    def gen(self):

        words = {}
        short_lang = {'en':['english',LancasterStemmer] , 'fr':['french',FrenchStemmer]}
        self.freqDist = {}
        topics = {}
        for k in self.languages:
            # This Part for English
            print "Working on", k
            topics[k] = self.topics[k]
            words[k] = []
            stop = stopwords.words(short_lang[k][0])
            stop = [unicode(i) for i in stop ]
            st = short_lang[k][1]

            self.freqDist[k]={}

            for topic in topics[k]:
                # Just the Laborious File Loading tasks
                f=open('files/'+topic+'.txt','r')
                content=f.read()
                f.close()
                print "Loaded",topic

                # This Part now stems every word in the document loaded and copies it into corpus['en'].
                words_in_topic  = [(st().stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content))]

                # Generate a histogram of words in the current document
                self.freqDist[k][topic]={x:words_in_topic.count(x) for x in words_in_topic}
                for word in self.freqDist[k][topic].keys()[:]:
                    if word in stop:
                        del self.freqDist[k][topic][word]

                # Applying a term frequency function... A factor to be experimented on...
                # Current Function: exp(frequency/(1+max(frequencies)))
                maxval = max(self.freqDist[k][topic].values())
                sumval = sum(self.freqDist[k][topic].values())
                self.freqDist[k][topic]={x:math.log(self.freqDist[k][topic][x]/(1.0+1.0*maxval)) for x in self.freqDist[k][topic].keys()}

                # Add all the words in the current document to all words list
                words[k] += self.freqDist[k][topic].keys()

                # Copy all words in the topic to corpus['en']
                self.corpus[k][topic] = ((self.freqDist[k][topic].keys()))

            # Converting the list of words into a set of words so that duplicates are removed
            words[k] = list(set(words[k]))

            for word in words[k]:
                vec=[]
                for topic in self.topics[k]:
                    try:
                        vec.append(self.freqDist[k][topic][unicode(word)])
                    except:
                        vec.append(0)
                self.word_vectors_all[word]=vec
                self.word_vectors[k][word]=vec

            print "-"*48,'\n'

        #-----------------------------------------------------------------------------------#


        print "All tasks Done... Exiting Now\n"


class Test:
    def __init__(self,wordVecGen, test_topics_list):
        self.wordVecGen = wordVecGen
        self.languages = ['en','fr']
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
        # Now lets Generate
        self.gen()

    def gen(self):
        words = {}
        short_lang = {'en':['english',LancasterStemmer] , 'fr':['french',FrenchStemmer]}
        test_topics = {}
        for k in self.languages:
            test_topics[k] = self.test_topics[k]
            words[k] = []
            stop = stopwords.words(short_lang[k][0])
            stop = [unicode(i) for i in stop ]
            st = short_lang[k][1]

            for test_topic in test_topics[k]:
                f=open('files/'+test_topic+'.txt','r')
                content=f.read()
                f.close()
                print "Loaded",test_topic

                # This Part now stems every word in the document loaded and copies it into corpus['en'].
                words_in_test_topic  = [(st().stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content))]
                self.corpus[k][test_topic] = list(set(words_in_test_topic))
                words[k] += self.corpus[k][test_topic]

            words[k] = list(set(words[k]))

            for word in words[k]:
                vec=[]
                for topic in self.wordVecGen.topics[k]:
                    try:
                        vec.append(self.wordVecGen(self.wordVecGen.freqDist[k][topic][unicode(word)]))
                    except:
                        vec.append(0)
                self.word_vectors[k][word] = vec
