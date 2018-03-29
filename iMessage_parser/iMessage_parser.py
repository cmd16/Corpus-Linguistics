
infilename = input("enter an infilename: ")
outfilename = input("enter an outfilename: ")
yourname = input("enter your name: ")
othername = input("enter the other person's name: ")
infile = open(infilename,'r')
outfile = open(outfilename,'w')
store = False
print("processing")

for line in infile:
    if yourname + ":" in line:
        store = True
    if othername + ":" in line:
        store = False
    if store:
        if "catherine:" not in line: #don't want to include actual name
            outfile.write(line + "\n")
print("done")

infile.close()
outfile.close()