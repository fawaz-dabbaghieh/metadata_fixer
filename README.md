# Metadata handler and fixer for the DEEP project metadata


## Table of Contentx
  * [Introduction](#Introduction)
  * [Prerequisites](#prerequisites)
  * [Getting started](#getting-started)
    * [1- metadata_fixer](#1--metadata_fixer)
    * [2- build_dictionary](#2--build_dictionary)
    * [3- controlled_vocab](#3--controlled_vocab)
  * [Extra Tools](#extra-tools)
    * [merging files](#merging-files)
    * [un-merging files](#un-merging-files)
    * [Comparing files](#comparing-files)
  * [Adding more JSON operations](#adding-more-json-operations)



## Introduction
Metadata is defined as a structured information which describes and explains other information source or files. This makes metadata a very important and integral part of any project that contains many information sources (e.g. different files, samples, experiments...etc.) which need to be described for easier access and understanding.

Sometimes, if the project is getting information from different sources, the metadata could not be consisted and differ in the way some values are written.
For example in our DEEP project we had this problem of having different sources of metadata describing the different samples and experiments done by different labs. And that lead to having problems such as:
1. Some files were written in differnt encodings (i.e. written on different operating systems) and that had an effect on some of the special characters in the metadata files
2. Some values were written differently depending on the lab that produced the file (e.g. Chip-seq or chip-seq or Chip-Seq)
3. Files were supposed to be in a tsv format, but some had be mistake some extra tabls.

Problems like these could accure in any project dealing with different sources of data and metadata.

In this simple pipeline, we will describe the strategy we used to fix these problems for all our files.

## Prerequisites
Before starting, the metadata_fixer.py script needs to [OpenRefine](http://openrefine.org/download.html). So please check if it's working on your system or if it needs any extra libraries.
The controlled_vocab.py needs [Dictotoxml](https://pypi.python.org/pypi/dicttoxml) to convert the report dictionary to an XML format.

the rest of the libraries are standard Python libraries (os, codecs, sys, re, subprocess, pickle, time, signal, shutil)

## Getting started
So far there are 3 main scripts that can be rand individually (metadata_fixer.py, build_dict.py and controlled_vocab.py). I will explain briefly what each one does and what kind of files does it accepts


### 1- metadata_fixer
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
value1  [[[key introduces]]]    value3
```


**Step Four** It will initiate the OpenRefine process and give OpenRefine the JSON operations file and the big table to be processed and OpenRefine gives back the fixed table which will be saved also as a .tsv file

**Step Five:** The script then will take the table that came out of OpenRefine and take each line and turn it back to a key value format in a opposite way of the previous one.

Taking the previous example:
```
merged_file_after_refine.tsv:
key1    key2    key3
value1_after_refine  value2_after_refine  [[[key introduced]]]
value1_after_refine  [[[key introduces]]]    value3_after_refine
```
becomes:
```
File1.tsv:
key1    value1_after_refine
key2    value2_after_refine
key3 [[[key introduce]]]

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


### 2- build_dictionary
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

### 3- controlled_vocab
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


## Extra Tools
### Merging files
This tool merges metadata files into one table with the each column is a key and each row is a file. Similar to the process written before.
This tool will help you visualize several files in a table for any any check or manual changes.

To merge files you just need to run the tools_launcher.py and us the option `-m DIRECTORY_PATH`
Example: ` python tools_launcher.py -m metadata/experiment ` This will search for all the files in that directory and merge them together and produce the file `table.tsv`
This script will also introduce a new key which is FILE_NAME to store the original file name in case you wanted to separate later to keep the original name

### Un-merging files
You can also use the tools_launcher to separate a table similar to the one previously made to separate files that the script will output in a directory called files_after_table.
You need to provide the path to the table you want to process and the name of the key (column name) which you want to be used for the naming of the files (e.g EXPERIMENT_ID, DEEP_SAMPLE_ID, FILE_NAME)
Example: ` python tools_launcher.py -u TABLE_PATH -k IK_KEY_FOR_NAMING ` and this will produce a directory with the separated files and it will remove the keys introduced by merging and keep the original keys

### Comparing files
You can use this tool to compare two metadata files and check for the differences, the files don't have to be ordered the same. The script will compare the files key-wise and show you the line that are different. You can compare two files and only look at the differences, or you can actually merge the two files by choosing which value you want to keep, and you'll get an output merged file.

1. An example for only comparing two files without an output: `python tools_launcher.py -o OLD_FILE_PATH -n NEW_FILE_PATH` and this will print the differences on the terminal screen in this form:

```
The file (OLD_FILE_PATH) has the line (key1 value1)
The file (NEW_FILE_PATH) has the line (key1 value2)

The file (OLD_FILE_PATH) has the line (key2 value3)
The file (NEW_FILE_PATH) has the line (key2 value4)
```


2. An example for comparing two files with an output: `python tools_launcher.py -o OLD_FILE_PATH -n NEW_FILE_PATH --out OUTPUT_FILE_PATH` the script will compare each key of the one file with another, if the they key is the same and the value is different you'll get to choose which one to keep (the value from the Old file or the value from the New file) or you can type q/Q to quit, in this example we'll chose for key1 the old value and for key2 the new value and you can see what the output file will look like:

```
The old value:	key1	value1
The new value:	key1	value2

Please type O/o to keep the old value, or type in N/n to keep the new value, or Q/q to quit:o

The old value:	key2	value3
The new value:	key2	value4

Please type O/o to keep the old value, or type in N/n to keep the new value, or Q/q to quit:n

$cat OUTPUT_FILE_PATH
key1    value1
key2    value4

```

## Adding more JSON operations

You can always use use the JSON operations on the OpenRefine web API.
**First:** you have to start OpenRefine and start a new project and import your table. Once you've done that, you can easily click on **Undo / Redo** on the top left and then click on **Apply** you can see Figure 1
![Figure 1](/images/figure_1.png)

**Second** You can copy the JSON operations to the window and click **Perform Operations** and it will perform these operations on the table and the number of the operations will show next to **Undo / Redo**, see Figure 2
![Figure 2](/images/figure_2.png)

**Third** You can work on the table (change values, merge cells, combine values...etc). Then after you're done you can click back on **Undo / Redo** and click on **Extract** on the top left, and you get a window of the JSON operations that have been added with a check list. You can use the check list to remove any operation you don't need to be there anymore then you can simply copy the JSON operation on the left window and save it in the operations.json file. See Figure 3
![Figure 3](/images/figure_3.png)
