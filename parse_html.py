__author__ = 'apollo_bian'
#coding=utf-8

import urllib
from bs4 import BeautifulSoup
import re
import sys
sys.setrecursionlimit(1000000)

class parse_html:
    def __init__(self, url):
        self.html=''
        self.title=''
        self.author=[]
        self.content=''

        self.pre_url = ''
        self.end_num = ''

        self.url = url
        self.need_action = 1
        pass

    def parseContent(self, f=1):
        '''using regular express to search the jpg
        reg = r'src="(.+?\.jpg)" pic_ext'
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        x = 0
        for imgurl in imglist:
            urllib.urlretrieve(imgurl,'%s.jpg' % x)
            x+=1
        '''
        if f == 1:
            page = urllib.urlopen(self.url)
            self.html = page.read()
            soup = BeautifulSoup(self.html)
        else:
            file_handle=open(f)
            data=file_handle.read()
            file_handle.close()
            soup = BeautifulSoup(data)


        #links
        if self.need_action == 1:
            self.need_action=0
            links = soup.find("div", class_='pages')

            start_p = links.find('a')
            start_page = start_p['href']
            #print start_page

            end_p = start_p.find_next_siblings('input')[0].find('a')
            end_page = end_p['href']

            self.pre_url = start_page.split("page")[0]+"page="
            self.end_num = end_page.split("page=")[1]


        #title
        #self.title = soup.title.string.split("草榴社區")[0].strip()
        self.title = soup.title.string.split(u"草榴社區")[0].strip()
        #print self.title
        '''
        author_list = soup.find_all("tr", class_='tr3 tr1')
        '''

        #author
        author_list = soup.select("div.t.t2 table tbody tr th font[face] b")
        for i in range(len(author_list)):
            author_list[i] = str(author_list[i]).replace("<b>", "").replace("</b>","")
        self.author = author_list[0]
        #print self.author

        #content
        content = soup.find_all("div",attrs={"class": "tpc_content"})
        print len(content)
        print type(content[0])

        for i in range(len(content)):
            if content[i] == None:
                print "None, "+i
                continue
            content[i] = str(content[i]).replace("<br><br>", 'apollo-br-br')
            content[i] = content[i].replace('<br>', '')
            content[i] = content[i].replace('</br>', '')
            content[i] = content[i].replace('<br/>', '')
            content[i] = content[i].replace('</div>', '')
            div_tag = re.compile('<div .*>')
            content[i] = div_tag.sub('', content[i])

            content[i] = content[i].replace('<div>', '')
            content[i] = content[i].replace('&nbsp;', '  ')
            content[i] = content[i].replace("apollo-br-br", '\n')
            if author_list[i] == self.author:
                self.content = self.content + '\n\n' + content[i]





    def writeContent(self):
        file=open("d:/test.txt",'w')
        file.write(self.title.encode('utf8'))
        file.write("\n".encode('utf8'))
        file.write(self.author)
        file.write("\n\n\n".encode('utf8'))
        file.write(self.content)
        file.close()

if __name__ == "__main__":
    url='http://cl.bearhk.info/read.php?tid=1513613&page=1'

    pu = parse_html()
    pu.parseContent(data)
#    pu.writeContent()
