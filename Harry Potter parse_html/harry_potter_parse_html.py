from bs4 import BeautifulSoup

def clean_html(html_doc, outfile):
    # html_doc = open(input("html doc: "))
    # outfile = open(input("outfile: "), 'w')
    soup = BeautifulSoup(html_doc, 'html.parser')
    main_text = soup.body.div.main.div.pre
    for line in main_text.contents:
        outfile.write(line)

def clean_txt(infile, outfile):
    for line in infile:
        if "Page |" in line:
            continue
        outfile.write(line)

clean_txt(open(input("infile: ")), open(input("outfile: "),'w'))