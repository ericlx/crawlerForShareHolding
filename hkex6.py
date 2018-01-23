# !/user/bin/env python
# -*- coding: utf-8 -*-
# Project: hkex3 - crawler for shareholding
# Version: 6.0.1
# Environment: Python 3.x; chromedriver.exe
# Date: 23/01/2018
# You may get the original codes from:
# https://github.com/ericlx/crawlerForShareHolding/blob/master/hkex6.py
__author__ = 'EricLX'

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import re
import datetime

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

def getEveryDay(begin_date, end_date):
    dateList = []
    beginDate = datetime.datetime.strptime(begin_date, '%Y%m%d')
    endDate = datetime.datetime.strptime(end_date, '%Y%m%d')
    while beginDate <= endDate:
        date_str = beginDate.strftime('%Y%m%d')
        dateList.append(date_str)
        beginDate += datetime.timedelta(days=1)
    return dateList

def obtainDate():
    # Please ensure the format and validity of the date input!
    startingDate = input('Enter the starting date (yyyymmdd format): ')
    endingDate = input('Enter the ending date (yyyymmdd format): ')
    return getEveryDay(startingDate, endingDate)

def printTitle():
    with open('shareholding.csv', 'a') as f:
        f.write(',')
        for key in myList1:
            f.write(key + ',' + '' + ',')
        f.write('\n')
        f.write(',')
        for i in range(len(myList1)):
            f.write('Shareholding,Percentage,')
        f.write('\n')

def main():
    myDateList = obtainDate()
    printTitle()
    url = 'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.set_page_load_timeout(300)
    for date in myDateList:
        myDict = {'ddlShareholdingDay': date[6:],
                  'ddlShareholdingMonth': date[4:6],
                  'ddlShareholdingYear': date[:4]
                  }
        for key in myDict:
            selectDate = Select(driver.find_element_by_name(key))
            selectDate.select_by_visible_text(myDict[key])
            
        forSearch = driver.find_element_by_name("btnSearch")
        forSearch.click()
        result = driver.page_source

        page = result.replace(' ', '').replace('\n', '').replace('\r', '')
        reg1 = '<tdvalign="top"class="arial12black">(.*?)</td>'
        reg2 = '<.*?"text-align:right;">(.*?)</td><.*?"text-align:right;">(.*?)</td>'
        names = re.findall(reg1, page)
        values = re.findall(reg2, page)
        myDict1 = dict(zip(names, values))
        myDict2 = dict(zip(myList2, myList1))

        with open('shareholding.csv', 'a') as f:
            f.write(date + ',')
            for key in myList2:
                myString = myDict1[key][0].replace(',', '') +\
                           ',' + myDict1[key][1] + ','
                f.write(myString)
            f.write('\n')
        sleep(0.5)
    driver.quit()
            
    print("Shareholding data have been saved in shareholding.csv successfully")

if __name__ == '__main__':
    main()
    print('Thanks for using, goodbye')
    toExit = input('Press Enter to exit')
