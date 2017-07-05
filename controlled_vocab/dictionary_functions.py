import os
import codecs
import sys
import re

def strip(x): return x.strip()
def encode(x): return x.encode("utf-8")
def split(x): return x.split("\t")

###########################################################################################################################
#reading files Function
#This will try different encodings, if it tries the wrong encoding it should give a UnicodeError
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

###########################################################################################################################
#Function to check for controlled vocabluary, verbose version which will print everything (OK lines and warning lines)
#TODO change the worning schema and store the warnings in an XML file, so it will be easier to read the report
def check_vocab_verbose(metadata_file, dictionaries):
    lines = read_files(metadata_file)
    lines = map(strip, lines)
    lines = map(encode, lines)
    lines = map(split, lines)
    if metadata_file.endswith("emd.tsv"):
        for l in lines:
                if l[0] in dictionaries["regex_dictionary"].keys():	#check if the key belongs to the regex then check the value if it fits the regex
                    
                    if re.search(dictionaries["regex_dictionary"][l[0]][0], l[1]):
                        print "\t".join(l)
                        print "\tAccepted"
                    else:
                        print("\nWarning! the value ({}) in key ({}) in file ({}) doesn't follow the accepted template").format(l[1], l[0], metadata_file)
                        print("\nWarning! the value ({}) in key ({}) don't comply with the templte which is ({})").format(l[1], l[0], dictionaries["regex_dictionary"][l[0]][1])
                elif l[0] in dictionaries["samples_dictionary"].keys():	#If the key is not from regex, check if it's a white list
                    if l[1] in dictionaries["samples_dictionary"][l[0]]:
                        print "\t".join(l)
                        print "\tAccepted"
                    else:
                        print("\n Warning! the value ({}) in key ({}) in line ({}) is not in the controlled vocabulary\n\n").format(l[1], l[0], metadata_file)
                else:					#if it's not regex nor white list then it's a balck list and can be left as it is
                    pass



    elif metadata_file.endswith("smd.txt"):
        for l in lines:
            if l[0] in dictionaries["regex_dictionary"].keys():	#check if the key belongs to the regex then check the value if it fits the regex
                if re.search(dictionaries["regex_dictionary"][l[0]][0], l[1]):
                    print "\t".join(l)
                    print "\tAccepted"
                else:
                    print("\nWarning! the value ({}) in key ({}) in file ({}) doesn't follow the remplate accepted").format(l[1], l[0], metadata_file)
                    print("\nWarning! the value ({}) in key ({}) don't comply with the templte which is ({})").format(l[1], l[0], dictionaries["regex_dictionary"][l[0]][1])
            elif l[0] in dictionaries["samples_dictionary"].keys():	#If the key is not from regex, check if it's a white list
                if l[1] in dictionaries["samples_dictionary"][l[0]]:
                    print "\t".join(l)
                    print "\tAccepted"
                else:
                    print("\nWarning! the value ({}) in key ({}) in line ({}) is not in the controlled vocabulary\n\n").format(l[1], l[0], metadata_file)
            else:					#if it's not regex nor white list then it's a balck list and can be left as it is
                pass


