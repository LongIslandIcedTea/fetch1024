__author__ = 'apollo_bian'
#coding=utf-8

import urllib
from bs4 import BeautifulSoup
import re

class parse_html:
    def __init__(self):
        self.html=''
        self.title=''
        self.author=''
        self.content=''
        pass

    def getHtml(self, url):
        page = urllib.urlopen(url)
        self.html = page.read()
        print self.html

    def parseContent(self, html):
        '''using regular express to search the jpg
        reg = r'src="(.+?\.jpg)" pic_ext'
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        x = 0
        for imgurl in imglist:
            urllib.urlretrieve(imgurl,'%s.jpg' % x)
            x+=1
        '''
        soup = BeautifulSoup(html)

        #self.tile = soup.title.string.split("草榴社區")[0].strip()
        self.tile = soup.title.string
        print self.title
        self.author = soup.find_all("th ")
        print self.author
        content = soup.find_all("div",attrs={"class": "tpc_content"})
        print len(content)
        print content[0]
        print type(content[1])
        print content[2]

        for i in range(len(content)):
            content[i] = content[i].replace("<br><br>", 'apollo-br-br')
            content[i] = content[i].replace('<br>', '')
            content[i] = content[i].replace('&nbsp;', '  ')
            content[i] = content[i].replace("apollo-br-br", '\n')
            self.content = self.content + '\n\n' + content[i]

    def writeContent(self):
        file=open("d:/test.txt",'w')
        file.writelines(self.title)
        file.writelines(self.author)
        file.writelines("\n\n\n")
        file.writelines(self.content)
        file.close()

if __name__ == "__main__":
    url='http://cl.bearhk.info/read.php?tid=1513613&page=1'
    file=open("d:/a.htm",'r')
    data=file.read()
    file.close()
    pu = parse_html()
    pu.parseContent(data)
    pu.writeContent()
