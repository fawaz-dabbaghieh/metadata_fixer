#!/usr/bin/python

import codecs
import os
import subprocess
import sys
import re
import pickle
import time
import signal
import shutil

def split(x): return x.split("\t")
def strip(x): return x.strip()
############################################################################################
#This functions will try 3 different kinds of encodings
#once codecs reads the file in the write encoding
#it will be read as un-encoded lines with u'' at the beginning
#this way when I write them back, I can encode them as utf-8

def read_files(file_name):
    encodings = ['utf-8-sig','iso-8859-1', 'utf-16']
    if os.path.exists(file_name):
        for e in encodings:
            try:
                f = codecs.open(file_name, 'r', encoding=e)
                lines = f.readlines()
                f.close()
            except UnicodeError:
                print('got unicode error with %s , trying different encoding' % e)
            else:
                #print('opening the file with encoding:  %s ' % e)
                break
    else:
        print file_name
        print "the path {} does not exist".format(file_name)
        
    return lines


############################################################################################
#removing a space from the key column in case there was
def remove_space_in_key(lines):
    for idx, l in enumerate(lines):
        l = l.split("\t")
        if " " in l[0]:
            l[0] = l[0].replace(" ", "_")
            lines[idx] = "\t".join(l)
        else:
            lines[idx] = "\t".join(l)
    return lines


#removing empty lines
def remove_empty_lines(lines):
    for l in list(lines):
        if l == u'\n':
            lines.remove(u'\n')
    return lines

############################################################################################
#remove encoding error characters (after checking these two are appearing when the file is
#wrongly encoded
#\u017d and \xc2
def remove_encoding_errors(lines):
    for idx, l in enumerate(lines):
        if u'\u017d' or u'\xc2' in l:
            lines[idx] = (l.replace(u'\u017d', '')).replace(u'\xc2', '')
    return lines


############################################################################################
#Check for duplicate keys
def duplicate_keys(lines):
    keys = []
    duplicates = []
    for idx, l in enumerate(lines):
        if l.split("\t")[0] in keys:
            duplicates.append(idx)
        else:
            keys.append(l.split("\t")[0])
    if len(duplicates) != 0:
        for d in duplicates:
            lines[d] = lines[d].split("\t")
            lines[d][0] = lines[d][0] + "_1"
            lines[d] = "\t".join(lines[d])
    return lines
############################################################################################
#Adding Experiment ID to the files
#Check if experiment id is there and if it's correctly written, other wise fix it or add it
def experiment_id_fix(lines, file_name):
    #checking if EXPERIMENT_ID exists
    experiment_id = file_name.split("/")[-1].replace("_emd.tsv", "")
    
    if any("EXPERIMENT_ID" in s for s in lines):    #check if the keys EXPERIMENT_ID exists otherwise added it
        for idx,l in enumerate(lines):
            if l.startswith("EXPERIMENT_ID"):
                if re.search("^\d{2}_\w+_\w+_\w+_\w+_[A-Z]_[0-9]$", l.split("\t")[1]):
                    pass
                else:
                    try:
                        experiment_id = re.search("^\d{2}_\w+_\w+_\w+_\w+_[A-Z]_[0-9]$", experiment_id)
                        lines[idx] = "EXPERIMENT_ID" + "\t" + experiment_id
                    except AttributeError:
                        print("WARNING!! the file {} doesn't fit the naming template. Please, check if something missing in the name").format(file_name)
    else:
        try:
            experiment_id = re.search("^\d{2}_\w+_\w+_\w+_\w+_[A-Z]_[0-9]$", experiment_id).group()
            experiment_id = "EXPERIMENT_ID" + "\t" + experiment_id
            lines.append(experiment_id)
        except AttributeError:
            print("WARNING!! the file {} doesn't fit the naming template. Please, check if something missing in the name").format(file_name)

    return lines

############################################################################################
#fixing the SAMPLE_ID in case it was simmilar to the DEEP_SAMPLE_ID
def deep_sample_id_fix(lines, file_name):
    #checking if DEEP_SAMPLE_ID exists
    deep_sample_id = file_name.split("/")[-1]
    deep_sample_id = re.sub("_smd.txt$", "", deep_sample_id) #removing _emd.tsv from the file name
    
    if any("DEEP_SAMPLE_ID" in s for s in lines):    #check if the keys DEEP_SAMPLE_ID exists
        for idx,l in enumerate(lines):
            if l.startswith("DEEP_SAMPLE_ID"):
                if re.search("^\d{2}_\w+_\w+_\w+$", l.split("\t")[1]):
                    pass
                else:
                    try:
                        deep_sample_id = re.search("(^\d{2}_\w+_\w+_\w+)_\w+_[A-Z]_[0-9]$", deep_sample_id)
                        lines[idx] = "DEEP_SAMPLE_ID" + "\t" + deep_sample_id
                    except AttributeError:
                        print("WARNING!! the DEEP_SAMPLE_ID in file {} doesn't fit the naming template. Please, check if something missing").format(file_name)
    else:
        try:
            deep_sample_id = re.search("^\d{2}_\w+_\w+_\w+$", deep_sample_id).group()
            deep_sample_id = "DEEP_SAMPLE_ID" + "\t" + deep_sample_id
            lines.append(deep_sample_id)
        except AttributeError:
            print("WARNING!! the DEEP_SAMPLE_ID in file {} doesn't fit the naming template. Please, check if something missing").format(file_name)

    return lines


