import numpy as np
from keras.models import Sequential
from keras.layers.core import Activation, Dense, Dropout
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.preprocessing import sequence
from keras.utils import np_utils
from docTimeSeries import  *
import random
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

class rC:
	def __init__(self,docSeries):
		self.load(docSeries)
	def load(self,docSeries):
		topics = docSeries.topicSeries.keys()
		seriesLength = 50
		sequenceTuples = []
		for j in range(len(topics)):
			topic = topics[j]
			topicLength = len(docSeries.topicSeries[topic])
			for i in range(0,topicLength):
				if i+seriesLength < topicLength:
					sequenceTuples.append((docSeries.topicSeries[topic][i:i+seriesLength],j))
		random.shuffle(sequenceTuples)
		X = []
		y = []
		for s,l in sequenceTuples:
			X.append(s)
			y.append(l)
		X = np.array(X).astype(np.uint8)
		y = np_utils.to_categorical(np.array(y)).astype(np.bool)
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
		print len(X_train),len(y_train)
		print X.shape,y.shape
		model = Sequential()
		model.add(Embedding(50, 64, input_length = seriesLength, mask_zero = True))
		model.add(LSTM(64,init='glorot_uniform',inner_init='orthogonal',activation='tanh',inner_activation='hard_sigmoid',return_sequences=False))
		model.add(Dropout(0.5))
		model.add(Dense(len(topics)))
		model.add(Activation('softmax'))
		model.compile(loss='categorical_crossentropy', optimizer='adam', class_mode='categorical')
		early_stopping = EarlyStopping(patience=5, verbose=1)
		model.fit(X_train, y_train,show_accuracy=True,verbose=1,shuffle=True)
		preds = model.predict_classes(X_test, batch_size=64, verbose=0)
		print '\n'
		print(classification_report(np.argmax(y_test, axis=1), preds, target_names=topics))
r=rC(d)
