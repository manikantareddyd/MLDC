import urllib2
from bs4 import BeautifulSoup
import wikipedia
import sys

for topic in ['Adele','Baboon','Chemistry','Energy','pokemon','English_language','French_language','India','Pakistan','Politics','Tennis','The_Beatles','Wikipedia']:
    print "Topic ",topic
    soup = BeautifulSoup(urllib2.urlopen('http://en.wikipedia.org/wiki/'+topic), "lxml")
    links = [(el.get('lang'), el.get('title')) for el in soup.select('li.interlanguage-link > a')]

    This one is for english
    wikipedia.set_lang('en')
    print "en ",topic
    page    = wikipedia.page(topic)
    content = page.content.lower()
    f=open('files/'+topic+'_en'+'.txt','w')
    f.write(content.encode('utf8'))
    f.close()
    languages = ['es','fr']
    for language, title in links:
        if language not in languages:
            continue
        page_title = title.split(u' - ')[0]
        try:
            print language + ' ' + str(page_title.split(' ')[0])
        except:
            print language + ' '  + topic
        wikipedia.set_lang(language)
        page    = wikipedia.page((page_title.split(' ')[0]))
        content = page.content.lower()
        f=open('files/'+topic+'_'+str(language)+'.txt','w')
        f.write(content.encode('utf8'))
        f.close()
