import urllib.request

blogpost = urllib.request.urlopen("http://vortexofdeduction.blogspot.com/2015/03/top-10-fictional-characters-who-are.html")
for line in blogpost:
    strline = str(line)
    print(line)
    if "property='og:title'" in strline:
        title_begin = strline.find("'") + 1
        title_list = strline[title_begin : strline.find("'", title_begin)].split() #split into words of title
        title = ""
        for item in title_list:
            title += item
        print(title)