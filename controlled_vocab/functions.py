import os
import codecs
import sys

def strip(x): return x.strip()
def encode(x): return x.encode("utf-8")
def split(x): return x.split("\t")

#Function to check for controlled vocabluary, verbose version which will print everything (OK lines and warning lines)
def check_vocab_verbose(metadata_file, dictionaries):
	f = codecs.open(metadata_file, encoding = "utf-8-sig")
	lines = f.readlines()
	f.close()
	lines = map(strip, lines)
	lines = map(encode, lines)
	lines = map(split, lines)
	if metadata_file.endswith("emd.tsv"):
		for l in lines:
			if l[0] in dictionaries[2].keys():	#check if the key belongs to the regex then check the value if it fits the regex
				if re.search(dictionaries[2][l[0]][0], l[1]):
					print "\t".join(l)
					print "\tAccepted"
				else:
					print("\nWarning! the value ({}) in key ({}) in file ({}) doesn't follow the accepted template").format(l[1], l[0], metadata_file)
					print("\nWarning! the value ({}) in key ({}) don't comply with the templte which is ({})").format(l[1], l[0], dictionaries[2][l[0]][1])
			elif l[0] in dictionaries[1].keys():	#If the key is not from regex, check if it's a white list
				if l[1] in dictionaries[1][l[0]]:
					print "\t".join(l)
					print "\tAccepted"
				else:
					print("\n Warning! the value ({}) in key ({}) in line ({}) is not in the controlled vocabulary\n\n").format(l[1], l[0], metadata_file)
			else:					#if it's not regex nor white list then it's a balck list and can be left as it is
				pass



	elif metadata_file.endswith("smd.txt"):
		for l in lines:
			if l[0] in dictionaries[2].keys():	#check if the key belongs to the regex then check the value if it fits the regex
				if re.search(dictionaries[2][l[0]][0], l[1]):
					print "\t".join(l)
					print "\tAccepted"
				else:
					print("\nWarning! the value ({}) in key ({}) in file ({}) doesn't follow the remplate accepted").format(l[1], l[0], metadata_file)
					print("\nWarning! the value ({}) in key ({}) don't comply with the templte which is ({})").format(l[1], l[0], dictionaries[2][l[0]][1])
			elif l[0] in dictionaries[0].keys():	#If the key is not from regex, check if it's a white list
				if l[1] in dictionaries[0][l[0]]:
					print "\t".join(l)
					print "\tAccepted"
				else:
					print("\nWarning! the value ({}) in key ({}) in line ({}) is not in the controlled vocabulary\n\n").format(l[1], l[0], metadata_file)
			else:					#if it's not regex nor white list then it's a balck list and can be left as it is
				pass



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
			if l[0] in dictionaries[2].keys():	#check if the key belongs to the regex then check the value if it fits the regex
				if re.search(dictionaries[2][l[0]][0], l[1]):
					pass
				else:
					print("\nWarning! the value ({}) in key ({}) in file ({}) doesn't follow the accepted template").format(l[1], l[0], metadata_file)
					print("\nWarning! the value ({}) in key ({}) don't comply with the templte which is ({})").format(l[1], l[0], dictionaries[2][l[0]][1])
			elif l[0] in dictionaries[1].keys():	#If the key is not from regex, check if it's a white list
				if l[1] in dictionaries[1][l[0]]:
					pass
				else:
					print("\n Warning! the value ({}) in key ({}) in line ({}) is not in the controlled vocabulary\n\n").format(l[1], l[0], metadata_file)
			else:					#if it's not regex nor white list then it's a balck list and can be left as it is
				pass



	elif metadata_file.endswith("smd.txt"):
		for l in lines:
			if l[0] in dictionaries[2].keys():	#check if the key belongs to the regex then check the value if it fits the regex
				if re.search(dictionaries[2][l[0]][0], l[1]):
					pass
				else:
					print("\nWarning! the value ({}) in key ({}) in file ({}) doesn't follow the remplate accepted").format(l[1], l[0], metadata_file)
					print("\nWarning! the value ({}) in key ({}) don't comply with the templte which is ({})").format(l[1], l[0], dictionaries[2][l[0]][1])
			elif l[0] in dictionaries[0].keys():	#If the key is not from regex, check if it's a white list
				if l[1] in dictionaries[0][l[0]]:
					pass
				else:
					print("\nWarning! the value ({}) in key ({}) in line ({}) is not in the controlled vocabulary\n\n").format(l[1], l[0], metadata_file)
			else:					#if it's not regex nor white list then it's a balck list and can be left as it is
				pass



#A third way to build the dictionary
def build_dic(keys, files):

	dic = {}
	for key in keys:
		dic[key] = []

	for f in files:
		f = codecs.open(f, encoding = "utf-8-sig")
		lines = f.readlines()
		f.close()
		lines = map(strip, lines)	# get rid of any white spaces of new lines at the end of each line
		lines = map(encode, lines)	# encode the lines as utf-8, it makes it easier for comparison later
		lines = map(split, lines)	# split each lines to ["key", "value"]

		for l in lines:	#if the value is already in the dictionary do nothing, otherwise add that value to the dictionaryLiam Gallagher
			if l[0] in dic.keys():
				if l[1] not in dic[l[0]]:
					dic[l[0]].append(l[1])
	return dic


#getting a list of keys
def list_keys(files, regex_keys, black_keys):
	keys = []
	for f in files:
		f = codecs.open(f, encoding = "utf-8-sig")
		lines = f.readlines()
		f.close()
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
