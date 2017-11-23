# -*- coding: utf-8 -*-
# Title: crawlerForShareHolding
# Author: EricLX
# Operating Environment: Python 2.X
# Version: 1.0.0
# Date: 22 November, 2017

pimport urllib, urllib2
import datetime
import re

def get_hiddenvalue(url):
    request=urllib2.Request(url)
    reponse=urllib2.urlopen(request)
    resu=reponse.read()
    VIEWSTATE =re.findall(r‘<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />‘, resu,re.I)
    EVENTVALIDATION =re.findall(r‘input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />‘, resu,re.I)
    return VIEWSTATE[0],EVENTVALIDATION[0]

a, b = get_hiddenvalue('http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk')

today = datetime.date.today()
year = today.year
month = today.month
day = today.day
Today = '%s%s%s' % (year, month, day)

myList1 = ['GALAXY ENTERTAINMENT GROUP LIMITED', 'MELCO INTERNATIONAL DEVELOPMENT LIMITED', 'SJM HOLDINGS LIMITED',
           'WYNN MACAU LIMITED', 'SANDS CHINA LTD.', 'MGM CHINA HOLDINGS LIMITED']
myList2 = ['GALAXYENTERTAINMENTGROUPLIMITED', 'MELCOINTERNATIONALDEVELOPMENTLIMITED', 'SJMHOLDINGSLIMITED',
           'WYNNMACAU,LIMITED', 'SANDSCHINALTD.', 'MGMCHINAHOLDINGSLIMITED']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Referer': 'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk'
}

postdata = {
    '__viewstate': a,
    '__VIEWSTATEGENERATOR': '3C67932C',
    '__eventvalidation': b,
    'today': 20171122,
    'sortBy': '',
    'alertMsg': '',
    'ddlShareholdingDay': '17',
    'ddlShareholdingMonth': '03',
    'ddlShareholdingYear': '%s' % (year),
    'btnSearch.x': '%s' % (month),
    'btnSearch.y': '%s' % (day)
}

req.headers = headers
urllib.urlencode(data)
url = 'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk'
req = urllib2.Request(url, data = 'postdata')
html = opener.open(req).read()
html = html.replace(' ', '')
reg1 = r'<tdvalign="top"class="arial12black">\r\n(.*?)\r\n</td>'
reg2 = r'<tdvalign="top"nowrap="nowrap"class="arial12black"style="text-align:right;">\r\n(.*?)\r\n</td>\r\n<tdvalign="top"nowrap="nowrap"class="arial12black"style="text-align:right;">\r\n(.*?)\r\n<'
reg1 = re.compile(reg1, re.S)
reg2 = re.compile(reg2, re.S)
names = re.findall(reg1, html)
values = re.findall(reg2, html)
myDict1 = dict(zip(names, values))
myDict2 = dict(zip(myList2, myList1))

with open('%s.csv' % Today, 'w') as f:
    for item in myList2:
        myString = myDict2[item] + ',' + myDict1[item][0].replace(',', '') + ',' + myDict1[item][1] + ',\n'
        f.write(myString)
