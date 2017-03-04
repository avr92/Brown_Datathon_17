import csv
import pandas as pd
#import matplotlib.pyplot as plt

def read_from_file():
	your_list = []
	with open('./datathon_tadata.csv', 'rb') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	return your_list

data = read_from_file()

col_index = []
h_map = {}

for item in data[0]:
	h_map[item] = []
	col_index.append(item)


for row in data:
	for i in range(0,len(col_index)):
		h_map[col_index[i]].append(row[i])

print len(h_map[col_index[0]])

col_index = col_index[13:]
i = 0
for ind in col_index:
	#if ind == 'p_sessionDuration' or ind == 'p_pageViews' or ind == 'p_TotalPrice':
	#	continue
	new_hash = {}
	for d in pd.unique(h_map[ind]):
		if d not in new_hash:
			new_hash[d] = [0,0]
	print len(new_hash)
	for row in data:
		row = row[13:]
		for key in new_hash:
			if row[i] == key:
				if row[len(col_index) - 1] == '0':
					new_hash[key][0] += 1
				else:
					new_hash[key][1] += 1
				break
	print new_hash
	i += 1

