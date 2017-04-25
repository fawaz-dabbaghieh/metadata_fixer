#!/usr/bin/python

#To convert a big table back to individual tsv files
#The table has column as keys, and rows as experiment metadata

import codecs

#The conversion function

def tsv_to_files(lines, i):

	#keys are the first row

	keys = lines[0].strip().split("\t")
	values = lines[i].split("\t")
	new_file = []
	for j in range(0,len(keys)):
		new_line = keys[j] + "\t" + values[j]
		new_file.append(new_line)
	return new_file

#the UTF-8-sig is used to get rid of the BOM in some files

f_read = codecs.open("all_experiments_after_json.tsv", encoding = "UTF-8-sig")
lines = f_read.readlines()
f_read.close()

#Checking which column is the EXPERIMENT_ID column to name each file with its corrisponding EXPERIMENT_ID

keys = lines[0].split("\t")
for idx, l in enumerate(keys):
	if l == "EXPERIMENT_ID":
		exp_id_idx = idx

#Looping through the lines and writing the files

for i in range(1,len(lines)):
	file_name = lines[i].split("\t")[exp_id_idx] + "_emd.tsv"
	f_write = open(file_name, "w+")
	new_file = tsv_to_files(lines = lines, i = i)
	for l in new_file:
		f_write.write(l.encode('UTF-8') + "\n")
	f_write.close()
