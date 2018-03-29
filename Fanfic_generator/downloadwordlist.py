import urllib.request
from string import ascii_lowercase


def getWordsFromUrl():
    words = []
    for letter in ascii_lowercase:
        print('getting words that start with', letter)
        words_url = urllib.request.urlopen('http://www.allscrabblewords.com/words-that-start-with/' + letter)
        lines = ""
        for line in words_url:
            lines += str(line)
        lines = lines.split('<')

        for idx in range(len(lines)):
            # print(lines[idx])
            if "Words made by unscrambling" in str(
                    lines[idx]):  # looking at the html reveals only the lines with relevant words include this phrase
                words.append(str(lines[idx][lines[idx].index(
                    '>') + 1:]))  # find the characters after '>'. Those are the characters of the word
    words.sort()
    return words
