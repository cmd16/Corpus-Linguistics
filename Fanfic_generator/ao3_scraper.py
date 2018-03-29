import urllib.request
import csv

class AO3_work:
    def __init__(self,title,creator,rating,warning,category,fandom,relationships,characters,tags,language,published,updated,words,chapters,comments,kudos,bookmarks,hits,id,text):
        self.title = title
        self.creator = creator
        self.rating = rating
        self.warning = warning
        self.category = category
        self.fandom = fandom
        self.relationships = relationships
        self.characters = characters
        self.tags = tags
        self.language = language
        self.published = published
        self.updated = updated
        self.words = words
        self.chapters = chapters
        self.comments = comments
        self.kudos = kudos
        self.bookmarks = bookmarks
        self.hits = hits
        self.id = id
        self.text = text


def pull_ids(url, startnum, pagenum, output):
    wr = csv.writer(output, delimiter=',')
    """
    key = "page="
    start = url.find(key)

    # there is already a page indicator in the url
    if (start is not -1):
        # find where in the url the page indicator starts and ends
        page_start_index = start + len(key)
        page_end_index = url.find("&", page_start_index)
        # if it's in the middle of the url
        if (page_end_index is not -1):
            page = int(url[page_start_index:page_end_index]) + 1
            url = url[:page_start_index] + str(page) + url[page_end_index:]
        # if it's at the end of the url
        else:
            page = int(url[page_start_index:]) + 1
            url = url[:page_start_index] + str(page)
    """
    current_url = url
    for current_page in range(startnum, pagenum+1):
        # BEGIN lines copied
        key = "page="
        start = current_url.find(key)
        # find where in the url the page indicator starts and ends
        page_start_index = start + len(key)
        page_end_index = current_url.find("&", page_start_index)
        # if it's in the middle of the url
        if (page_end_index is not -1):
            # page = int(url[page_start_index:page_end_index]) + 1
            page = current_page
            current_url = current_url[:page_start_index] + str(page) + current_url[page_end_index:]
        # if it's at the end of the url
        else:
            page = int(current_url[page_start_index:]) + 1
            current_url = current_url[:page_start_index] + str(page)
        # END lines copied
        print(current_url)
        file = urllib.request.urlopen(current_url)
        for line in file:
            strline = str(line)
            if 'class="work blurb group"' in strline:
                id = strline[strline.index('_')+1:strline.index('" role')]
                '''if id in sherlock_ids or id in sherlock_all_ids:
                    continue'''
                # output.write(id+'\n')
                wr.writerow([id, current_url])


# scraping
outfile = open("Undertale_ids.csv", 'a')
url = 'http://archiveofourown.org/tags/Supernatural/works?commit=Sort+and+Filter&page=1&utf8=%E2%9C%93&work_search%5Bcomplete%5D=0&work_search%5Blanguage_id%5D=1&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Bsort_column%5D=revised_at'
pull_ids(url, 489, 8537, outfile)
outfile.close()


# get ids
"""
infile = open("sherlock_id_list.txt", "r")
outfile = open("sherlock_work_urls.txt", "w")
for line in infile:
    work_id = line.strip()
    work_url = 'http://archiveofourown.org/works/' + work_id + "?view_full_work=true"
    outfile.write(work_url+"\n")
infile.close()
outfile.close()
"""

"""
#THIS PART NOT WORKING YET
import urllib.request

infile = open('vortexofdeductionfanfics.txt', 'r')
for work_id in infile:
    work_url = 'http://archiveofourown.org/works/' + work_id
    file = urllib.request.urlopen(work_url)
    for line in file:
        strline = str(line)
        if '[Archive' in strline:
            splitted = strline.split(' - ')
            title = splitted[0][10:].replace(' ','%20')
            author = splitted[1]
    download_url = "http://download.archiveofourown.org/downloads/"+author[0:2]+'/'+author+'/'+work_id+'/'+title+'.html?'
    download_url = download_url.replace('\n','')
    print(download_url)
    work = urllib.request.urlopen(download_url)
    line_num = 1
    workline = 0
    end_line = 0
    workfile = open(title+".txt",'w')
    for line in work:
        print(line)
        strline = str(line)
        if '<div id="endnotes">' in strline:
            end_line = line_num
        if '<p class="message">' in strline and end_line == 0:
            end_line = line_num
        if 'div class="userstuff"' in strline:
            workline = line_num+1
        print(workline, line_num, end_line) #is this needed?
        if workline <= line_num < end_line:
            workfile.write(line)
        line_num += 1
    workfile.close()
    print('NEXT WORK')
infile.close()
"""
