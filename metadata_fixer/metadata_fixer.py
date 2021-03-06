#!/usr/bin/python
# todo an arg parser for this script
# to get where is the script I can use this os.sep.join(os.path.realpath(__file__).split(os.sep)[:-1])

from metadata_fixer_functions import *
import os
import subprocess
import sys
import refine
import time
import signal
import shutil
sys.path.append("refine.py")


def strip(x): return x.strip()


def split(x): return x.split("\t")


def encode(x): return x.encode("utf-8")


# Check if the metadata file path was given as an argument otherwise take it from input
arguments = sys.argv

if len(arguments) == 1:
    while True:
        metadata_path = raw_input("Give the name or path of the metadata file. or type exit"
                                  "\nPlease note, that the metadata file should have two directories"
                                  " (experiment and sample):\n")
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

# storing the names of the directories and files in lists
metadata_files = []
directories = []
for root, dirs, files in os.walk(metadata_path):
    for f in files:
        metadata_files.append(os.path.join(root, f))
    for d in dirs:
        directories.append(os.path.join(root, d))

#####################################################################################################
# copying all files to work on them, then output the results in a separate
# folder and delete the intermediate copy folder
if metadata_path.endswith(os.sep):
    metadata_cp, sep, tail = metadata_path.rpartition(os.sep)
    metadata_cp = metadata_cp + "_cp" + os.sep
else:
    metadata_cp = metadata_path + "_cp"

if not os.path.exists(metadata_cp):
    os.makedirs(metadata_cp)
    for directory in directories:
        os.makedirs(directory.replace(metadata_path, metadata_cp))
        # print directory.replace(metadata_path, metadata_cp)

        
"""
looping through the files.
I separated the several tasks (removing empty lines, fixing encoding, removing extra spaces and so on) To 3 functions
(lines_fixer1, lines_fixer2 and experiment_id) This way it's easier to catch the errors and trouble shoot any problem.

Also I saved the keys of the original files separately for later filtering after merging all the files together.

I'm reading each file once and looping through the lines
"""

all_files_keys = []  # storing the unique keys from all the files to make the big table
             
skipped_files = {}  # storing any file that is not in (key value) tsv format

for f in metadata_files:
    lines = read_files(file_name=f)  # function for reading the files with the correct encoding
    
    # checking if the file is actually in (key value) tsv format, otherwise the file will be skipped
    if check_if_tsv(lines):
        new_lines = lines_fixer1(lines)  # First round of fixes
        new_lines = lines_fixer2(new_lines)  # Second round of fixes
        if f.endswith("emd.tsv"):
            new_lines = experiment_id_fix(new_lines, f)  # This function checks if the experiment_id is correct
        else:
            new_lines = deep_sample_id_fix(new_lines, f)  # This function checks if the sample_id is correct

        keys = []  # storing the keys for later filtering
        for l in new_lines:
            keys.append(l.split("\t")[0])
        
        for k in keys:
            if k in all_files_keys:	 # making a list of all the unique keys of all the files
                pass
            else:
                all_files_keys.append(k)

        f_write = open(f.replace(metadata_path, metadata_cp), "w+")  # writing the fixed files
        for l in new_lines:
            f_write.write(l.encode('utf-8') + '\n')
        f_write.close()
    else:
        skipped_files[f] = check_if_tsv(lines)    
    
# remove skipped files before further analysis
if len(skipped_files) != 0:
    for f in skipped_files:
        metadata_files.remove(f)
###########################################################################

# combine the experiment files and sample files each to one table to process with the JSON operations using OpenRefine
# new_files_table = []  # Table of all experiments
new_files_table = merge_files(metadata_files, all_files_keys, metadata_path)
w = open("all_files_table.tsv", "w+")
for l in new_files_table:
    w.write(l.encode("utf-8")+"\n")
w.close()

###########################################################################
# giving the tables to Openrefine with the JSON operations
# we need to start OpenRefine first in the background to use it
# We need to start with subprocess and store the ID to kill it later
# todo for linux use subprocess.Popen, not sure what to use for windows

current_dir = os.getcwd()
script_dir = os.sep.join(os.path.realpath(__file__).split(os.sep)[:-1])
os.chdir(script_dir)
if "win" in sys.platform:
    open_refine = subprocess.Popen(os.path.join("openrefine-2.8", "openrefine.exe"))
else:
    open_refine = subprocess.Popen(os.path.join("openrefine-2.7-rc.1", ".", "refine"),
                                   stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

print "starting OpenRefine:",
for i in ["1"]*7:
    print "."
    time.sleep(float(i))

r = refine.Refine()
p = r.new_project("all_files_table.tsv")
p.apply_operations("operations.json")
after_json_experiment_table = p.export_rows()
p.delete_project()

after_json_experiment_table = after_json_experiment_table.split("\n")
    

if after_json_experiment_table[-1] == "":
    del after_json_experiment_table[-1]

os.chdir(current_dir)
w = open("after_refine_table.tsv", "w+")
for l in after_json_experiment_table:
    w.write(l + "\n")
w.close()

os.killpg(os.getpgid(open_refine.pid), signal.SIGTERM)  # Send the signal to all the process groups
# also open_refine.kill is not working

# splitting the table after REFINE to individual files
if metadata_path.endswith(os.sep):
    metadata_json, sep, tail = metadata_path.rpartition(os.sep)
    metadata_json = metadata_json + "_after_refine" + os.sep
else:
    metadata_json = metadata_path + "_after_refine" + os.sep
    

if not os.path.exists(metadata_json):
    os.makedirs(metadata_json)
    for directory in directories:
        os.makedirs(directory.replace(metadata_path, metadata_json))
        
table_to_files2(after_json_experiment_table, metadata_path)


if os.path.exists(metadata_json):
    shutil.rmtree(metadata_cp)	

# report skipped files
if len(skipped_files) != 0:
    for f in skipped_files:
        print("The file ({}) was skipped because the line(s) ({}) "
              "in it are not in a key \\t value format".format(f, skipped_files[f]))

if os.path.exists("after_refine_table.tsv"):
    os.remove("after_refine_table.tsv")
if os.path.exists("all_files_table.tsv"):
    os.remove("all_files_table.tsv")
