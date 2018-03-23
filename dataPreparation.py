

import urllib.request
from bs4 import BeautifulSoup
import os
import threading
import time
import shutil
import wikipedia
import re

output_folder = './images'
shutil.rmtree(output_folder, ignore_errors=True)
os.makedirs(output_folder)

def webscrap(wiki):
    #filecontent = open(filepath, "r", encoding='utf-8').readlines()
    wikilinks = set()
    wikilinks.add(wiki)
    for url in wikilinks:
        filename = url.strip().split("/")[-1].replace('_', ' ')
        t1 = threading.Thread(target=wikiread, args=(filename,))
        t2 = threading.Thread(target=info_box, args=(url,))
        t1.start()
        t2.start()

def wikiread(name):
    try:
        page = wikipedia.page(name)
        content = page.content
        filename = os.path.join(output_folder, name+".txt")
        with open(filename, "w", encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print("Exception occured while reading %s" %(e) + str(page.url))

def info_box(url):
    try:
        urlobj = urllib.request.urlopen(url)
        html = urlobj.read()
        soup = BeautifulSoup(html, "lxml")
        table = soup.find('table', {'class' : re.compile("infobox.*")})
        time_string = soup.find('li', id='footer-info-lastmod')
        time_list = time_string.get_text().split(" ")
        modified_date = ' '.join(time_list[7:10])
        print (modified_date)
        tags = ['th', 'td']
        dirname = "images"
        filename = url.strip().split("/")[-1] + "_info.txt"
        filename = os.path.join(dirname, filename)
        for tag in table.findAll(tags):
            paragragph =  tag.get_text()
            with open(filename, "a", encoding='utf-8') as f:
                f.write(paragragph + "\n")
        with open(filename, "a") as f:
            f.write("\n" + time_string.get_text() + "\n")

        urlobj.close()
    except Exception as e:
        print("Exception occured %s" %(e) + str(filename))

if __name__ == "__main__":
    start = time.time()

with open('inputq.csv') as fo:
    next(fo)
    for rec in fo:
      # print rec.split(',')[0] + '-----' + rec.split(',')[1] + '----' + rec.split(',')[3]
      url=rec.split(',')[3]
      webscrap(url)
    final = time.time()
    total = final - start
    print("total time of execution is " + str(total))
