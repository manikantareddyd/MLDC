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
        self.corpus_en = {}
        self.topics_en = ['Physics','Chemistry','Politics','Adele','Pakistan_en','India','Baboon','pokemon_en']
        self.topics_en_test = ['Baboon','pokemon_en']
        self.corpus_fr = {}
        self.topics_fr = ['Physique','chimie','Politique','Adele_fr','Pakistan_fr','Inde','Babouin','pokemon_fr']
        self.topics_fr_test = ['Babouin','pokemon_fr']
        self.word_vectors = {}
        self.word_vectors_en = {}
        self.word_vectors_fr = {}
        print "Topics Chosen"
        t = PrettyTable(['English', 'French'])
        for i in range(len(self.topics_en)):
            t.add_row([self.topics_en[i],self.topics_fr[i]])
        print t
        # Now lets Generate
        self.gen()

    def gen(self):

        # This Part for English
        print "Working on English"
        topics_en = self.topics_en
        words_en  = []
        stop_en = stopwords.words('english')
        stop_en = [unicode(i) for i in stop_en ]
        st_en = LancasterStemmer()
        freqDist_en={}
        for topic in topics_en:
            # Just the Laborious File Loading tasks
            f=open('files/'+topic+'.txt','r')
            content=f.read()
            f.close()
            print "Loaded",topic

            # This Part now stems every word in the document loaded and copies it into corpus_en.
            words_in_topic  = [(st_en.stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content)) if unicode(i) not in stop_en]

            # Generate a histogram of words in the current document
            freqDist_en[topic]={x:words_in_topic.count(x) for x in words_in_topic if words_in_topic.count(x) > 1}

            # Applying a term frequency function... A factor to be experimented on...
            # Current Function: exp(frequency/(1+max(frequencies)))
            maxval = max(freqDist_en[topic].values())
            freqDist_en[topic]={x:math.exp(freqDist_en[topic][x]/(1.0+1.0*maxval)) for x in freqDist_en[topic].keys()}

            # Add all the words in the current document to all words list
            words_en += freqDist_en[topic].keys()

            # Copy all words in the topic to corpus_en
            self.corpus_en[topic] = freqDist_en[topic].keys()

        # Converting the list of words into a set of words so that duplicates are removed
        words_en = list(set(words_en))

        print "Generating vectors for english words"
        for word in words_en:
            vec=[]
            for topic in topics_en:
                if topic in self.topics_en_test:
                    pass
                try:
                    vec.append(freqDist_en[topic][unicode(word)])
                except:
                    vec.append(0)
            self.word_vectors[word]=vec
            self.word_vectors_en[word]=vec
        print "All Done with English"
        print "-"*48

        #-----------------------------------------------------------------------------------#

        # This Part for French
        print "Working on French"
        topics_fr = self.topics_fr
        words_fr  = []
        stop_fr = stopwords.words('french')
        stop_fr = [unicode(i) for i in stop_fr ]
        st_fr = FrenchStemmer()
        freqDist_fr={}
        for topic in topics_fr:
            # Just the Laborious File Loading tasks
            f=open('files/'+topic+'.txt','r')
            content=f.read()#content.encode('utf8'))
            f.close()
            print "Loaded",topic
            # This Part now stems every word in the document loaded and copies it.
            words_in_topic = [(st_fr.stem(unicode(i))) for i in (re.findall("[a-zA-Z]+", content)) if unicode(i) not in stop_fr]

            # Generate a histogram of words in the current document
            freqDist_fr[topic]={x:words_in_topic.count(x) for x in words_in_topic if words_in_topic.count(x) > 1}

            # Applying a term frequency function... A factor to be experimented on...
            # Current Function: exp(frequency/(1+max(frequencies)))
            maxval = max(freqDist_fr[topic].values())
            freqDist_fr[topic]={x:math.exp(freqDist_fr[topic][x]/(1.0+1.0*maxval)) for x in freqDist_fr[topic].keys()}

            # Add all the words in the current document to all words list
            words_fr += freqDist_fr[topic].keys()

            # Copy all words in the topic to corpus_fr
            self.corpus_fr[topic] = freqDist_fr[topic].keys()

        # Converting the list of words into a set of words so that duplicates are removed
        words_fr = list(set(words_fr))

        print "Generating vectors for french words"
        for word in words_fr:
            vec=[]
            for topic in topics_fr:
                if topic in self.topics_fr_test:
                    pass
                try:
                    vec.append(freqDist_fr[topic][word])
                except:
                    vec.append(0)
            self.word_vectors[word]=vec
            self.word_vectors_fr[word]=vec
        print "All Done with French"
        print "-"*48
        print "All tasks Done... Exiting Now\n"
