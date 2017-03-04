#import matplotlib.pyplot as plt

# This function finds out the average of the number of empty cells in each 
# row and column and removes a row/column data if the percentage is more than 
# the given cut-off percentage "per"
def check_fill_percentage(data, per):

	tot = len(data)
	data_new = []
	column = []
	count = []
	# First update the column variance & the the row variance
	for j in range(0,len(data[0])):
		ct = 0
		for i in range(0,len(data)):
			if data[i][j] == "?":
				ct += 1
		p = ct*1.0/tot
		count.append(p)
		if p<= per:
			column.append(0)
		else:
			column.append(1)

	print sum(column)
	print count

	for row in data:
		j = 0
		temp = []
		temp = column[:]
		for element in row:
			if temp[j] == 1:
				del row[j]
				del temp[j]
			else:
				j += 1
		data_new.append(row)

	print data[0]
	data = []
	tot = len(data_new[0])
	for row in data_new:
		ct = 0
		for element in row:
			if element == '?':
				ct += 1
		p = ct*1.0/tot
		if p <= per:
			data.append(row)
	return data

# Verify duplicate data entries based on Encounter ID and returns True if there is
# any duplicate data
def isduplicate(data):
	k = {}
	for row in data:
		if row[0] not in k:
			k[row[0]] = 1
		else:
			return True
	return False

# Remove duplicate data entries based on Encounter ID and returns the data with the
# duplicate data entries removed
def deduplication(data):
	k = {}
	i = 0
	for row in data:
		if row[0] not in k:
			k[row[0]] = 1
			i += 1
		else:
			data.pop(i)
	return data


# This function checks the variance of each of the data features and returns it as
# a list (After treating the missing variables!!!!!!!!!!!!!!!!!!!!!!!!!)
# Write another function that gets the cut-offs as an input and handles the removal
# of highly invariant data or data with no invariance
def variance_check(data):
	a = []
	tot = len(data)
	l = {}
	for j in range(0,len(data[0])):
		k = {}
		ct = 0
		for i in range(0,len(data)):
			if data[i][j] not in k:
				k[data[i][j]] = 1
				ct += 1
		p = ct*1.0/tot
		a.append(p)
		l[len(a)] = k
	return a,l

# This function is responsible for recategorizing the readmitted column i,e, output
# column to just binary outputs by replacing <30 as 1 and remaining as 0
def recategorize_output(data):
	for row in data:
		if row[-1] == "readmitted":
			pass
		elif row[-1] == "<30":
			row[-1] = "1"
		else:
			row[-1] = "0"
	return data

# The following code snippet is responsible for handling the missing values in 
# the feature column race by filling it with data that's already present using 
# the correlation in the patient number ids feature
def handle_empty_data_race(data):
	a = {}
	for row in data:
		if row[2] != "?":
			if row[1] not in a:
				a[row[1]] = row[2]

	for row in data:
		if row[2] == "?":
			if row[1] in a:
				row[2] = a[row[1]]
			else:
				pass#row[2] = "Other"
	return data


# This functions returns the count on categorical data w.r.t each column, thereby 
# used for plotting a boxplot to study and understand how the data is scattered. 
def plot(data,colum):
	a = {}
	count = 0
	for row in data:
		if row[colum-1] not in a:
			count +=1
			a[row[colum-1]] = 1
		else:
			a[row[colum-1]] += 1
	print count
	return a


# This function helps down in processing to replace the tuple into a single data
# row
def processed_range_to_string(a):
	return "(" + str(a[0]) + " - " + str(a[1]) + ")"

# This code snippet recategorizes the diagonosis feature values into a smaller
# number of category set, by grouping up logically similar kind of diagonosis 
# values
def recategorize_column_diag(data,st,j):
	for l in range(0,len(data[0])):
		if data[0][l] == "diag_1":
			break
	for row in data:
		if row[l+j] == "diag_1" or row[l] == "diag_2" or row[l] == "diag_3":
			continue
		try:
			g = float(row[l+j])
			flag = 0
			i = 0
			while flag != 1 and i < 17:
				if g >= st[i][0] and g <= st[i][1]:
					row[l+j] = processed_range_to_string(st[i])
					flag = 1
				i += 1
		except:
			g = row[l+j]
			if g[0] == st[17][0][0]:
				row[l+j] = processed_range_to_string(st[17])
			elif g[0] == st[18][0][0]:
				row[l+j] = processed_range_to_string(st[18])



