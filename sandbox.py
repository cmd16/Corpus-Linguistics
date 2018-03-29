import os
import re
project_dir = "/Volumes/2TB/Final_Project"
# filename = os.path.join(proj_dir, "Fanfic_all/13346448.txt")
# f_in = open(filename, 'r+')
# print(bool(re.search('[a-zA-Z]', f_in.readline())))
# if re.search('[a-zA-Z]', f_in.readline()):
#     print("false positive")
# f_in.close()
# print(bool(re.search('[a-zA-Z]', " word1")))
# if re.search('[a-zA-Z]', " word1"):
#     print("true positive")
# print(bool(re.search('[a-zA-Z]', "")))

test_str = "hello.txt"
print(test_str[:test_str.index(".txt")])
