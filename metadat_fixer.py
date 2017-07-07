#!/usr/bin/python

from functions import *
import codecs
import os
import subprocess
import sys
import re
import pickle
sys.path.append("refine.py")
import refine
import time
import signal


def strip(x): return x.strip()
def split(x): return x.split("\t")
def encode(x): return x.encode("utf-8")


#Check if the metadata file path was given as an argument otherwise take it from input
arguments = sys.argv

if len(arguments) == 1:
    while True:
        metadata_path = raw_input("Please, give the name or path of the metadata file.\nAlso note that the metadata file should have two directories (experiment and sample):\n")
        if os.path.exists(metadata_path):
            break
        elif metadata_path == "exit":
            sys.exit()
        else:
            print("The metadata directory path is not valid, please try again or type \"exit\"")
else:
    if os.path.exists(arguments[1]):
        metadata_path = arguments[1]
    else:
        print("WARNING!! The metadata directory path given as an argument was not valid, please try again")
        sys.exit()


#storing the names of the directories and files in lists
metadata_files = []
directories = []
for root, dirs, files in os.walk(metadata_path):
    for f in files:
        metadata_files.append(os.path.join(root, f))
                        
for root, dirs, files in os.walk(metadata_path):
    for d in dirs:
        directories.append(os.path.join(root, d))


#####################################################################################################
#copying all files to work on them, then output the results in a separate folder and delete the intermediate copy folder
if metadata_path.endswith("/"):
    metadata_cp = metadata_path.replace("/", "_cp/")
else:
    metadata_cp = metadata_path + "_cp"

if not os.path.exists(metadata_cp):
    os.makedirs(metadata_cp)
    for directory in directories:
        os.makedirs(directory.replace(metadata_path, metadata_cp))

        
"""
looping through the files.
I separated the several tasks (removing empty lines, fixing encoding, removing extra spaces and so on) To 3 functions (lines_fixer1, lines_fixer2 and experiment_id) This way it's easier to catch the errors and trouble shoot any problem.

Also I saved the keys of the original files separately for later filtering after merging all the files together.

I'm reading each file once and looping through the lines
"""

all_files_keys = [] #storing the unique keys from all the files to make the big table
             

for f in metadata_files:
    lines = read_files(file_name = f)		#function for reading the files with the correct encoding
    
    new_lines = lines_fixer1(lines)		#First round of fixes
    new_lines = lines_fixer2(new_lines)		#Second round of fixes
    if f.endswith("emd.tsv"):                   #TODO readme
        new_lines = experiment_id_fix(new_lines, f)	#This function checks if the experiment_id is correct
    else:
        new_lines = deep_sample_id_fix(new_lines, f)	#This function checks if the sample_id is correct

    keys = []			#storing the keys for later filtering
    for l in new_lines:
        keys.append(l.split("\t")[0])
    
    for k in keys:
        if k in all_files_keys:	#making a list of all the unique keys of all the files
            pass
        else:
            all_files_keys.append(k)
    
    f_write = open(f.replace(metadata_path,metadata_cp) + "keys", "w+") 
    pickle.dump(keys, f_write)
    f_write.close()
    
    f_write = open(f.replace(metadata_path,metadata_cp), "w+")	#writing the fixed files
    for l in new_lines:
        f_write.write(l.encode('utf-8') + '\n')
    f_write.close()

    
###########################################################################
#combine the experiment files and sample files each to one table to process with the JSON operations using OpenRefine
new_files_table = []  #Table of all experiments

    
new_files_table = merge_files(metadata_files, all_files_keys)
w = open( "all_files_table.tsv", "w+")
for l in new_files_table:
    w.write(l.encode("utf-8")+"\n")
w.close()

###########################################################################
#giving the tables to Openrefine with the JSON operations
#we need to start OpenRefine first in the background to use it
#We need to start with subprocess and store the ID to kill it later

open_refine = subprocess.Popen("openrefine-2.7-rc.1/./refine", stdout=subprocess.PIPE, shell=True, preexec_fn = os.setsid)

print "starting OpenRefine:",
for i in ["1"]*10:
    print "."
    time.sleep(float(i))


r = refine.Refine()
p = r.new_project("all_files_table.tsv")
p.apply_operations("operations.json")
after_json_experiment_table = p.export_rows()
p.delete_project()

after_json_experiment_table = after_json_experiment_table.split("\n")

#for idx, l in enumerate(after_json_experiment_table):
    #after_json_experiment_table[idx] = after_json_experiment_table[idx].decode("utf-8")
    

if after_json_experiment_table[-1] == "":
    del after_json_experiment_table[-1]

w = open("after_json_experiment_table.tsv", "w+")
for l in after_json_experiment_table:
    w.write(l + "\n")
w.close()

os.killpg(os.getpgid(open_refine.pid), signal.SIGTERM)  # Send the signal to all the process groups

#splitting the table after JSON to individual files
#TODO make new directory replace metadata_path 
metadata_json = metadata_path + "_after_json"
if not os.path.exists(metadata_json):
    os.makedirs(metadata_json)
    for directory in directories:
        os.makedirs(directory.replace(metadata_path, metadata_json))
        
table_to_files2(after_json_experiment_table, metadata_path)
#a functions to check that's experiments are tsv and samles are txt
#Continue with tasks according to metadata_fixer
