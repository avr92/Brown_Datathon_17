import numpy as np
import random
import csv
from sklearn import *
from sklearn.metrics import *
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing


from sklearn.feature_selection import SelectFromModel

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


def oversample(X):
	new = []
	for i in range(0,5):
		for row in X:
			if row[-1] == 1:
				new.append(row)
	#print "HAHAHA" + str(len(new))

	k = len(X)

	X1 = X.tolist()

	for row in new:
		j = random.randint(0,k)
		X1.append(row)

	X = np.asarray(X1)
	return X


def undersample(X):
	s = {}
	for i in range(0,len(my_data[0])):
		if (('?' in my_data[0][i]) or ('Not' in my_data[0][i]) or ('Unknown' in my_data[0][i])) :
			#print "HAHAA"
			s[i] = 1


	X1 = X.tolist()
	
	new = []
	k = 1
	no = 0
	d = 70000
	for row in X1:
		flag = 0
		if row[-1] == 0:
			for i in s:
				if row[i] == 1:
					flag = 1
					break
			if flag == 0:
				if k % 2 == 0 and no < d:
					no += 1
					pass
				else:
					new.append(row)
				k += 1
		else:
			new.append(row)


	return np.asarray(new)



def building_model_accuracy(my_dat):

	X = np.array(my_dat[1:])

	X = X.astype("float")

	#X = undersample(X)

	X = oversample(X)

	print "total number of class 0 instances:" +  str(len(X) - sum(X[:,-1]))
	print "total number of class 1 instances:" +  str(sum(X[:,-1]))


	#myfile = open("processed_data_newsample_v3.csv",'wb')
	#wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	#wr.writerow(my_data[0])
	#for row in X:
	#	wr.writerow(row)

	#print X[:,:-1].shape

	X_normalized = preprocessing.normalize(X[:,:-1], norm='l2')

	features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(X_normalized, X[:,-1], random_state=42, test_size=0.3)

	clf = RandomForestClassifier(n_estimators=50, max_depth=18)

	clf = clf.fit(features_train, labels_train)

	#print clf.score(features_test, labels_test)
	y_pred = clf.predict(features_test)
	#print confusion_matrix(labels_test, y_pred,labels=[0, 1])

	scores = cross_val_score(clf, X_normalized, X[:,-1], cv=10)
	print scores
	print scores.mean(), scores.std() * 2

	y_pred1 = clf.predict(features_train)
	#print clf.score(features_train, labels_train)


'''
	# This function was used to rank and extract the best features 
	# using inbuilt library techniques. This data was used for study 
	# and used for possiblities of picking up selective feature attributes.
	clf = ExtraTreesClassifier(n_estimators=10)
	clf = clf.fit(X[:,:-1], X[:,-1])
	model = SelectFromModel(clf, prefit=True)
	X_new = model.transform(X[:,:-1])
	print X_new.shape
'''

