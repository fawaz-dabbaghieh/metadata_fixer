from optparse import OptionParser
import sys
import re
import os
import codecs
import merge_files
import unmerge_files
import comparing_files


def strip(x): return x.strip()
def encode(x): return x.encode("utf-8")


if sys.argv[1:] == []:
    print "No Arguments were given, please try -h or --help to print the help message"
    sys.exit()
    
#Arguments parser
parser = OptionParser()

parser.add_option("-m","--merge",dest="merge_files_dir",help="path to directory with files to merge", metavar="MERGE_DIRECTORY")

parser.add_option("-u","--unmerge",dest="table_path",help="path to the tsv table you want to separate to individual files, need option --file_key ", metavar="TABLE_PATH")

parser.add_option("-k", "--file_key",dest="key",help="key or column name which containe the ID to name the individual files", metavar="KEY")

parser.add_option("-o","--old", dest="old_file", help="path to the old file for comparison, needs the new file too to compare", metavar="OLD_PATH")

parser.add_option("-n","--new", dest="new_file", help="path to the new file for comparison, needs the old file too to compare", metavar="NEW_PATH")

parser.add_option("--out","--output_file", dest="output_file", help="Path or name to output file, if this is specified with having an Old and New file, there will be an output file which compares and merges the two files and the user can choose which value to keep in case they were different", metavar="OUTPUT_FILE")



(options, args) = parser.parse_args()
merge_directory = options.merge_files_dir

table_path = options.table_path
id_key = options.key

old_file_path = options.old_file
new_file_path = options.new_file
output_file_path = options.output_file

##############################################
if merge_directory is not None:
    if os.path.exists(merge_directory):
        merge_files.combine_files(merge_directory)
    else:
        print "the path you gave does not exits, please try again"
        

##############################################        
if table_path is not None:
    if id_key is not None:
        
        unmerge_files.separate_table(table_path, id_key)
        
    else:
        print "you did not give the id key name in the table, please add that using -k or --file_key option"
        sys.exit()

##############################################
if old_file_path is not None:
    if os.path.exists(old_file_path):
        if new_file_path is not None:
            if os.path.exists(new_file_path):
                if output_file_path is not None:
                    comparing_files.comparing_files_with_output(old_file_path, new_file_path, output_file_path)
                else:
                    comparing_files.comparing_files(old_file_path, new_file_path)
            else:
                print("the path {} does not exists, try again").format(new_file_path)
                sys.exit()
    else:
        print("the path {} does not exists, try again").format(old_file_path)
        sys.exit()
