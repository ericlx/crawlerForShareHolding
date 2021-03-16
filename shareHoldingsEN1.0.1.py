# Project Name: ShareholdingEN
# Version: 1.0.1
# Updated: Eric
# Date: 16 March, 2021

import re
import sys
import xlrd
import xlwt
import datetime
import requests
from lxml import etree
from time import sleep

def get_every_day(begin_date, end_date):
    dateList = []
    beginDate = datetime.datetime.strptime(begin_date, '%Y%m%d')
    endDate = datetime.datetime.strptime(end_date, '%Y%m%d')
    while beginDate <= endDate:
        date_str = beginDate.strftime('%Y%m%d')
        dateList.append(date_str)
        beginDate += datetime.timedelta(days=1)
    return dateList

def obtain_date():
    # Please ensure the format and validity of the date input!
    startingDate = input('Enter the starting date (yyyymmdd format): ')
    endingDate = input('Enter the ending date (yyyymmdd format): ')
    return startingDate, endingDate, get_every_day(startingDate, endingDate)

def get_form_data(url, headers, search_date):
    response = requests.get(url, headers = headers)
    sel = etree.HTML(response.content)
    VIEW = sel.xpath('//input[@name="__VIEWSTATE"]/@value')
    GENERATOR = sel.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value')
    EVENT = sel.xpath('//input[@name="__EVENTVALIDATION"]/@value')
    today = sel.xpath('//input[@name="today"]/@value')

    form_data = {
        '__VIEWSTATE' : VIEW,
        '__VIEWSTATEGENERATOR' : GENERATOR,
        '__EVENTVALIDATION' : EVENT,
        'today' : today,
        'sortBy' : 'stockcode',
        'sortDirection' : 'asc',
        'alertMsg' : '',
        'txtShareholdingDate': search_date,
        'btnSearch': 'Search'
    }

    return(form_data)

def get_content(url, form_data):
    response = requests.post(url, data = form_data, headers = headers)
    contents = response.content
    contents_encode = str(contents, encoding = "utf8")
    return(contents_encode)

url = 'https://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk'

mozilla = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
apple = 'AppleWebKit/537.36 (KHTML, like Gecko) '
chrome = 'Chrome/89.0.4389.82 '
safari = 'Safari/537.36'
header_content = mozilla + apple + chrome + safari

headers = {
    'user-agent': header_content
}

repl1 = '                                        '
repl2 = '                                            '
repl3 = '                                                '

reg = f'''\
<tr>\
{repl2}<td class="col-stock-code">\
{repl3}<div class="mobile-list-heading">(.*?)</div>\
{repl3}<div class="mobile-list-body">(.*?)</div>\
{repl2}</td>\
{repl2}<td class="col-stock-name">\
{repl3}<div class="mobile-list-heading">(.*?)</div>\
{repl3}<div class="mobile-list-body">(.*?)</div>\
{repl2}</td>\
{repl2}<td class="col-shareholding">\
{repl3}<div class="mobile-list-heading">(.*?)</div>\
{repl3}<div class="mobile-list-body">(.*?)</div>\
{repl2}</td>\
{repl2}<td class="col-shareholding-percent">\
{repl3}<div class="mobile-list-heading">(.*?)</div>\
{repl3}<div class="mobile-list-body">(.*?)</div>\
{repl2}</td>\
{repl1}</tr>\
'''
f = xlwt.Workbook(encoding='utf-8', style_compression=0)
start, end, datelist = obtain_date()

for date in datelist:
    search_date = '{}/{}/{}'.format(date[:4], date[4:6], date[6:])

    try:
        content = get_content(url, get_form_data(url, headers, search_date))
        page = content.replace('\n', '').replace('\r', '')
        results = re.findall(reg, page)

        sheet = f.add_sheet(search_date.replace('/',''))

        for i in range(0, 8, 2):
            sheet.write(0, i // 2, results[0][i])

        for index, item in enumerate(results):
            for i in range(1, 8, 2):
                cell = item[i].replace(',','').replace('%','')
                sheet.write(index + 1, i // 2, cell.strip())
                
        print('{} Done!'.format(search_date))
        
    except:
        print('Error: {} is not available!'.format(search_date))
    
    sleep(3)

date_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
file_saved = 'ShareholdingEN_{}_{}_at_{}.xls'.format(start, end, date_time)
file_path = sys.path[0] + '\\' + file_saved
f.save(file_path)
