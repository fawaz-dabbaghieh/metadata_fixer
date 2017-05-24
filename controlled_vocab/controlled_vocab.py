#!/usr/bin/python

##################################################################################

# This pipeline is used to to check metadata files belong to the DEEP project
# To check for controlled vocabulary and for accepted values and keys

##################################################################################

from optparse import OptionParser
import sys
import os
import codecs
import pickle
import functions

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

(options, args) = parser.parse_args()
filename = options.filename
list_file = options.list_file
dir_path = options.dir_path
verbose = options.verbose
key_from_user = options.key


#loading the dictionary
if os.path.exists("dictionary.txt"):
	dic = open("dictionary.txt", "r+")
	dictionary = pickle.load(dic)
	dic.close()
else:
	print("The dictionary file has either not been built or is not in this directory")
	sys.exit()

#checking the file from option -f --file
if filename is not None:
	if os.path.exists(filename):
		f = codecs.open(filename, encoding = "utf-8-sig")
		lines = f.readlines()
		f.close()
		lines = map(strip,lines)
		lines = map(encode, lines)
		if verbose == True:
			print filename + "\n"
			functions.check_vocab_verbose(lines = lines, dictionary = dictionary)
		else:
			print filename + "\n"
			functions.check_vocab(lines = lines, dictionary = dictionary)
	else:
		print("the path ({}) you gave is not correct, please check it again".format(options.filename))
		
#checking the file from option -l --list
if list_file is not None:
	if os.path.exists(list_file):
		f = open(list_file, "r+")
		files = f.readlines()
		f.close()
		files = map(strip,files)
		for f in files:
			read = codecs.open(f, encoding = "utf-8-sig")
			lines = read.readlines()
			read.close()
			lines = map(strip,lines)
			lines = map(encode, lines)
			if verbose == True:
				print f + "\n"
				functions.check_vocab_verbose(lines = lines, dictionary = dictionary)
			else:
				print f + "\n"
				functions.check_vocab(lines = lines, dictionary = dictionary)
	else:
		print("the path ({}) you gave is not correct, please check it again".format(list_file))


#checking the file from option -d --directory
if dir_path is not None:
	if os.path.exists(dir_path):
		files = os.listdir(dir_path)
		files = [l for l in files if l.endswith("smd.txt") or l.endswith("emd.tsv")]
		files = map(strip,files)
		for f in files:
			read = codecs.open(dir_path+"/"+f, encoding = "utf-8-sig")
			lines = read.readlines()
			read.close()
			lines = map(strip,lines)
			lines = map(encode, lines)
			if verbose == True:
				print f + "\n"
				functions.check_vocab_verbose(lines = lines, dictionary = dictionary)
			else:
				print f + "\n"
				functions.check_vocab(lines = lines, dictionary = dictionary)
	else:
		print("the path ({}) you gave is not correct, please check it again".format(dir_path))	

#checking the file from option -k --key
if options.key is not None:
	if options.key in dictionary.keys():
		print dictionary[key_from_user]
	else:
		print("The key ({}) you entered is not one of the dictionary keys".format(key_from_user))

#checking the file from option --list_keys
if options.list_keys is True:
	list_keys = dictionary.keys()
	list_keys = map(encode, list_keys)
	print list_keys
