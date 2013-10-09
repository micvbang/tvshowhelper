import random

import requests
import lxml.html


USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0'
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
               'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',)


def gethtml(query):
    query = query.replace(' ', '+')
    response = requests.get('https://www.google.com/search?ie=utf-8&q={}'.format(query),
                            headers={'User-Agent': random.choice(USER_AGENTS)})
    return response.text

def getimdblink(query):
    html = gethtml(query)
    links = lxml.html.fromstring(html).cssselect('h3.r a')
    if links == []:
        return None
    else:
        return links[0].get('href')
