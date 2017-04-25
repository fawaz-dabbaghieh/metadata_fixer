#!/usr/bin/python

import codecs

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
				#exp_id = lines[idx].split("\t")
				#print exp_id[1]
				#exp_id[1] = file_name.decode('UTF-8','ignore')
				#exp_id = "\t".join(exp_id)

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

#Getting the names of all the files and making a list of them
all_ = open("files.txt")
all_files = all_.readlines()
all_.close()

all_files = map(str.rstrip, all_files)  #removing the newline \n

#looping through the files
for f in all_files:
	f_read = codecs.open(f,encoding = "UTF-8-sig")  #opening reading
	f_write = open("after_python/"+f, "w+") #opening writing
	lines = f_read.readlines()
	f_read.close()
	
	new_lines = lines_fixer(lines = lines)
	new_lines_no_dup = duplicate_lines(lines = new_lines)
	new_lines_fixed = experiment_id(lines = new_lines_no_dup, file_name = f)
	for l in new_lines_fixed:
  		f_write.write(l.encode('UTF-8') + '\n')
	f_write.close()
