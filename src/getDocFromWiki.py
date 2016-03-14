import wikipedia
import sys

wikipedia.set_lang(str(sys.argv[1]))
page    = wikipedia.page(str(sys.argv[2]))
content = page.content.lower()
f=open('files/'+str(sys.argv[2])+'.txt','w')
content=f.write(content.encode('utf8'))
f.close()
