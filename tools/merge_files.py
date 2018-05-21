#!/usr/bin/python
import codecs
import sys
import os


def read_files(file_name):
    encodings = ['utf-8-sig', 'iso-8859-1', 'utf-16']
    if os.path.exists(file_name):
        for e in encodings:
            try:
                f = codecs.open(file_name, 'r', encoding=e)
                lines = f.readlines()
                f.close()
                lines_to_return = []
                for l in lines:
                    if not l.isspace():
                        lines_to_return.append(l)
                if lines_to_return:
                    return lines_to_return

            except UnicodeError:
                print('got unicode error with %s , trying different encoding' % e)
            else:
                # print('opening the file with encoding:  %s ' % e)
                break
    else:
        return file_name


def check_if_tsv(lines):
    wrong_lines = []
    for idx, l in enumerate(lines):
        if len(l.strip().split("\t")) == 2:
            continue
        else:
            wrong_lines.append(idx)
    if not wrong_lines:
        return True
    else:
        return wrong_lines


# making a list of keys and adding new keys.
def new_keys(keys, files):
    for f in files:
        lines = read_files(f)
        for l in lines:
            key = l.split("\t")[0]
            if key in keys:
                continue
            else:
                keys.append(key)
    return keys


# returning the value that corresponds to key
def return_value(key, lines):
    value = "[[[Extra Key Introduced]]]"
    for l in lines:
        if key in l:
            value = l[1]
        else:
            continue
    return value


############################################################################
def combine_files(directory_path):
    if os.path.exists(directory_path):
        pass
    else:
        print("WARNING!! The metadata directory path given as an argument was not valid, please try again")
        sys.exit()

    metadata_files = []
    for root, dirs, files in os.walk(directory_path):
        for f in files:
            metadata_files.append(os.path.join(root, f))

    # Get a list of all keys
    keys = []
    keys = new_keys(keys, metadata_files)
    keys.append("FILE_NAME")
    # making the tsv table
    new_table = ["\t".join(keys)]

    skipped_files = []
    for f in metadata_files:
        lines = read_files(f)
        # This file will be skipped because the read_files() functions returned the name of the file,
        # that means there was an error and the file wasn't read properly
        if lines == f:
            skipped_files.append(f)
            continue
        elif check_if_tsv(lines):
            # adding the file name with the new key to the file before merging
            lines.append("FILE_NAME\t" + f.split("/")[-1])
            for idx, l in enumerate(lines):
                lines[idx] = l.split("\t")

            new_file = []
            for key in keys:
                value = return_value(key, lines)
                new_file.append(value)

            for idx, value in enumerate(new_file):
                new_file[idx] = value.strip()
            new_file = "\t".join(new_file)
            new_table.append(new_file)
        else:
            print("The file ({}) is not in the accepted format which is a (key value) "
                  "and tab separated, please check it again").format(f)
            skipped_files.append(f)

    w = codecs.open("table.tsv", "w+")
    for l in new_table:
        w.write(l.encode("utf-8")+"\n")
    w.close()


############################################################################
if __name__ == "__main__":
    arguments = sys.argv

    if len(arguments) == 1:
        while True:
            metadata_path = raw_input("Please, give the name or path of the metadata file:\n")
            if os.path.exists(metadata_path):
                break
            elif metadata_path == "exit":
                sys.exit()
            else:
                print("The metadata directory path is not valid, please try again or type \"exit\"")
    else:
        if os.path.exists(arguments[1]):
            metadata_path = arguments[1]
        else:
            print("WARNING!! The metadata directory path given as an argument was not valid, please try again")
            sys.exit()

    combine_files(metadata_path)
