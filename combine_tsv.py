#!/usr/bin/python

import codecs
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

#Get files paths and check if path is correct
while True:
	arguments = sys.argv
	if os.path.exists(arguments[1]):
		break
	else:
		print("The path in first argument is not correct")
		sys.exit()


f = codecs.open(arguments[1], encoding = 'utf-8-sig')
files = f.readlines()
f.close()
for idx,l in enumerate(files):
	files[idx] = l.strip()

#Get a list of all keys
keys = []
keys = new_keys(keys = keys, files = files)

#making the tsv table
new_table = []
new_table.append("\t".join(keys))	#First line is the keys

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
	new_table.append(new_file)

w = codecs.open(arguments[2], "w+")
for l in new_table:
	w.write(l.encode("utf-8")+"\n")
w.close()

