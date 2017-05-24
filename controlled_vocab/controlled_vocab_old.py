#!/usr/bin/python

import codecs
import pickle
import os


def strip(x): return x.strip()
def encode(x): return x.encode("utf-8")

def check_vocab(lines, dictionary):
    for idx, l in enumerate(lines):
        l = l.split("\t")
        if l[0] in dictionary.keys():
            if l[1] in dictionary[l[0]]:
                print l
		print "\t Is OK\n"

            else:
                print "\nWarning! the value ("+l[1]+") in key ("+l[0]+") is not in the controlled vocabulary\n"

        elif l == ['']:
            print "Line %s is empty" %idx

        else:
            print l
            print "Warning! the Key ("+ l[0] + ") is not one of the dictionary keys"


while True:
	f_name = raw_input("Please give the path for the file you want to check: ")

	if os.path.exists(f_name):
		break
	else:
		print("\nThe path to the file is not correct or does not exists\nPlease try again\n")

f = codecs.open(f_name, encoding = "utf-8")
lines = f.readlines()
f.close()
lines = map(strip,lines)
lines = map(encode, lines)

d = open("dictionary.txt", "rb")
dictionary = pickle.load(d)
d.close()

check_vocab(lines = lines, dictionary = dictionary)

