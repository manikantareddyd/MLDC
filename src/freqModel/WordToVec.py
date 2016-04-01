import numpy as np
from prettytable import PrettyTable
import re
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import FrenchStemmer
import math


class wordVecGen:
    def __init__(self):
        # Initializations...
        print "Initializing..."
        self.languages = ['en','fr']
        self.topics_all = ['Adele','Baboon','Chemistry','Pokemon','Energy','English_language','French_language','India','Pakistan','Politics','Tennis','The_Beatles','Wikipedia']
        self.topics_all = self.topics_all[:4]
        self.corpus = {}
        self.topics = {}
        self.topics_train = {}
        self.word_vectors = {}
        self.topics['en_test'] = ['Pokemon_en_test','Chemistry_en']
        self.topics['fr_test'] = ['Pokemon_fr_test','Chemistry_fr']

        for k in self.languages:
            self.topics[k] = [i +'_'+ k for i in self.topics_all]+self.topics[k+'_test']
            self.topics_train[k] = [i +'_'+ k for i in self.topics_all]
            self.word_vectors[k] = {}
            self.corpus[k] = {}

        self.word_vectors_all = {}

        print "Topics Chosen"
        t = PrettyTable(['English', 'French'])
        for i in range(len(self.topics['en'])):
            t.add_row([self.topics['en'][i],self.topics['fr'][i]])
        print t
        # Now lets Generate
        self.gen()

    def gen(self):

        words = {}
        short_lang = {'en':['english',LancasterStemmer] , 'fr':['french',FrenchStemmer]}
        freqDist = {}
        topics = {}
        for k in self.languages:
            # This Part for English
            print "Working on" + k
            topics[k] = self.topics[k]
            words[k] = []
            stop = stopwords.words(short_lang[k][0])
            stop = [unicode(i) for i in stop ]
            st = short_lang[k][1]

            freqDist[k]={}

            for topic in topics[k]:
                # Just the Laborious File Loading tasks
                f=open('files/'+topic+'.txt','r')
                content=f.read()
                f.close()
                print "Loaded",topic

                # This Part now stems every word in the document loaded and copies it into corpus['en'].
                words_in_topic  = [(st().stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content))]

                # Generate a histogram of words in the current document
                freqDist[k][topic]={x:words_in_topic.count(x) for x in words_in_topic}
                for word in freqDist[k][topic].keys()[:]:
                    if word in stop:
                        del freqDist[k][topic][word]

                # Applying a term frequency function... A factor to be experimented on...
                # Current Function: exp(frequency/(1+max(frequencies)))
                maxval = max(freqDist[k][topic].values())
                freqDist[k][topic]={x:math.exp(freqDist[k][topic][x]/(1.0*maxval)) for x in freqDist[k][topic].keys()}

                # Add all the words in the current document to all words list
                words[k] += freqDist[k][topic].keys()

                # Copy all words in the topic to corpus['en']
                self.corpus[k][topic] = freqDist[k][topic].keys()

            # Converting the list of words into a set of words so that duplicates are removed
            print "Number words in English: "+str(len(words[k]))
            words[k] = list(set(words[k]))
            print "Number words in English as set: "+str(len(words[k]))

            print "Generating vectors for english words"
            for word in words[k]:
                vec=[]
                for topic in self.topics_train[k]:
                    try:
                        vec.append(freqDist[k][topic][unicode(word)])
                    except:
                        vec.append(0)
                self.word_vectors_all[word]=vec
                self.word_vectors[k][word]=vec
            print "All Done with English"
            print "-"*48

        #-----------------------------------------------------------------------------------#


        print "All tasks Done... Exiting Now\n"
