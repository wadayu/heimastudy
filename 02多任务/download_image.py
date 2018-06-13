#/usr/bin/python

import re,gevent
import gevent.monkey
import urllib.request
import random

gevent.monkey.patch_all()

f = open('./image.log','rb')
content = f.read().decode('utf-8')
f.close()

url_list = re.findall(r'https://rpic.*\.jpg',content)


def tasks(url):
    res = None
    try:
        res = urllib.request.urlopen(url)
    except Exception as error:
        pass 
    if res:
        image = res.read()
        image_name = str(random.randint(1,100)) + '.jpg'
        with open(image_name,'wb') as f:
            f.write(image)
         

def main():

    gevent.joinall([
        gevent.spawn(tasks,url) for url in url_list
    ])


if __name__ == '__main__':
    main()
