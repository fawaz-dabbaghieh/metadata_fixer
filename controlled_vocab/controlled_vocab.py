#!/usr/bin/python

##################################################################################

# This pipeline is used to to check metadata files belong to the DEEP project
# To check for controlled vocabulary and for accepted values and keys

##################################################################################

from optparse import OptionParser
import sys
import re
import os
import codecs
from dictionary_functions import *		#an acompanied python file with functions needed to process the files

def strip(x): return x.strip()
def encode(x): return x.encode("utf-8")

#Check if no arguments were given, print message
if sys.argv[1:] == []:
    print "No Arguments were given, please try -h or --help"
    sys.exit()


#Arguments parser
parser = OptionParser()
parser.add_option("-f","--file",dest="filename",help="The name of the file to be processed by the pipeline", metavar="FILE")

parser.add_option("-l","--list",dest="list_file",help="name or path to a file, containing list of files to be processed", metavar="FILES_LIST")

parser.add_option("-d","--directory",dest="dir_path",help="name or path of the directory containing files to be processed", metavar="PATH")

parser.add_option("-v","--verbose",dest="verbose",action="store_true", default=False,help="To turn on Verbose")

parser.add_option("-k","--key", dest="key", help="Shows the accepted values for the key given by user",metavar="KEY")

parser.add_option("--list_keys", dest="list_keys", action="store_true",default=False,help="List all keys in dictionary")

parser.add_option("--list_regex", dest="list_regex", action="store_true",default=False,help="List all regular expression that are controlled with examples")

(options, args) = parser.parse_args()
filename = options.filename
list_file = options.list_file
dir_path = options.dir_path
verbose = options.verbose
key_from_user = options.key


#loading the dictionaries, we have 3 dictionaries, one for experiments metadata, one for samples and one for the regular expression to check for
#So I made a dict of dicts to have all three and work with them and be able to call them
#TODO change the way the dictionaries are read
dictionaries = {"samples_dictionary": {}, "experiments_dictionary": {},"regex_dictionary": {}}

for k in dictionaries.keys():
    if os.path.exists(k + ".tsv"):
        dictionaries[k] = read_dictionary(k + ".tsv")
    else:
        print("Was not able to load the ({})".format(k))
    
    
#for idx, l in enumerate(dictionaries):
	#if os.path.exists(l):
		#f = open(l, "r")
		#dictionaries[idx] = pickle.load(f)
		#f.close()
	#else:
		#print("The dictionary file has either not been built or it is not in this directory")
		#sys.exit()


#checking the file from option -f --file
if filename is not None:
    if os.path.exists(filename):
        if verbose == True:
            check_vobac_verbose(filename, dictionaries)
        else:

            check_vocab(filename, dictionary)
    else:
            print("the path ({}) you gave is not correct, please check it again".format(options.filename))
            sys.exit()



#checking the file from option -l --list
if list_file is not None:
    if os.path.exists(list_file):
        files = read_files(list_file)
        files = map(strip,files)
        
        for f in files:
            if verbose == True:	#for verbose
                print f + "\n"
                check_vobac_verbose(f, dictionaries)

            else:	#for not verbose
                print f + "\n"
                chech_vocab(f, dictionaries)

    else:
        print("the path ({}) you gave for a list of files is not correct, please check it again".format(list_file))
        sys.exit()


#checking the file from option -d --directory
if dir_path is not None:
    if not dir_path.endswith("/"):		#adding a slash to the directory name in case it was forgotten
        dir_path = dir_path + "/"

    if os.path.exists(dir_path):
        data_files = []
        for root, dirs, files in os.walk(dir_path):	#Checking the directory and sub direcotory recursively and listing all files
            for f in files:
                if f.endswith("emd.tsv") or f.endswith("smd.txt"):
                    data_files.append(os.path.join(root, f))

        for f in data_files:
            lines = read_files(f)
            lines = map(strip,lines)
            lines = map(encode, lines)
            if verbose == True:
                print f + "\n"
                check_vocab_verbose(f, dictionaries)

            else:
                print f + "\n"
                check_vocab(f, dictionaries)

    else:
        print("the path ({}) you gave is not correct, please check it again".format(dir_path))	


#checking the file from option -k --key
if key_from_user is not None:
    if key_from_user in dictionaries["samples_dictionary"].keys():
        print dictionaries["samples_dictionary"][key_from_user]

    elif key_from_user in dictionaries["experiments_dictionary"].keys():
        print dictionaries["experiments_dictionary"][key_from_user]

    elif key_from_user in dictionaries["regex_dictionary"].keys():
        print dictionaries["regex_dictionary"][key_from_user]

    else:
        print("The key ({}) you entered is not one of the dictionary keys".format(key_from_user))

#checking the file from option --list_keys
if options.list_keys is True:
    list_keys = ["####################		samples metadata keys		####################\n"]
    for k in dictionaries["samples_dictionary"].keys():
        list_keys.append(k)
    
    list_keys.append("\n####################		experiments metadata keys		####################\n")
    for k in dictionaries["experiments_dictionary"].keys():
        list_keys.append(k)
        
        
    list_keys = map(encode, list_keys)
    print "\n".join(list_keys)


#listing regular expression available
if options.list_regex is True:
    for k in dictionaries["regex_dictionary"]:
        print k
        print dictionaries["regex_dictionary"][k]