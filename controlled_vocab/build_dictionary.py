#!/usr/bin/python

##################################################################################

# This pipeline is used to build a dictionary out of 

##################################################################################

import os
import codecs
import sys
import pickle

#getting a list of keys
def list_keys(files):
	keys = []
	for f in files:
		f = codecs.open(f, encoding = "utf-8-sig")
		lines = f.readlines()
		f.close()
		lines = map(encode, lines)
		for l in lines:
			l = l.split("\t")
			if l[0] not in keys:
				keys.append(l[0])
			else:
				continue
	return keys

#Build dictionary function
def make_dic(keys, files):
	dic = {}
	for key in keys:
		dic[key] = []
	for f in files:
		f = codecs.open(f, encoding = "utf-8-sig")
		lines = f.readlines()
		f.close()
		lines = map(strip, lines)
		lines = map(encode, lines)
		for l in lines:
			if l.split("\t")[1] in dic[l.split("\t")[0]]:
				continue
			else:
				dic[l.split("\t")[0]].append(l.split("\t")[1])
	return dic


def strip(x): return x.strip()
def encode(x): return x.encode("utf-8")


####################################################################################################

#get directory
directory = raw_input("Please give the path to the directory containing the metadata you want to build the dictionary for:")

if os.path.exists(directory):
	data_files = []
	for root, dirs, files in os.walk(directory):	#Checking the directory and sub direcotory recursively
		for f in files:
			if f.endswith("emd.tsv") or f.endswith("smd.txt"):
				data_files.append(os.path.join(root, f))
else:
	print "The path you gave does not exist, please check it again"
	sys.exit()


#Get a list of all keys
keys = list_keys(data_files)

#make the dictionry
dictionary = make_dic(keys, data_files)

f = open("dictionary.txt", "w+")
pickle.dump(dictionary,f)
f.close()
