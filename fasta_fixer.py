import shutil
def fix_file(input_file):
    with open(input_file, "r") as ifile:
        everything = ifile.read()
    with open(input_file + ".tmp", "w") as ofile:
        for line in everything.split("\n"):
            try:
                if line[0] == ">":
                    ofile.write("\n" + line + "\n")
                else:
                    ofile.write(line)
            except IndexError:
                print line + "\n"
    shutil.move(input_file + ".tmp", input_file)