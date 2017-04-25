#!/usr/bin/python

import codecs

#function for comparing the keys of the new file
#with the keys of the original file, and keeping only the original in the same order

def filtering_keys(original_keys, new_file):
	new_fixed_file = []
	for i in range(0,len(original_keys)):
		for l in new_file:
			if l[0] == original_keys[i]:
				new_line = "\t".join(l)
				new_fixed_file.append(new_line)
	return new_fixed_file


#Getting the names of all the files
all_ = open("sample.txt")
all_files = all_.readlines()
all_.close()

all_files = map(str.rstrip, all_files)  #removing the newline \n

#looping through the files
for f in all_files:

	#retrieving original keys

	f_read_keys = codecs.open("../tmp_metadata/sample/keys/"+f, encoding = "UTF-8-sig")
	original_keys = f_read_keys.readlines()
	f_read_keys.close()

	#removing new lines from original keys
	for idx, l in enumerate(original_keys):
        	original_keys[idx] = original_keys[idx].strip()

	#reading the metadata file
	f_read_file = codecs.open(f,encoding = "UTF-8-sig")  #opening reading

	new_file = f_read_file.readlines()
	f_read_file.close()
	
	#removing new lines
	for idx, l in enumerate(new_file):
		new_file[idx] = new_file[idx].split("\t")

	new_fixed_file = filtering_keys(original_keys = original_keys, new_file = new_file)
	f_write = open("filtered_samples/"+f, "w+") #opening writing
	for l in new_fixed_file:
  		f_write.write(l.encode('UTF-8'))
	f_write.close()



