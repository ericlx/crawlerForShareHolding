# !/user/bin/env python
# -*- coding: utf-8 -*-
# Project: hkex3 - crawler for shareholding
# Version: 1.1.6
# Environment: Python 3.x; chromedriver.exe
# Date: 15/01/2018
# You may get the original codes from: 
__author__ = 'EricLX'

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
import datetime

# Please ensure the format and validity of the date input!
date = input('Enter the date you need, in yyyymmdd format: ')

# You may update the companies required
# myList1 is the original company names with ',' in the name deleted,
# all other punctuations remain
myList1 = ['GALAXY ENTERTAINMENT GROUP LIMITED',
           'MELCO INTERNATIONAL DEVELOPMENT LIMITED',
           'SJM HOLDINGS LIMITED',
           'WYNN MACAU LIMITED', 'SANDS CHINA LTD.',
           'MGM CHINA HOLDINGS LIMITED']
# myList2 is the corresponding company names with spaces deleted,
# all other punctuations remain
myList2 = ['GALAXYENTERTAINMENTGROUPLIMITED',
           'MELCOINTERNATIONALDEVELOPMENTLIMITED',
           'SJMHOLDINGSLIMITED',
           'WYNNMACAU,LIMITED',
           'SANDSCHINALTD.',
           'MGMCHINAHOLDINGSLIMITED']

def getPage(date):
    # get the desired page information using selenium
    url = 'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.set_page_load_timeout(30)
    myDict = {'ddlShareholdingDay': date[6:],
              'ddlShareholdingMonth': date[4:6],
              'ddlShareholdingYear': date[:4]
              }
    for key in myDict:
        # select desired date in the website using select method from selenium
        # the select_by_visible_text() can also be replaced with other selecting methods
        selectDate = Select(driver.find_element_by_name(key))
        selectDate.select_by_visible_text(myDict[key])
        
    # to click search button
    forSearch = driver.find_element_by_name("btnSearch")
    forSearch.click()
    result = driver.page_source

    # to quit the chromedriver and return the page information
    driver.quit()
    return result

def getDateOfToday():
    # to get the date of today
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    Today = '%s%02d%02d' % (year, month, day)
    return Today

while len(date) < 8:
    # to validate the input date
    date = input('Invalid date input! Please enter again: ')
else:
    if int(date) >= int(getDateOfToday()):
        print("Invalid date input!")
        print("If you are trying to get the data for today, please run hkex1.py")
    elif int(date) < 20170317:
        print("Invalid date input!")
    else:
        # to obtain desired shareholding information for companies in the list
        page = getPage(date).replace(' ', '').replace('\n', '').replace('\r', '')
        reg1 = '<tdvalign="top"class="arial12black">(.*?)</td>'
        reg2 = '<.*?"text-align:right;">(.*?)</td><.*?"text-align:right;">(.*?)</td>'
        names = re.findall(reg1, page)
        values = re.findall(reg2, page)
        myDict1 = dict(zip(names, values))
        myDict2 = dict(zip(myList2, myList1))

        # to write the shareholding information to a .csv file with input date as file name
        with open('%s.csv' % date, 'w') as f:
            for key in myList2:
                myString = myDict2[key] + ',' + myDict1[key][0].replace(',', '') +\
                           ',' + myDict1[key][1] + ',\n'
                f.write(myString)
                
        # pop up the successful notice
        print("Shareholding data have been saved in %s.csv successfully" % date)
