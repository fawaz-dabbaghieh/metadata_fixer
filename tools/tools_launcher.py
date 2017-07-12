from optparse import OptionParser
import sys
import re
import os
import codecs
import combine_tsv
import table_to_files

def strip(x): return x.strip()
def encode(x): return x.encode("utf-8")

if sys.argv[1:] == []:
    print "No Arguments were given, please try -h or --help"
    sys.exit()
    
#Arguments parser
parser = OptionParser()
parser.add_option("-m","--merge",dest="merge_files_dir",help="path to directory with files to merge", metavar="MERGE_DIRECTORY")

parser.add_option("-u","--unmerge",dest="table_path",help="path to the tsv table you want to separate to individual files, need option --file_key ", metavar="TABLE_PATH")

parser.add_option("-k", "--file_key",dest="key",help="key or column name which containe the ID to name the individual files", metavar="KEY")

parser.add_option("--list_regex", dest="list_regex", action="store_true",default=False,help="List all regular expression that are controlled with examples")

(options, args) = parser.parse_args()
merge_directory = options.merge_files_dir
table_path = options.table_path
id_key = options.key
key_from_user = options.key


if merge_directory is not None:
    if os.path.exists(merge_directory):
        combine_tsv.combine_files(merge_directory)
    else:
        print "the path you gave does not exits, please try again"
        
        
if table_path is not None:
    if id_key is not None:
        
        table_to_files.separate_table(table_path, id_key)
        
    else:
        print "you did not give the id key name in the table, please add that using -k or --file_key option"
        sys.exit()
    