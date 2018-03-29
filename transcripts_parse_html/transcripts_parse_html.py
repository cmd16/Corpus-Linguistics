from bs4 import BeautifulSoup
import os
import urllib.request


def clean_html_from_foreverdreaming(html_doc, outfile):
    # html_doc = open(input("html doc: "))
    # outfile = open(input("outfile: "), 'w')
    soup = BeautifulSoup(html_doc, 'html.parser')
    table_list = soup.body.find_all("table", limit=2)
    rows = table_list[1].find_all("tr", limit=3)
    data = rows[2].find_all("p")
    for p in data:
        for content in p.contents:
            outfile.write(str(content) + "\n")


def pull_transcripts(doc):
    # doc = urllib.request.urlopen(url)
    # for line in doc:
    #     print(line)
    main_soup = BeautifulSoup(doc, 'html.parser')
    current = main_soup.body.find_all('p')
    for line in current:
        title = line.get_text()
        link = line.span.get("onclick")
        link = link[link.find("'")+1:len(link)-1]
        clean_html_from_foreverdreaming(urllib.request.urlopen(link), open(title + ".txt", 'w'))


def pull_transcripts_from_chakoteya(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    current = soup.body.table.tbody.find_all("tr", limit=3)[2]
    current = current.find_all("td", width='623')[0]
    tables = current.find_all("table")
    for section in tables:
        rows = section.tbody.find_all("tr")
        for i in range(1, len(rows)):
            a = rows[i].td.font.a
            title = a.get_text()
            link = a.get('href')
            link_soup = BeautifulSoup(urllib.request.urlopen("http://www.chakoteya.net/Andromeda/"+link), 'html.parser')
            new_soup = link_soup.body.div
            outfile = open(title + ".txt", 'w')
            outfile.write(new_soup.get_text())
            outfile.close()


def transcript_from_chakoteya(path, names):
    for name in names:
        print(name)
        soup = BeautifulSoup(urllib.request.urlopen(path + name + ".htm"), 'html.parser')
        title = soup.body.font.get_text()
        soup = soup.body.div
        outfile = open(title + ".txt", 'w')
        outfile.write(soup.get_text())


def transcript_from_tk421(path, names, title):
    outfile = open(title + ".txt", 'w')
    for name in names:
        print(name)
        soup = BeautifulSoup(urllib.request.urlopen(path + name + ".html"), 'html.parser')
        paragraphs = soup.find_all("p")
        for idx in range(1, len(paragraphs) - 1):  # ignore first and last paragraphs
            outfile.write(paragraphs[idx].get_text() + '\n')


def book_from_flyingmoose(path, names, title):
    outfile = open(title + ".txt", 'w')
    for name in names:
        print(name)
        soup = BeautifulSoup(urllib.request.urlopen(path + name + ".html"), 'html.parser')
        soup = soup.body.pre
        # print(soup)
        outfile.write(soup.get_text() + '\n***')  # asterisks denote a new chapter


transcript_from_chakoteya("http://www.chakoteya.net/DoctorWho/",
                          ["33-" + str(x) for x in range(15, 17)])

"""
mydir = "/Users/cat/Documents/Movies"
for file in os.listdir(mydir):
    if file.endswith(".html"):
        infilename = os.path.join(mydir, file)
        clean_html_from_foreverdreaming(open(infilename), open(infilename.replace("html", "txt"), 'w'))
"""

# pull_transcripts(open("/Users/cat/Documents/Doctor Who Transcripts Index.html"))
