import numpy as np
#import matplotlib.pyplot as plt
import random
import csv
from data_clean import *
from sklearn import preprocessing
from RandomForest import *


# This file is responsible for reading the diabetics data from the
# file in the specified path, under data folder 
def read_from_file():
	your_list = []
	with open('./data/diabetic_data.csv', 'rb') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	return your_list

categories = []
unique_list = {}


# This function retreives the unqiue list of categories present for each feature 
# columns
def encode(arr):
	for i in categories:
		for j in range(0,len(unique_list[i])):
			if unique_list[i][j] == arr[i]:
				arr[i] = str(j)
				break
	return arr


if __name__ == "__main__":

	data = []

	# The following is the list of logical classes used to
	# recategorize the Diagonosis 1, Diagnosis 2, Diagnosis 3
	# into reduced number of features
	st = [(1,139), (140,239), (240,279), (280,289),
		  (290,319), (320,389), (390,459), (460,519),
		  (520,579), (580,629), (630,679), (680,709),
		  (710,739), (740,759), (760,779), (780,799),
		  (800,999), ("V01","V91"), ("E000","E999")]

	data = read_from_file()

	data = check_fill_percentage(data, 0.39)   # Part of the data_clean.py
	
	data = deduplication(data)     # Part of the data_clean.py
	
	data = recategorize_output(data)    # Part of the data_clean.py
	data = handle_empty_data_race(data)    # Part of the data_clean.py
	a,l = variance_check(data)    # Part of the data_clean.py

	for j in range(0,3):
		recategorize_column_diag(data,st,j)     # Part of the data_clean.py

	recategorize_column_adm_type(data)			 # Part of the data_clean.py
	data = recategorize_column_adm_source_id(data)    # Part of the data_clean.py
	data = recategorize_column_discharge_id(data)      # Part of the data_clean.py
	
	a = extract_first_patient_encounter(data)     # Part of the data_clean.py

	remove_encounter_patientid(data)      # Part of the data_clean.py


	# This code snippet is responsible for recording the row ids of first instance
	# of a patient record in the data
	myfile = open("patient_first_encounter.csv",'wb')
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	for row in a:
		wr.writerow(row)

	# Converting to numpy data
	my_data = np.array(data)

	#print data[1]
	#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

	# The list of feature categories that are nominal data type
	categories = [0,1,2,3,4,5,13,14,15,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
	unique_list = {}

	# The following code section is responsible for facilitating the process
	# of hotencoding, i,e, splitting the categories in an individual feature column
	# to multiple feature columns. This is a step to converting the nominal data
	# type to close to numeric data type. Hence, the values can be directly inputted to
	# our model libraries to predict accuracy values.
	m = 0
	for i in categories:
		unique_list[i] = np.unique(my_data[1:,i])
		if len(unique_list)>m:
			m = len(unique_list)

	
	encoder = []
	for k in range(0,m):
		row = []
		for i in range(0,len(my_data[0])):
			if i in unique_list:
				if k < len(unique_list[i]):
					row.append(str(k))
				else:
					row.append("0")
			else:
				row.append("0")
		encoder.append(row)
	

	X_label = []
	X_label1 = []
	for i in range(0,len(my_data[0])):
		if i in unique_list:
			for j in range(0,len(unique_list[i])):
				X_label.append(unique_list[i][j]+str(i))
		else:
			X_label1.append(my_data[0][i]+str(i))
	i = 0
	print X_label1
	for i in range(0,len(X_label1)):
		X_label.append(X_label1[i])

	X = [X_label]

	print len(X)

	enc = preprocessing.OneHotEncoder(categorical_features=categories)
	enc.fit(encoder)
	for row in my_data[1:]:
		X_small = enc.transform(encode(row)).toarray()
		X.append(X_small[0].tolist())

	#myfile = open("processed_data_new_v2.csv",'wb')
	#wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	#for row in X:
	#	wr.writerow(row)

	building_model_accuracy(X)

