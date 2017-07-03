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


#Check if the metadata file path was given as an argument other wise take it from input
arguments = sys.argv

if len(arguments) == 1:
    while True:
        metadata_path = raw_input("Please, give the name or path of the metadata file.\nAlso note that the metadata file should have two directories (experiment and sample):\n")
        if os.path.exists(metadata_path):
            break
        elif metadata_path == "exit":
            sys.exit()
        else:
            print("WARNING!! The metadata directory path is not valid, please try again or type \"exit\"")
else:
    if os.path.exists(arguments[1]):
        metadata_path = arguments[1]
    else:
        print("WARNING!! The metadata directory path given as an argument was not valid, please try again")
        sys.exit()

#shutil.copytree(metadata_path, metadata_path +"_copy")

#getting the names of file recursively and storing experiment, sample and directories in lists
metadata_files = []
directories = []
for root, dirs, files in os.walk(metadata_path):
    for f in files:
        metadata_files.append(os.path.join(root, f))
                        
for root, dirs, files in os.walk(metadata_path):
    for d in dirs:
        directories.append(os.path.join(root, d))


#####################################################################################################
#making a copy folder for processsed files for now, later will be deleted and one output folder will be present
#TODO use regular expression to name metadata_path everything before the "/"
if metadata_path.endswith("/"):
    metadata_cp = metadata_path.replace("/", "_cp/")
else:
    metadata_cp = metadata_path + "_cp"

if not os.path.exists(metadata_cp):
    os.makedirs(metadata_cp)
    for directory in directories:
        os.makedirs(directory.replace(metadata_path, metadata_cp))

        
#looping through the files
#I separated the several tasks (removing empty lines, fixing encoding, removing extra spaces and so on
#To 3 functions (lines_fixer1, lines_fixer2 and experiment_id)
#This way it's easier to cartch the errors and trouble shoot
#Also I saved the keys separately for later filtering
#As the files will be combined to one table to be processed with the JSON operations we have, then separated again to individual files
#So we need the old keys to filter agains, this way we'll end up with new files that have the same old keys but new values

all_files_keys = [] #storing the unique keys from all the files to make the big table
             

for f in metadata_files:
    lines = read_files(file_name = f)
    
    new_lines = lines_fixer1(lines)
    new_lines = lines_fixer2(new_lines)
    if f.endswith("emd.tsv"):
        new_lines = experiment_id_fix(new_lines, f)
    else:
        new_lines = deep_sample_id_fix(new_lines, f)

    keys = []
    for l in new_lines:
        keys.append(l.split("\t")[0])
    
    for k in keys:
        if k in all_files_keys:
            pass
        else:
            all_files_keys.append(k)
    
    f_write = open(f.replace(metadata_path,metadata_cp) + "keys", "w+") #store the kyes for later filtering, faster than re-reading the old files and extracting the keys then filtering
    pickle.dump(keys, f_write)
    f_write.close()
    
    f_write = open(f.replace(metadata_path,metadata_cp), "w+")
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
