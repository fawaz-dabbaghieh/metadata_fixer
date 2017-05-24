def strip(x): return x.strip()
def encode(x): return x.encode("utf-8")

#Function to check for controlled vocabluary verbose version
def check_vocab_verbose(lines, dictionary):
    for idx, l in enumerate(lines):
        l = l.split("\t")	#each line becomes a list of ['key','value']
        if l[0] in dictionary.keys():
            if l[1] in dictionary[l[0]]:
                print l
		print "\t Is OK\n"
            else:
		print("\n Warning! the value ({}) in key ({}) in line ({}) is not in the controlled vocabulary'n".format(l[1],l[0],idx))

        elif l == ['']:
            print "Line %s is empty" %idx

        else:
            print l
            print("Warning! the key ({}) is not one of the dictionary keys".format(l[0]))



#Function to check for controlled vocabluary
def check_vocab(lines, dictionary):
    for idx, l in enumerate(lines):
        l = l.split("\t")	#each line is a list of ['key','value']
        if l[0] in dictionary.keys():
            if l[1] in dictionary[l[0]]:
		continue
            else:
		print("\n Warning! the value ({}) in key ({}) in line ({}) is not in the controlled vocabulary'n".format(l[1],l[0],idx))

        elif l == ['']:
            print "Line %s is empty" %idx

        else:
            print l
            print("Warning! the key ({}) is not one of the dictionary keys".format(l[0]))


#Check for duplicate lines
def duplicate_lines(lines):
	duplicates = []
	for idx, l in enumerate(lines):
		if l.startswith("RNA_cDNA_PREPARATION_REVERSE_TRANSCRIPTION_PROTOCOL".decode('UTF-8', 'ignore')):
			duplicates.append(idx)
	if len(duplicates) == 2:
		dup_line = lines[duplicates[0]].split("\t")
		dup_line[0] = dup_line[0] + "_1"
		dup_line = "\t".join(dup_line) 
		lines[duplicates[0]] = dup_line
	return lines


#Adding Experiment ID to the files
def experiment_id(lines, file_name):
	#checking if EXPERIMENT_ID exists
	if any("EXPERIMENT_ID" in s for s in lines):
		for idx,l in enumerate(lines):
			if l.startswith("EXPERIMENT_ID"):
				exp_id = "EXPERIMENT_ID".decode('UTF-8', 'ignore') + "\t" + file_name.decode('UTF-8', 'ignore')
				lines[idx] = exp_id.decode('UTF-8', 'ignore')
	else:
		exp_id = "EXPERIMENT_ID" + "\t" + file_name
		lines.append(exp_id) 
	return lines



#checks line start and append to previous if it does not start with a key
def check_line_start(line):
	starts = ["5".decode('UTF-8', 'ignore'),"CGC".decode('UTF-8', 'ignore'),"HCS".decode('UTF-8', 'ignore'),"Julia".decode('UTF-8', 'ignore'),"Rep".decode('UTF-8', 'ignore'),"http".decode('UTF-8', 'ignore')]
	for s in starts:
		if line.startswith(s): return True
	return False

#returning a list of all the lines of a file
def lines_fixer(lines):
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
            key = s[0]
            value = " ".join(s[1:])
            new_line = [key, value]
            new_line = "\t".join(new_line)
            new_lines.append(new_line)

		
    return new_lines

#getting a list of keys
def list_keys(files):
	keys = []
	for f in files:
		f = codecs.open(f, encoding = "utf-8-sig")
		lines = f.readlines()
		f.close()
		lines = map(encode, lines)
		for l in lines:
			l = l.split("\t")
			if l[0] not in keys:
				keys.append(l[0])
			else:
				continue
	return keys
	

"""
#Making dictionary from list of files
def make_dic(keys, files):                
    dic = {}
    for key in keys:
        dic[key] = []
        for f in files:
            f = codecs.open(f, encoding = "utf-8-sig")
            lines = f.readlines()
            f.close()
            lines = map(strip,lines)
            lines = map(encode, lines)
            for l in lines:
                if l.split("\t")[0] == key:
                    if l.split("\t")[1] not in dic[key]:
				dic[key].append(l.split("\t")[1])
                    else:
			continue
                else:
                    continue
    return dic
"""
"""
#A faster way to get the dictionary:
def make_dic(keys, files):
	dic = {}
	for f in files:
		f = codecs.open(f, encoding = "utf-8-sig")
		lines = f.readlines()
		f.close()
		lines = map(strip, lines)
		lines = map(encode, lines)
		for key in keys:
			dic[key] = []
			for l in lines:
				if l.split("\t")[0] == key:
					if l.split("\t")[1] not in dic[key]:
						dic[key].append(l.split("\t")[1])
					else:
						continue
				else:
					continue
	return dic
"""

#A third way to build the dictionary
def make_dic(keys, files):
	dic = {}
	for key in keys:
		dic[key] = []
	for f in files:
		f = codecs.open(f, encoding = "utf-8-sig")
		lines = f.readlines()
		f.close()
		lines = map(strip, lines)
		lines = map(encode, lines)
		for l in lines:
			if l.split("\t")[1] in dic[l.split("\t")[0]]:
				continue
			else:
				dic[l.split("\t")[0]].append(l.split("\t")[1])
	return dic

