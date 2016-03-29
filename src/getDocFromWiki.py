import urllib2
from bs4 import BeautifulSoup
import wikipedia
import sys

print "Topic ",str(sys.argv[1])
soup = BeautifulSoup(urllib2.urlopen('http://en.wikipedia.org/wiki/'+str(sys.argv[1])), "lxml")
links = [(el.get('lang'), el.get('title')) for el in soup.select('li.interlanguage-link > a')]

# This one is for english
wikipedia.set_lang('en')
print "en ",str(sys.argv[1])
page    = wikipedia.page(str(sys.argv[1]))
content = page.content.lower()
f=open('files/'+str(sys.argv[1])+'_en'+'.txt','w')
f.write(content.encode('utf8'))
f.close()

for language, title in links:
    if language not in ['fr']:
        continue
    page_title = title.split(u' - ')[0]
    try:
        print language + ' ' + str(page_title.split(' ')[0])
    except:
        print language + ' '  + str(sys.argv[1])
    wikipedia.set_lang(language)
    page    = wikipedia.page((page_title.split(' ')[0]))
    content = page.content.lower()
    f=open('files/'+str(sys.argv[1])+'_'+str(language)+'.txt','w')
    f.write(content.encode('utf8'))
    f.close()
