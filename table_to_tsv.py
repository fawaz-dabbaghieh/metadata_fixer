#!/usr/bin/python

import codecs

def tsv_to_files(lines, i):
	keys = lines[0].strip().split("\t")
	values = lines[i].split("\t")
	new_file = []
	for j in range(0,len(keys)):
		new_line = keys[j] + "\t" + values[j]
		new_file.append(new_line)
	return new_file

tsv_file = raw_input("Please give the tsv file name:\n")
directory = raw_input("please give the output directory name:\n")

f_read = codecs.open(tsv_file, encoding = "UTF-8-sig")
lines = f_read.readlines()
f_read.close()
keys = lines[0].split("\t")
for idx, l in enumerate(keys):
	if l == "EXPERIMENT_ID":
		exp_id_idx = idx

for i in range(1,len(lines)):
	file_name = lines[i].split("\t")[exp_id_idx] + "_emd.tsv"
	f_write = open(directory+"/"+file_name, "w+")
	new_file = tsv_to_files(lines = lines, i = i)
	for l in new_file:
		f_write.write(l.encode('UTF-8') + "\n")
	f_write.close()
