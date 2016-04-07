from WordToVec import *
from sklearn.cluster import KMeans
import math
import numpy as np
from scipy.spatial.distance import *

class docSeries:
	def __init__(self,wordVecGen,k):
		self.wv = wordVecGen # Generator for Word Vectors
		# self.Test = Test(wordVecGen, test_list)
		self.k = k
		self.Model = KMeans(k)
		self.Model.fit(self.wv.word_vectors_all.values())
		self.languages = self.wv.languages
		self.topicSeries={}
		threads = {}
		for j in self.languages:
			threads[j]=threading.Thread( target=self.gen, args=(k,j,))
			print "Sequencing "+j+" docs"
			threads[j].start()
			# self.gen(k,j)
		for j in self.languages:
			threads[j].join()
		print "All docs sequenced!"

	def gen(self,k,j):
		#This part for English

		threadTopic = {}
		for topic in self.wv.topics[j]:
			# self.seriesGen(topic,k,j)
			threadTopic[topic] =  threading.Thread(target = self.seriesGen, args = (topic,k,j,))
			threadTopic[topic].start()

		for topic in self.wv.topics[j]:
			threadTopic[topic].join()
			print "Loaded", topic

	def seriesGen(self,topic,k,j):
		series = []
		[series.append(int(self.Model.predict([self.wv.word_vectors[j][word]])[0])) for word in self.wv.corpus[j][topic]]

		self.topicSeries[topic]=np.array(series)


languages = ['en','fr','es'][:]
topics_list = ['Adele','Baboon','Chemistry','Energy','pokemon','English_language','French_language','India','Pakistan','Politics','Tennis','The_Beatles','Wikipedia']
wordVecGen = wordVecGen(topics_list,languages,len(topics_list)/5)
d=docSeries(wordVecGen,50)
