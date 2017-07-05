#writing down a test_dict as tsv
test_dict_lines = []
for k in test_dict.keys():
    test_dict[k] = "\t".join(test_dict[k])
    test_dict_lines.append(k+"\t"+test_dict[k])

f = open("test_dict.tsv", "w+")
for l in test_dict:
    f.write(l+"\n")
f.close()


#reading the dictionary again
f = open("test_dict.tsv", "r+")
test_dict = f.readlines()
f.close()
regex_dict = {}
    for idx,l in enumerate(test_dict):
        l = l.encode("utf-8")
        regex_dict[l.split("\t")[0]] = l.split("\t")[1:]


#TODO
#   1- the dictionaries stuff
#   2- optional arguments for functions
#   3- make controlled vocabulary pipeline works for only experiments or only samples
#   4- XML stuff on the reporting
#   5- Documentation