############################################################################################
#checks line start and append to previous if it does not start with a key
def check_line_start(line):
    starts = ["5".decode('UTF-8', 'ignore'),"CGC".decode('UTF-8', 'ignore'),"HCS".decode('UTF-8', 'ignore'),"Julia".decode('UTF-8', 'ignore'),"Rep".decode('UTF-8', 'ignore'),"http".decode('UTF-8', 'ignore')]
    for s in starts:
        if line.startswith(s): return True
    return False

    
############################################################################################
#returning a list of all the lines of a file
def lines_fixer1(lines):
    lines = remove_space_in_key(lines)
    new_lines = []
    appended_lines = 1
    for (idx, l) in enumerate(lines):
        l = l.strip()
        if check_line_start(l):
                previous_line = new_lines[idx - appended_lines]
                new_lines[idx - appended_lines] = previous_line + " " + l
                appended_lines = appended_lines + 1
                continue

        s = l.split()
        if len(s) == 1:
                key = s[0]
                value = "[MISSING]"
                new_line = [key, value]
                new_line = "\t".join(new_line)
                new_lines.append(new_line)

        else:
            try:
                key = s[0]
                value = " ".join(s[1:])
                new_line = [key, value]
                new_line = "\t".join(new_line)
                new_lines.append(new_line)
            except IndexError:
                continue

                
    return new_lines

############################################################################################
def lines_fixer2(new_lines1):
    new_lines2 = remove_encoding_errors(new_lines1)
    new_lines2 = duplicate_keys(new_lines2)
    return new_lines2

############################################################################################

def check_if_tsv(lines):
    wrong_lines = []
    for idx, l in enumerate(lines):
        if len(l.split("\t")) == 2:
            continue
        else:
            wrong_lines.append(idx)
    if wrong_lines == []:
        return True
    else:
        return False
############################################################################################
#returning the value that corresponds to key
def return_value(key, lines):
    value = "[[[Extra Key Introduced]]]"
    for l in lines:
        if key in l:
            value = l[1]
        else:
            continue
    return value


def merge_files(files_list, all_keys, metadata_path):
    all_keys.append("FILE_NAME")
    
    #making the tsv table
    new_table = []
    new_table.append("\t".join(all_keys))	#First line is the keys
    
    if metadata_path.endswith("/"):
        metadata_cp = metadata_path.replace("/", "_cp/")
    else:
        metadata_cp = metadata_path + "_cp"  
    
    for f in files_list:
        lines = read_files(f.replace(metadata_path, metadata_cp))
        lines.append("FILE_NAME\t"+f)
        lines = map(split, lines)
        
        new_file = []
        for key in all_keys:
            value = return_value(key = key, lines = lines)
            new_file.append(value)
        new_file = map(strip, new_file)
        new_file = "\t".join(new_file)
        new_table.append(new_file)
    
    return new_table


############################################################################################
#keys filtering
def filtering_keys(original_keys, new_file):
    new_filtered_file = []
    for i in range(0,len(original_keys)):
        for l in new_file:
            if l.split("\t")[0] == original_keys[i]:
                new_filtered_file.append(l)
    return new_filtered_file
    

#converting back the big table to individual tsv files and filtering against the original keys
def table_to_files1(lines, i):
    keys = lines[0].strip().split("\t")
    values = lines[i].split("\t")
    new_file = []
    for j in range(0,len(keys)):
        new_line = keys[j] + "\t" + values[j]
        new_file.append(new_line)
    return new_file


def table_to_files2(lines ,metadata_path):
    if metadata_path.endswith("/"):
        metadata_json = metadata_path.replace("/", "_after_refine/")
    else:
        metadata_json = metadata_path + "_after_refine"
        
    if metadata_path.endswith("/"):
        metadata_cp = metadata_path.replace("/", "_cp/")
    else:
        metadata_cp = metadata_path + "_cp"    
    
    keys = lines[0].split("\t")
        
    file_name_idx = len(keys) -1

    for i in range(1,len(lines)):
        
        file_name = lines[i].split("\t")[file_name_idx].replace(metadata_path,metadata_json)
        f_write = open(file_name, "w+")
        new_file = table_to_files1(lines, i)
        
        #filter here before writing
        original_keys_f = open(file_name.replace(metadata_json,metadata_cp) + "keys")
        original_keys = pickle.load(original_keys_f)
        original_keys_f.close()
        new_filtered_file = filtering_keys(original_keys, new_file)
        for l in new_filtered_file:
            f_write.write(l + "\n")
        f_write.close()
