# Metadata handler and fixer for the DEEP project metadata
Pipeline for fixing some problems related to metadata of the DEEP project. Still under construction.
More comments and better warnings and reporting will be added to the scripts soon.

### Prerequisites
Before starting, the metadata_fixer.py script needs to [OpenRefine](http://openrefine.org/download.html). So please check if it's working on your system or if it needs any extra libraries.
The controlled_vocab.py needs [Dictotoxml](https://pypi.python.org/pypi/dicttoxml) to convert the report dictionary to an XML format.

the rest of the libraries are standard Python libraries (os, codecs, sys, re, subprocess, pickle, time, signal, shutil)

## Getting started
So far there are 3 main scripts that can be rand individually (metadata_fixer.py, build_dict.py and controlled_vocab.py). I will explain briefly what each one does and what kind of files does it accepts


### 1- metadata_fixer.py
This script takes the path to a directory with metedata files as an argument or will ask for it in case it was ran without an argument, regardless of the structure of this directory, it will search recursively for all the files inside of it in a tree strcuture and store the paths of the files to work on. e.g:
```
python metadata_fixer.py metadata/
```
**Step One:** thing it will read the files using the read_files function which will try several encodings and accept the right encodings (using codecs package). This step will help then read the files in the right encodings and when writing them again, they'll be written as UTF-8.
Then it will check if the files are actually TSV and (key value) formatted, otherwise it will skip the file that doesn't comply to this rule and report it at the end.
It will build an exact replicate of the original directory but with the fixed files.

**What are these fixes?**
1. It will fix encodings and remove wrong encoding characters like Ž and Â
2. Remove the space that is sometimes present instead of an "_" in the key
3. Checks if the experiment id inside the file is in correct format according to the DEEP naming scheme, if it's not, it will take the metdata file name and checks if it's correct and then add it to the file. Does the same for the DEEP_SAMPLE_ID files in the sample files
4. Fixes the lines that had a line break in the middle of the value and attach them back to the line they belong to

**Step Two:** It will store all the unique keys from all the files it processed to make a big table of all the files combined later, also stores the original keys fr each files for later filtering.

**Step Three:** It will take all the files that has been processed in step one and merge them in one big .tsv file which we need to give later to OpenRefine to apply the JSON operations on, using the merge_files function. Example of the merging process:

Let's say we have these two files in a key value format:
```
File1.tsv:
key1    value1
key2    value2

File2.tsv:
key1    value1
key3    value3
```
We see that they have one key similar and a different key, when the script merge them, they become
```
merged_file.tsv:
key1    key2    key3
value1  value2  [[[key introduced]]]
value2  [[[key introduces]]]    value3
```


**Step Four** It will initiate the OpenRefine process and give OpenRefine the JSON operations file and the big table to be processed and OpenRefine gives back the fixed table which will be saved also as a .tsv file

**Step Five:** The script then will take the table that came out of OpenRefine and take each line and turn it back to a key value format in a opposite way of the previous one.

Taking the previous example:
```
merged_file_after_refine.tsv:
key1    key2    key3
value1_after_refine  value2_after_refine  [[[key introduced]]]
value2_after_refine  [[[key introduces]]]    value3_after_refine
```
becomes:
```
File1.tsv:
key1    value1_after_refine
key2    value2_after_refine
keu3 [[[key introduce]]]

File2.tsv:
key1    value1_after_refine
key2    [[[key introduce]]]
key3    value3_after_refine
```
**Step 6:** We can see that we have these [[[key introduce]]] because of the merging, the script will filter each file against the original keys it had and keep the new fixed values.
The final outcome will be:

```
File1.tsv:
key1    value1_after_refine
key2    value2_after_refine

File2.tsv:
key1    value1_after_refine
key3    value3_after_refine
```


### 1- build_dictionary.py
This script will also takes a path to a directory with metadata and checks all the files and make a white-list accepted values dictionary out of those files and output them in a human readabel TSV format, which can be editted easily to add new accepted keys and values.
This script also comes with two files: 
1. black_keys.txt file which have the balck keys that we are ignoring from checking, and these keys can have any value (e.g. COMMENTS)
2. regex_dictionary.tsv which has the regular expression for values related to some keys and an accepted example

The steps to this script are simple.
**Step one:** It will check for all the files in that directory and read them one by one and start building the dictionary in a very simple way:

If the file is an experiment metadata file (ends with _emd.tsv) it will check each key, if the key is black key or a regex key it will be ignored. Otherwise, it's considered to be a white key and the value is taken and stored in an experiment's metadata dictionary and this is done recursively for all the files and all the keys.
The same thing is done for the sample files and they are stored in a sample metadata dictionary.

**Why do we need this script?**
We need it to build new dictionaries when we have new files, let's say now we have 800 experiments metadata files that have accepted value, if we introduce 20 new accepted files with accepted values different than the other 800 we can run this script again and build a new dictionary.

These dictionaries are important for the third script

### 1- controlled_vocab.py
This script has many options which can be viewed easily using:
```
python controlled_vocab.py -h
```
Or `--help`
This will print the following option

```
Usage: controlled_vocab.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  The name of the file to be processed by the pipeline
  -l FILES_LIST, --list=FILES_LIST name or path to a file, containing list of files to be processed
  -d PATH, --directory=PATH name or path of the directory containing files to be processed
  -v, --verbose         To turn the Verbose mode on
  -k KEY, --key=KEY     Shows the accepted values for the key given by user
  --list_keys           List all keys in dictionary
  --list_regex          List all regular expression that are controlled with examples
```

A brief introduction on each option:

`-f, --file` You can give the path to one metadata file you want to check if it has correct values or not accroding the the dictionaries that been explained before. Then a report will be written in the same directory of the script in an XML format *Still working in making the XML better and desigining a template for readabillity*
Example: `python controlled_vocab.py -f PATH_TO_FILE`

`-l, --list` Takes a file that contains a list of files that you would to check recursively, it will go through each file written inside that file and then output one report.xml file with a report on all the files, each file will be a parent with each line as a child in the XML file.
Example: `python controlled_vocab.py -l PATH_TO_FILE`

`-d, --directory` Takes the path of a directory containing the files you want to check for and then output one report.xml for all the files.
Example: `python controlled_vocab.py -d PATH_TO_DIRECTORY`

`-v, --verbose` If this option is present with one of the previous option, will turn Verbose on. Which means that the report.xml will include all the lines (the accepted ones and the ones with Warnings!). Without it, the report will only have the lines with warnings.
Example: `python controlled_vocab.py -v -f PATH_TO_FILE`

`-k, --key` Takes a valid key that belongs to one of the dictionaries and output the accepted values for that key
Example: `python controlled_vocab.py -k KEY`

`-list_keys` Will list all the keys available in all the dictionaries and outputs them to the terminal
Example: `python controlled_vocab.py --list_keys`

`-list_regex` Will list all the keys we're doing regular expression on with the regular expression and an example of an accepted value
Example: `python controlled_vocab.py --list_regex`
