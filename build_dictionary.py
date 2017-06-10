#!/usr/bin/python

##################################################################################

# This pipeline is used to build a dictionary out of 

##################################################################################

import os
import codecs
import sys
import pickle
from functions import list_keys, make_dic

####################################################################################################




#get directory either from arguments or from user
arguments = sys.argv
if len(arguments) == 1:
	directory = raw_input("Please give the path to the directory containing the metadata you want to build the dictionary for:")
else:
	directory = sys.argv[1]


if not directory.endswith("/"):		#adding a slash to the directory name in case it was forgotten
	directory = directory + "/"


if os.path.exists(directory):	#check the path
	experiment_data_files = []
	sample_data_files = []
	for root, dirs, files in os.walk(directory):	#Checking the directory and sub direcotory recursively and make a list of files
		for f in files:
			if f.endswith("emd.tsv"):
				experiment_data_files.append(os.path.join(root, f))
			elif f.endswith("smd.txt"):
				sample_data_files.append(os.path.join(root, f))
else:
	print "The path you gave does not exist, please check it again"
	sys.exit()


#Get a list of all keys using list_keys from functions
experiment_keys = list_keys(experiment_data_files)
sample_keys = list_keys(sample_data_files)


#make the dictionry using make_dic from functions
experimets_dictionary = make_dic(experiment_keys, experiment_data_files)
f = open("experimets_dictionary.txt", "w+")
pickle.dump(experimets_dictionary, f)
f.close()

samples_dictionary = make_dic(sample_keys, sample_data_files)
f = open("samples_dictionary.txt", "w+")
pickle.dump(samples_dictionary, f)
f.close()

