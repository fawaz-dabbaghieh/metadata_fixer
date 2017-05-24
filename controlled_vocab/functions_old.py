#!/usr/bin/python

import codecs

def strip(x): return x.strip()
def split(x): return x.split("\t")

#def check_values(lines, keys):
#	lines = map(strip, lines)
#	lines = map(split, lines)
#	print lines


#####
def make_dic(keys, files):                
    dic = {}
    for key in keys:
        dic[key] = []
        for f in files:
            f = codecs.open(f, encoding = "utf-8")
            lines = f.readlines()
            f.close()
            lines = map(strip,lines)
            for l in lines:
                if l.split("\t")[0] == key:
                    dic[key].append(l.split("\t")[1])
                else:
                    continue
    for k in dic:
        dic[k] = set(dic[k])
	dic[k] = list(dic[k])
    return dic


dic = {}

f = codecs.open("all_keys.txt", encoding = "utf-8-sig")
keys = f.readlines()
keys = map(strip, keys)
f.close()

for key in keys:
	f = codecs.open(key, encoding = 'utf-8-sig')
	values = f.readlines()
	f.close()
	values = map(strip, values)
	dictionary[key] = values

f = codecs.open("43_Hm05_BlMa_TE_smd.txt", encoding = "utf-8-sig")
lines = f.readlines()
f.close()

check_values(lines = lines, keys = keys)


##writing and reading a dictionary
import pickle

w = open("output.txt", "ab+")
pickle.dump(dictionary, w)
w.close()

f = open("output.txt", "rb")
dictionary = pickle.load(output)

##Check Vocab
def check_vocab(lines, dictionary):
    for l in lines:
        l = l.split("\t")
        if l[0] in dictionary.keys():
            if l[1] in dictionary[l[0]]:
                continue
            else:
                print "Warning! the value ("+l[1]+") in key ("+l[0]+") is not in the controlled vocabulary"