# This code snippet is responsible for recategorizing to feature column 
# admission_type_id deleting inconsistencies in the categorization using 
# data study
def recategorize_column_adm_type(data):
	for l in range(0,len(data[0])):
		if data[0][l] == "admission_type_id":
			break
	for row in data:
		if row[l] == "admission_type_id":
			continue
		if row[l] == "7" or row[l] == "1":
			row[l] = "Emergency"
		elif row[l] == "5" or row[l] == "6" or row[l] == "8":
			row[l] = "Not Available"
		elif row[l] == "3":
			row[l] = "Elective"
		elif row[l] == "2":
			row[l] = "Urgent"
		else:
			row[l] = "Newborn"

# This code snippet is responsible for recategorizing to feature column 
# admission_source_id deleting inconsistencies in the categorization using 
# data study, combining categories that have similar definitions and 
# deleting rows that seem to have been categorized as outlier
def recategorize_column_adm_source_id(data):
	for l in range(0,len(data[0])):
		if data[0][l] == "admission_source_id":
			break
	k = 0
	new = []
	for row in data:
		if row[l] == "admission_source_id":
			new.append(row)
			continue
		if row[l] == "17" or row[l] == "9" or row[l] == "20":  #Combining Not Available
			row[l] = "Not Available"
			new.append(row)
		elif row[l] == "10":    # Combining Transfer from hospitals 
			row[l] = "4"
			new.append(row)
		elif row[l] == "11" or row == "13" or row[l] == "14": # Deleting Rows (very low vfill ratio)
			pass
		else:
			new.append(row)
	return new

# This code snippet is responsible for recategorizing to feature column 
# discharge_disposition_id deleting inconsistencies in the categorization using 
# data study, combining categories that have similar definitions and 
# deleting rows that seem to have been categorized as outlier
def recategorize_column_discharge_id(data):
	for l in range(0,len(data[0])):
		if data[0][l] == "discharge_disposition_id":
			break
	new = []
	for row in data:
		if row[l] == "discharge_disposition_id":
			new.append(row)
			continue
		if row[l] == "18" or row[l] == "25":  #Combining Not Available
			row[l] = "Not Available"
			new.append(row)
		elif row[l] == "19" or row[l] == "20":    # Combining Expired 
			row[l] = "11"
			new.append(row)
		elif row[l] == "17":    # Combining Discharged/transferred to outpatient services 
			row[l] = "16"
			new.append(row)
		elif row[l] == "14":    # Combining Hospice 
			row[l] = "13"
			new.append(row)
		elif row[l] == "10" or row == "12" or row[l] == "27":  # Deleting Rows (very low vfill ratio)
			pass
		else:
			new.append(row)
	return new


# The following code snippet checks the counts on the categories for individual
# features. Specifically counts the number of 0 and 1 classifications.
def category_check(data,i):
	a = {}
	for row in data:
		if data[0] == row:
			continue
		if row[i] not in a:
			if row[-1] == 1:
				a[row[i]] = 1
				a[row[i]+"_neg"] = 0
			else:
				a[row[i]] = 0
				a[row[i]+"_neg"] = 1
		else:
			if row[-1] == 1:
				a[row[i]] += 1
			else:
				a[row[i]+"_neg"] += 1
	return a

# This code snippet is used to extract the first occurence of a patient id in
# the data set
def extract_first_patient_encounter(data):
	a = {}
	for row in data:
		if row[1] not in a:
			a[row[1]] = True

	return a

# This code remove the feature values patient_num_id and encounter_id, since
# these features have very high variance
def remove_encounter_patientid(data):
	for row in data:
		del row[0]
		del row[0]
		row[4] = str(row[4])
		row[5] = str(row[5])