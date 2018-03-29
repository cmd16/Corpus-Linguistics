from bs4 import BeautifulSoup
import urllib.request

def pull_transcript_urls(url):
    soup = BeautifulSoup(urllib.request.urlopen(url))
    current = soup.body.find_all("div", class_="WikiaSiteWrapper", limit=1)[0]
    current = current.section
    current = current.find_all("div", class_="WikiaPageContentWrapper", limit=1)[0]
    current = current.article.div.div
    current = current.find_all("div", id="mw-content-text", limit=1)[0]
    current = current.find_all("div", limit=2)[1]
    current = current.div.div
    current = current.table.tbody.tr
    transcript_urls = []
    for column in current:
        uls = column.find_all("ul")
        for ul in uls:
            link = ul.li.a.get('href')
            transcript_urls.append(link)
    return transcript_urls

def pull_transcript_from_url(url):
    pass