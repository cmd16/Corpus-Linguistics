"""This script takes in a file and creates a file with the html tags removed."""

import re

infilename = input("enter an infilename: ")
outfilename = input("enter an outfilename: ")

infile = open(infilename,'r')
outfile = open(outfilename,'w')

print("processing")

for line in infile:
    # remove div tags
    line = re.sub('<.*?>'," ",line)
    #line = line.replace("<div>" , "")
    #line = line.replace("</div>" , "")
    # write the line
    outfile.write(line + "\n")

print("done")
