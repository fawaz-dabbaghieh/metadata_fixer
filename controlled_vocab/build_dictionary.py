#!/usr/bin/python

##########################################################################################

# This pipeline is used to build a dictionary out of the metadata from the DEEP project

##########################################################################################

import os
import codecs
import sys
import re
from dictionary_functions import *


####################################################################################################


#get directory path either from arguments or from user

arguments = sys.argv
if len(arguments) == 1:
    directory = raw_input("Please give the path to the directory containing the metadata you want to build the dictionary for:")
else:
    directory = sys.argv[1]


if not directory.endswith("/"):		#adding a slash to the directory name in case it was forgotten
    directory = directory + "/"



#check if the path exists and get the names of all the files
if os.path.exists(directory):
    experiment_data_files = []
    sample_data_files = []
    for root, dirs, files in os.walk(directory):    #Checking the directory and sub directory recursively and make a list of files
        for f in files:
            if f.endswith("emd.tsv"):
                experiment_data_files.append(os.path.join(root, f))      #joining the name of the file with the path
            elif f.endswith("smd.txt"):
                sample_data_files.append(os.path.join(root, f))     #joining the name of the file with the path
else:
    print "The path you gave does not exist, please check it and try again"
    sys.exit()
    
    
    
#getting the regex keys for later filtering, the file should be in the same directory with the script
if os.path.exists("regex_dictionary.tsv"):
    regex_dict = read_dictionary("regex_dictionary.tsv")
    regex_keys = regex_dict.keys()
else:
    print ("The regex_dictionary.tsv was not found, it should be in the same directory as this script. Please, try again ")
    sys.exit()



#getting the black keys for later filtering, the file should be in the same directory with the script
if os.path.exists("black_keys.txt"):
    black_keys = read_files("black_keys.txt")
    black_keys = map(strip, black_keys)
else:
    print ("The black_keys.txt file was not found, it should be in the same directory as this script. Please, try again ")
    sys.exit()


#Get a list of all unique keys for all the files using list_keys from functions
#Then give the list of keys to the build_dic function to make the dictionary from these files

if experiment_data_files != []:             #in case there were no experient files
    experiment_keys = list_keys(experiment_data_files, regex_keys, black_keys)
    experiments_dictionary = build_dic(experiment_keys, experiment_data_files)
    if experiments_dictionary:
        write_dictionary(experiments_dictionary, "experiments_dictionary.tsv")
    else:
        print "experiments dictionary was not built"
else:
    print "There were no experiment data files"


#Get a list of all unique keys for all the files using list_keys from functions
#Then give the list of keys to the build_dic function to make the dictionary from these files

if sample_data_files != []:             #in case there were no sample files
    sample_keys = list_keys(sample_data_files, regex_keys, black_keys)
    samples_dictionary = build_dic(sample_keys, sample_data_files)
    if samples_dictionary:
        write_dictionary(samples_dictionary, "samples_dictionary.tsv")
    else:
        print "samples dictionary was not built"
        
else:
    print "There were no Sample data files"