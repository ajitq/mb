#
class Book(object):
    def __init__(self, name):
        self.name = name
        self.parvas = []

    def __repr__(self):
        return self.name

class Parva(object):
    def __init__(self, name):
        self.name = name
        self.summary = None
        self.chapters = []

    def __repr__(self):
        return self.name
    
    def text(self):
        return '\n'.join([x.text() for x in self.chapters])

class Chapter(object):
    def __init__(self, name):
        self.name = name
        self.ps = []

    def __repr__(self):
        return self.name

    def text(self):
        return '\n'.join([p.get_text() for p in self.ps])

import codecs

filename = 'html-convert/The Mahabharata_ Volume 6.html'
html_doc = codecs.open(filename, encoding='utf-8').read()

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'html.parser')

text = soup.body(id='calibre_link-779')

def remove_footnotes(para):
    for link in para.find_all("a", class_='calibre2'):
        link.clear()

book = Book("Mahabharata Volume 6")
parvas = soup.body(class_='eb04smallcapsmainhead') # e.g. Abhimanyu-Vadha Parva
for parva in parvas:
    p = Parva(parva.text)
    book.parvas.append(p)
    print(parva.text)
    summary = parva.find_next_sibling("blockquote")
    try:
        p.summary = summary(class_="eb19extrafeaturefullout")[2]
    except:
        continue
    try:
        print(p.summary.get_text())
    except:
        continue
    chapters = parva.find_next_siblings(class_='eb07smallcapsmediumhead')
    for c in chapters:
        ch = Chapter(c.text)
        p.chapters.append(ch)
        np = c.next_sibling
        while np and np.name != 'h5':
            if np.name == 'p':
                remove_footnotes(np)
                ch.ps.append(np)
            np = np.next_sibling


def get_stats(book):
    stats = {'parvas':0, 'chapters':0, 'paras':0, 'words':0}
    for p in book.parvas:
        stats['parvas'] += 1
        for c in p.chapters:
            stats['chapters'] += 1
            for pa in c.ps:
                stats['paras'] += 1
                stats['words'] += len(pa.get_text().split())
    return stats

import spacy

spacy.util.set_data_path('e:/spacy/models')
# Load English tokens and dependencies
nlp = spacy.load('en')

parva1 = nlp(book.parvas[1].text())
