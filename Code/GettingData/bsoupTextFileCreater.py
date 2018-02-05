#Read the txt file and find the links
#open the each link
#read the content inside the link
#write into a new file
#

import urllib.request
from bs4 import BeautifulSoup
import os
import threading
import time

def webscrap(filepath):
    filecontent = open(filepath, "r", encoding='utf-8').readlines()
    link = "<http://xmlns.com/foaf/0.1/name>"
    wikilinks = set()
    for line in filecontent:
        if line.startswith('#'):
            continue
        if link in line:
            wiki = line.split()[-2].strip('<>').split('?')[0]
            wikilinks.add(wiki)
    for url in wikilinks:
        t1 = threading.Thread(target=crawl, args=(url,))
        #crawl(url)
        t1.start()
   
def crawl(url):
    try:
        urlobj = urllib.request.urlopen(url)
        html = urlobj.read()
        tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'li']
        soup = BeautifulSoup(html, "lxml")
        dirname = "images"
        filename = url.split("/")[-1] + ".txt"
        filename = os.path.join(dirname, filename)
        for tag in soup.findAll(tags):
            paragragph =  tag.get_text()
            with open(filename, "a", encoding='utf-8') as f:
                f.write(paragragph + "\n\n")
        urlobj.close()
    except Exception:
        print("Exception occured " + str(url))

if __name__ == "__main__":
    start = time.time()
    webscrap("Sample_Peoples_Data.txt")
    final = time.time()
    total = final - start
    print("total time of execution is " + str(total))
    
    
	