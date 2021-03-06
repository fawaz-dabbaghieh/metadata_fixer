# To convert a big table back to individual tsv files
# The table has column as keys, and rows as experiment metadata

import codecs
import sys
import os


def strip(x): return x.strip()


def encode(x): return x.encode("utf-8")


# The conversion function
def read_files(file_name):
    encodings = ['utf-8-sig', 'iso-8859-1', 'utf-16']
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


# Function to check if all lines has the same number of columns
def check_lines_equals(lines):
    column_number = len(lines[0].split("\t"))
    wrong_lines = []
    for idx, l in enumerate(lines):
        if len(l.split("\t")) == column_number:
            continue
        else:
            wrong_lines.append(idx)
    if not wrong_lines:
        return True
    else:
        return wrong_lines


def tsv_to_files(lines, i):
    # keys are the first row
    keys = lines[0].strip().split("\t")
    values = lines[i].split("\t")
    new_file = []
    for j in range(0, len(keys)):
        new_line = keys[j] + "\t" + values[j]
        new_file.append(new_line)
    return new_file


# filter the extra keys
def filter_lines(lines):
    filtered_lines = []
    # for l in lines:
    # if not l.split("\t")[1] == "[[[Extra Key Introduced]]]":
    # filtered_lines.append(l)
    for l in lines:
        if "[[[Extra Key Introduced]]]" not in l:
            filtered_lines.append(l)
    return filtered_lines


##################################################################################
def separate_table(table_path, id_key):
    lines = read_files(table_path)

    if check_lines_equals(lines):
        # Checking the id_key given
        keys = map(encode, map(strip, lines[0].split("\t")))
        if id_key.encode("utf-8") in keys:
            for idx, k in enumerate(keys):
                if k == id_key:
                    id_idx = idx
        else:
            print("The key ({}) was not one of the column names in the table, please check again".format(id_key))
            sys.exit()

        # Looping through the lines and writing the files
        if not os.path.exists(table_path.split(os.sep)[-1] + "_files"):
            os.mkdir(table_path.split(os.sep)[-1] + "_files")

        for i in range(1, len(lines)):
            file_name = lines[i].split("\t")[id_idx]

            f_write = open(table_path.split(os.sep)[-1] + "_files" + "/" + file_name + ".tsv", "w+")
            new_file = tsv_to_files(lines=lines, i=i)
            filtered_file = filter_lines(new_file)
            for l in filtered_file:
                f_write.write(l.encode('UTF-8') + "\n")
            f_write.close()
    else:
        wrong_lines = check_lines_equals(lines)
        print("The lines ({}) in the table have different column number, "
              "please check the file and try again".format(",".join(wrong_lines)))
        sys.exit()


############################################################################
if __name__ == "__main__":
    arguments = sys.argv
    if (len(arguments) == 1) or (len(arguments) == 2):
        print "please, try again and give the path to the table and the column " \
              "name to use for naming the separate files"
        sys.exit()
    else:
        if os.path.exists(arguments[1]):
            table_path = arguments[1]
        else:
            print("WARNING! The table path given as an argument was not valid, please try again")
            sys.exit()
    separate_table(table_path, arguments[2])
