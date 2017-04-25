#!/usr/bin/python

import codecs
import re
import sys
import os

#Taking answers for file comparison
def answers(l_old, l_new, compared_file):
	while True:
		print("The old value:"+"\t".join(l_old)+"\n"+"The new value:"+"\t".join(l_new)+"\n")
		answer = raw_input("\nPlease type in O/o to keep the old value, or type in N/n to change the old value to the new one, or Q/q to quit :")
		if (answer == "O") or (answer == "o"):
			compared_file.append(l_old)
			break
		elif (answer == "N") or (answer == "n"):
			compared_file.append(l_new)
			break
		elif (answer == "Q") or (answer == "q"):
			sys.exit()
		else:
			print("You did not choose a right answer, please try again or type Q/q to quit: ")


#function to do comparison
def comparing_files(old,new):
	compared_file = []
	for idx_old, l_old in enumerate(old):
		for idx_new, l_new in enumerate(new):
			if l_old[0] == l_new[0]:
				if l_old[1] == l_new[1]:
					compared_file.append(l_old)
				else:
					answers(l_old=l_old, l_new=l_new,compared_file=compared_file)
	return compared_file

#adding new keys
def adding_new_keys(old,new, compared):
	nas = ["no-data\n", "NA\n", "na\n", "N/A\n"]
	old_keys = []
	for l in old:
		old_keys.append(l[0])
	for l in new:
		if l[0] not in old_keys:
			if l[1] in nas:
				continue
			else:
				compared.append(l)
	return compared

#Read file names
files_path = raw_input("please give the path to file with the list of names: ")
f = codecs.open(files_path, encoding = "utf-8-sig")
files = f.readlines()
f.close()

for idx, l in enumerate(files):
	files[idx] = l.strip()

#Taking the paths from raw input for old and new file

for l_file in files:

	print l_file
	old_file_path = files_path.split("/")[0] + "/"  + "fixed_files/" + l_file

	new_file_path = files_path.split("/")[0] + "/" + l_file


	if not os.path.exists("new_files/"):
	    os.makedirs("new_files/")

	f = codecs.open(old_file_path, encoding = "UTF-8-sig")
	old_file = f.readlines()
	f.close()

	f = codecs.open(new_file_path, encoding = "UTF-8-sig")
	new_file = f.readlines()
	f.close()

	for idx,l in enumerate(old_file):
		old_file[idx] = l.split("\t")

	for idx,l in enumerate(new_file):
		new_file[idx] = l.split("\t")

	compared_file = comparing_files(old = old_file, new = new_file)
	compared_file = adding_new_keys(old = old_file, new = new_file, compared = compared_file)
	for idx, l in enumerate(compared_file):
		compared_file[idx] = "\t".join(l)


	file_name = old_file_path.split("/")[-1]

	f_write = open("new_files/"+file_name, "w+")
	for l in compared_file:
		f_write.write(l.encode('UTF-8'))
	f_write.close()
