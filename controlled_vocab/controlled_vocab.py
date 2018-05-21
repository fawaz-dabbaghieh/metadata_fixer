#!/usr/bin/python

##################################################################################

# This pipeline is used to to check metadata files belong to the DEEP project
# To check for controlled vocabulary and for accepted values and keys

##################################################################################

from optparse import OptionParser
import sys
from dictionary_functions import *  # an accompanied python file with functions
from dicttoxml import dicttoxml


def strip(x): return x.strip()


def encode(x): return x.encode("utf-8")


# Check if no arguments were given, print message
if not sys.argv[1:]:
    print "No Arguments were given, please try -h or --help"
    sys.exit()

# Arguments parser
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="The name of the file to be processed by the pipeline",
                  metavar="FILE")

parser.add_option("-l", "--list", dest="list_file",
                  help="name or path to a file, containing list of files (line separated) to be processed",
                  metavar="FILES_LIST")

parser.add_option("-d", "--directory", dest="dir_path",
                  help="name or path of the directory containing files to be processed", metavar="PATH")

parser.add_option("-v", "--verbose", dest="verbose",
                  action="store_true", default=False, help="To turn the Verbose mode on")

parser.add_option("-k", "--key", dest="key", help="Shows the accepted values for the key given by user",
                  metavar="KEY")

parser.add_option("--list_keys", dest="list_keys", action="store_true", default=False,
                  help="List all keys in dictionary")

parser.add_option("--list_regex", dest="list_regex", action="store_true", default=False,
                  help="List all regular expression that are controlled with examples")

(options, args) = parser.parse_args()
filename = options.filename
list_file = options.list_file
dir_path = options.dir_path
verbose = options.verbose
key_from_user = options.key

"""
Loading dictionaries, we have 3 dictionaries (experiments, samples and regular expressions),
the first two are made by running the build_dictionary.py first to build dictionaries from a set of files,
the regular expression dictionary is "hard coded" 
according to the keys that we agreed that have to be checked for regular 
expression, all dictionaries are in .tsv format and can be opened and editted easily,
so new keys and value can be added to these dictionaries.
"""

dictionaries = {"samples_dictionary": {}, "experiments_dictionary": {}, "regex_dictionary": {}}

for k in dictionaries.keys():
    if os.path.exists(k + ".tsv"):
        dictionaries[k] = read_dictionary(k + ".tsv")
    else:
        print("The ({}) dictionary was not loaded, please run (build_dictionary.py) first"
              " to build a dictionary from the files".format(k))
        sys.exit()

# checking the file from option -f --file
if filename is not None:
    if os.path.exists(filename):
        if verbose:
            report_dict = {}
            report = check_vocab_verbose(filename, dictionaries, report_dict)
            
        else:
            report_dict = {}
            report = check_vocab(filename, dictionaries, report_dict)
    else:
            print("the path ({}) you gave was not found, please check it again".format(options.filename))
            sys.exit()
            
    report_xml = dicttoxml(report, custom_root="filesCheckReport", attr_type=True)
    w = open("report.xml", "w+")
    w.write(report_xml)
    w.close()

# checking the file from option -l --list
if list_file is not None:
    if os.path.exists(list_file):
        files = read_files(list_file)
        files = map(strip, files)
        
        report_dict = {}
        for f in files:
            if verbose:  # for verbose
                report_dict = check_vocab_verbose(f, dictionaries, report_dict)

            else:  # for not verbose
                report_dict = check_vocab(f, dictionaries, report_dict)

    else:
        print("the path ({}) you gave for a list of files is not correct, please check it again".format(list_file))
        sys.exit()
        
    report_xml = dicttoxml(report_dict, custom_root="filesCheckReport", attr_type=False)
    w = open("report.xml", "w+")
    w.write(report_xml)
    w.close()

# checking the file from option -d --directory
if dir_path is not None:
    if not dir_path.endswith(os.sep):  # adding a sep to the directory name in case it was forgotten
        dir_path = dir_path + os.sep

    if os.path.exists(dir_path):
        data_files = []
        # Checking the directory and sub directory recursively and listing all files
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if f.endswith("emd.tsv") or f.endswith("smd.txt"):
                    data_files.append(os.path.join(root, f))

        report_dict = {}
        for f in data_files:
            lines = read_files(f)
            lines = map(strip, lines)
            lines = map(encode, lines)
            if verbose:
                report_dict = check_vocab_verbose(f, dictionaries, report_dict)

            else:
                report_dict = check_vocab(f, dictionaries, report_dict)

    else:
        print("the path {} you gave is not correct, please check it again".format(dir_path))
        sys.exit()

    report_xml = dicttoxml(report_dict, custom_root="filesCheckReport", attr_type=False)
    w = open("report.xml", "w+")
    w.write(report_xml)
    w.close()

# checking the file from option -k --key
if key_from_user is not None:
    if key_from_user in dictionaries["samples_dictionary"].keys():
        print dictionaries["samples_dictionary"][key_from_user]

    elif key_from_user in dictionaries["experiments_dictionary"].keys():
        print dictionaries["experiments_dictionary"][key_from_user]

    elif key_from_user in dictionaries["regex_dictionary"].keys():
        print dictionaries["regex_dictionary"][key_from_user]

    else:
        print("The key ({}) you entered is not one of the dictionary keys".format(key_from_user))

# checking the file from option --list_keys
if options.list_keys is True:
    list_keys = ["####################		samples metadata keys		####################\n"]
    for k in dictionaries["samples_dictionary"].keys():
        list_keys.append(k)
    
    list_keys.append("\n####################		experiments metadata keys		####################\n")
    for k in dictionaries["experiments_dictionary"].keys():
        list_keys.append(k)

    list_keys = map(encode, list_keys)
    print "\n".join(list_keys)


# listing regular expression available
if options.list_regex is True:
    for k in dictionaries["regex_dictionary"]:
        print k
        print dictionaries["regex_dictionary"][k]