###########################################################################################################################
#Function to check for controlled vocabluary, only prints warning lines
def check_vocab(metadata_file, dictionaries):
    f = codecs.open(metadata_file, encoding = "utf-8-sig")
    lines = f.readlines()
    f.close()
    lines = map(strip, lines)
    lines = map(encode, lines)
    lines = map(split, lines)
    if metadata_file.endswith("emd.tsv"):
        for l in lines:
            if l[0] in dictionaries["regex_dictionary"].keys():	#check if the key belongs to the regex then check the value if it fits the regex
                if re.search(dictionaries["regex_dictionary"][l[0]][0], l[1]):
                    pass
                else:
                    print("\nWarning! the value ({}) in key ({}) in file ({}) doesn't follow the accepted template").format(l[1], l[0], metadata_file)
                    print("\nWarning! the value ({}) in key ({}) don't comply with the templte which is ({})").format(l[1], l[0], dictionaries["regex_dictionary"][l[0]][1])
            elif l[0] in dictionaries["experiments_dictionary"].keys():	#If the key is not from regex, check if it's a white list
                if l[1] in dictionaries["experiments_dictionary"][l[0]]:
                    pass
                else:
                    print("\n Warning! the value ({}) in key ({}) in line ({}) is not in the controlled vocabulary\n\n").format(l[1], l[0], metadata_file)
            else:					#if it's not regex nor white list then it's a balck list and can be left as it is
                pass



    elif metadata_file.endswith("smd.txt"):
        for l in lines:
            if l[0] in dictionaries["regex_dictionary"].keys():	#check if the key belongs to the regex then check the value if it fits the regex
                if re.search(dictionaries["regex_dictionary"][l[0]][0], l[1]):
                    pass
                else:
                    print("\nWarning! the value ({}) in key ({}) in file ({}) doesn't follow the remplate accepted").format(l[1], l[0], metadata_file)
                    print("\nWarning! the value ({}) in key ({}) don't comply with the templte which is ({})").format(l[1], l[0], dictionaries["regex_dictionary"][l[0]][1])
            elif l[0] in dictionaries["samples_dictionary"].keys():	#If the key is not from regex, check if it's a white list
                if l[1] in dictionaries["samples_dictionary"][l[0]]:
                    pass
                else:
                    print("\nWarning! the value ({}) in key ({}) in line ({}) is not in the controlled vocabulary\n\n").format(l[1], l[0], metadata_file)
            else:					#if it's not regex nor white list then it's a balck list and can be left as it is
                pass


###########################################################################################################################
#A third way to build the dictionary
def build_dic(all_keys, files):
    dic = {}
    for key in all_keys:
        dic[key] = []

    for f in files:
        lines = read_files(f)
        lines = map(strip, lines)	# get rid of any white spaces of new lines at the end of each line
        lines = map(encode, lines)	# encode the lines as utf-8, it makes it easier for comparison later
        lines = map(split, lines)	# split each lines to ["key", "value"]

        for l in lines:	#if the value is already in the dictionary do nothing, otherwise add that value to the dictionaryLiam Gallagher
            if l[0] in dic.keys():  #check if the keys of the line is one of the controlled vocabulary keys
                if l[1] not in dic[l[0]]:   #Check if the value is in the dictionary otherwise add it
                    dic[l[0]].append(l[1])
    return dic

###########################################################################################################################
#getting a list of keys
def list_keys(files, regex_keys, black_keys):
    keys = []
    for f in files:
        lines = read_files(f)
        lines = map(encode, lines)
        lines = map(split, lines)
        for l in lines:
            if l[0] in regex_keys:
                pass
            elif l[0] in black_keys:
                pass
            elif l[0] not in keys:
                keys.append(l[0])

    return keys

###########################################################################################################################
#writing a dictionary as a tsv file so it can be human readabel, editable and addable
#This w

def write_dictionary(dictionary, output_name):
    dict_as_lines = []
    for k in dictionary.keys():
        if type(dictionary[k]) == list:                 #It will be a list if there was more than one value for the key
            dictionary[k] = "\t".join(dictionary[k])
            dict_as_lines.append(k+"\t"+dictionary[k])
        else:                                           #otherwise the value for the 
            dict_as_lines.append(k+"\t"+dictionary[k])

    f = open(output_name, "w+")
    for l in dict_as_lines:
        f.write(l+"\n")
    f.close()
    
    
###########################################################################################################################
#Read a dictionary written in tsv foramt
#Take the first element as the key and the rest are values
def read_dictionary(file_name):
    lines = read_files(file_name)
    lines = map(strip, lines)
    
    dictionary = {}
    for l in lines:
        l = l.encode("utf-8")   #TODO check if it needs to be encoded or not
        dictionary[l.split("\t")[0]] = l.split("\t")[1:]
    
    return dictionary