#!/usr/bin/python

import codecs
import re
import sys
import os

#making a list of keys and adding new keys.

def new_keys(keys, files):
	for f in files:
		f = codecs.open(f, encoding = "UTF-8-sig")
		lines = f.readlines()
		f.close()

		for l in lines:
			key = l.split("\t")[0]
			if key in keys:
				continue
			else:
				keys.append(key)
	return keys

#returning the value that corresponds to key
def return_value(key, lines):
	value = "NA/na"
	for l in lines:
		if key in l:
			value = l[1]
		else:
			continue
	return value

while True:
	list_files = raw_input("Give the path to the list of files you want to merge:\n")
	if os.path.exists(list_files):
		break
	else:
		print("The path is not correct")

name = raw_input("Give the name of the output tsv file:")

f = codecs.open(list_files, encoding = 'utf-8-sig')
files = f.readlines()
f.close()
for idx,l in enumerate(files):
	files[idx] = l.strip()

keys = []
keys = new_keys(keys = keys, files = files)


new_table = []
new_table.append("\t".join(keys))
for f in files:
	f = codecs.open(f, encoding = "UTF-8-sig")
	lines = f.readlines()
	f.close()
	for idx, l in enumerate(lines):
		lines[idx] = l.split("\t")
	new_file = []
	for key in keys:
		value = return_value(key = key, lines = lines)
		new_file.append(value)
	for idx, value in enumerate(new_file):
		new_file[idx] = value.strip()
	new_file = "\t".join(new_file)
	new_file = new_file
	new_table.append(new_file)

w = codecs.open(name, "w+")
for l in new_table:
	w.write(l.encode("utf-8")+"\n")
w.close()
