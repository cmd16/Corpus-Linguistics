import os

def count_sentences(dir): # this version walks through all directories
    sentence_count = 0
    for path in os.walk(dir):
        for localname in path[2]:
            if localname.endswith(".txt"):
                filename = os.path.join(path[0],localname)
                with open(filename, 'r') as file:
                    file_contents = file.read()
                    sentence_count += file_contents.count(".") + file_contents.count("!") + file_contents.count("?") + file_contents.count("\n")
    return sentence_count

"""for item in os.walk("/Users/cat/Intro to Corpus Linguistics/Catherine DeJager Corpus"):
    print(item[0])
    for filename in item[2]:
        if (filename.endswith(".txt")):
            print(filename)
"""

file_contents = open("cdj_POLS207_academicessayNov3016_GlobalizationandDecolonization.txt").read()
print(file_contents.count(".") + file_contents.count("!") + file_contents.count("?") + file_contents.count("\n"))

#print(count_sentences("/Users/cat/Intro to Corpus Linguistics/Catherine DeJager Corpus"))
