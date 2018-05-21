import codecs
import sys
import os


def split(x): return x.split("\t")


# function for reading files in the right encodings
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
            break


# Taking answers for file comparison
def answers(l_old, l_new, compared_file):
    while True:
        print("The old value:\t{}\n"+"The new value:\t{}\n").format("\t".join(l_old).encode("utf-8").strip(),
                                                                    "\t".join(l_new).encode("utf-8").strip())
        answer = raw_input("Please type O/o to keep the old value, or type in N/n to keep the new value, "
                           "or Q/q to quit:")
        if (answer == "O") or (answer == "o"):
            compared_file.append(l_old)
            break
        elif (answer == "N") or (answer == "n"):
            compared_file.append(l_new)
            break
        elif (answer == "Q") or (answer == "q"):
            sys.exit()
        else:
            print("You did not choose a right answer, please try again or type Q/q to quit: ")
                
    return compared_file


# function to do comparison
def comparing(old, new):
    compared_file = []
    for idx_old, l_old in enumerate(old):
        for idx_new, l_new in enumerate(new):
            if l_old[0] == l_new[0]:
                if l_old[1] == l_new[1]:
                    compared_file.append(l_old)
                else:
                    compared_file = answers(l_old, l_new, compared_file)
    return compared_file


# adding new keys that aren't present in the old file
def adding_new_keys(old, new, compared):
    nas = ["no-data\n", "NA\n", "na\n", "N/A\n"]
    old_keys = []
    for l in old:
        old_keys.append(l[0])
    for l in new:
        if l[0] not in old_keys:
            if l[1] in nas:
                continue
            else:
                compared.append(l)
    return compared


# Taking the paths from raw input for old and new file
def comparing_files_with_output(old_file_path, new_file_path, output_file_path):
    if os.path.exists(old_file_path):
        if os.path.exists(new_file_path):
            new_file = read_files(new_file_path)
            if new_file == new_file_path:
                print("The file ({}) doesn't seem to be in a tsv format, "
                      "please check the file and try again").format(new_file_path)
                sys.exit()
            old_file = read_files(old_file_path)
            if old_file == old_file_path:
                print("The file ({}) doesn't seem to be in a tsv format, "
                      "please check the file and try again").format(old_file_path)
                sys.exit()
        else:
            print("the path ({}) does not exists, please try again".format(new_file_path))
            sys.exit()
    else:
        print("the path ({}) does not exists, please try again".format(old_file_path))
        sys.exit()

    old_file = map(split, old_file)
    new_file = map(split, new_file)

    compared_file = comparing(old_file, new_file)
    compared_file = adding_new_keys(old_file, new_file, compared_file)
    for idx, l in enumerate(compared_file):
        compared_file[idx] = "\t".join(l)

    f_write = open(output_file_path, "w+")
    for l in compared_file:
        f_write.write(l.encode('utf-8'))
    f_write.close()


############################################################################
def comparing_files(old_file_path, new_file_path):
    if os.path.exists(old_file_path):
        if os.path.exists(new_file_path):
            new_file = read_files(new_file_path)
            if new_file == new_file_path:
                print("The file ({}) doesn't seem to be in a tsv format, "
                      "please check the file and try again").format(new_file_path)
                sys.exit()
            old_file = read_files(old_file_path)
            if old_file == old_file_path:
                print("The file ({}) doesn't seem to be in a tsv format, "
                      "please check the file and try again").format(old_file_path)
                sys.exit()
        else:
            print("the path {} does not exists, "
                  "please try again").format(new_file_path)
            sys.exit()
    else:
        print("the path {} does not exists, "
              "please try again").format(old_file_path)
        sys.exit()

    old_file = map(split, old_file)
    new_file = map(split, new_file)

    for idx_old, l_old in enumerate(old_file):
        for idx_new, l_new in enumerate(new_file):
            if l_old[0] == l_new[0]:
                if l_old[1] == l_new[1]:
                    pass
                else:
                    print("The file ({}) has the line\t({})\nThe file ({}) "
                          "has the line\t({})\n").format(old_file_path,
                                                         "\t".join(l_old).encode("utf-8").strip(),
                                                         new_file_path, "\t".join(l_new).encode("utf-8").strip())

    
############################################################################

if __name__ == "__main__":
    arguments = sys.argv

    if len(arguments) < 3:
        print "please, try again and give the path to the old file then the new file " \
              "then optionally the output file path or name"
        sys.exit()
        
    else:
        if os.path.exists(arguments[1]):
            if os.path.exists(arguments[2]):
                if arguments[3]:
                    comparing_files_with_output(arguments[1], arguments[2], arguments[3])
                else:
                    comparing_files(arguments[1], arguments[2])
            else:
                print "the path to the new file does not exists, please try again (old file then new file)"
                sys.exit()
        else:
            print("the path to the old file does not exists, please try again (old file then new file)")
            sys.exit()
