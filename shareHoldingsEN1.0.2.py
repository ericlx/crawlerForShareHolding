# Project Name: ShareholdingEN
# Version: 1.0.2
# Updated: Eric
# Date: 20 March, 2021

# Standard library from Python
import re
import sys
import datetime
from time import sleep

# Library to be installed
import xlrd
import xlwt
import requests
from lxml import etree

# To obtain start and ending date from user input
def obtain_date():
    # Please ensure the format and validity of the date input!
    startingDate = input('Enter the start date (YYYYMMDD format): ')
    endingDate = input('Enter the ending date (YYYYMMDD format): ')
    return startingDate, endingDate, get_every_day(startingDate, endingDate)

# To construct a list including every date from the start to the end
def get_every_day(begin_date, end_date):
    dateList = []
    beginDate = datetime.datetime.strptime(begin_date, '%Y%m%d')
    endDate = datetime.datetime.strptime(end_date, '%Y%m%d')
    while beginDate <= endDate:
        date_str = beginDate.strftime('%Y%m%d')
        dateList.append(date_str)
        beginDate += datetime.timedelta(days=1)
    return dateList

# To extract data required with regular expresseion
def re_extract(reg, html):
    page = html.replace('\n', '').replace('\r', '')
    results = re.findall(reg, page)
    return results

# To get the formdata required for post requests
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

# To get the content of the website using post requests
def get_content(url, form_data):
    response = requests.post(url, data = form_data, headers = headers)
    contents = response.content
    contents_encode = str(contents, encoding = "utf8")
    return(contents_encode)

# To define the headers
def get_headers():
    mozilla = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    apple = 'AppleWebKit/537.36 (KHTML, like Gecko) '
    chrome = 'Chrome/89.0.4389.82 '
    safari = 'Safari/537.36'
    header_content = mozilla + apple + chrome + safari
    headers = {
        'user-agent': header_content
    }

# Main program
if __name__ == '__main__':
    # To obtain user input and define the data required
    sp = int(input('Enter 0 for shares, enter 1 for percentage: '))
    selection = 5
    if sp == 1:
        selection = 7

    # To obtain user input and define the time period
    start, end, datelist = obtain_date()
    number_of_days = 0

    # To define the url to visit and get the headers
    url = 'https://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk'
    headers = get_headers()

    # To set up regular expression
    repl1, repl2, repl3 = ' ' * 40, ' ' * 44, ' ' * 48
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

    # To define the default table title and table name
    title = ['Stock code', 'Stock Name']
    request_list = ['Share', 'Percentage']

    # To obtain the data by date, and store in a dictionary named output
    output = {}
    for date in datelist:
        search_date = '{}/{}/{}'.format(date[:4], date[4:6], date[6:])
        # To pause the program for three seconds
        sleep(3)

        # To skip invalid date
        try:
            title.append(search_date)

            # The content should be a html file from the website
            content = get_content(url, get_form_data(url, headers, search_date))

            # The results should be a list of data ordered by stock code
            results = re_extract(reg, content)

            # The storing process
            for item in results:
                if output.get(int(item[1])):
                    output[int(item[1])].append(item[selection])
                else:
                    output[int(item[1])] = []
                    output[int(item[1])].append(item[3])
                    for i in range(0, number_of_days):
                        output[int(item[1])].append('N/A')
                    output[int(item[1])].append(item[selection])
            print('{} Done!'.format(search_date))
            number_of_days += 1
        except:
            print('Error: {} is not available!'.format(search_date))

    # To trasfer the dictionary to list for further use
    to_excel = []
    for key, value in output.items():
        temp = []
        temp.append(key)
        temp.extend(value)
        to_excel.append(temp)

    # To store all the data in a Excel file
    f = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = f.add_sheet('Shareholdings_{}'.format(request_list[sp]))
    for index, cell in enumerate(title):
        sheet.write(0, index, cell)
    for i, j in enumerate(to_excel):
        for m, n in enumerate(j):
            sheet.write(i + 1, m, n)
    date_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    file_saved = 'ShareholdingEN_{}_{}_at_{}.xls'.format(start, end, date_time)
    file_path = sys.path[0] + '\\' + file_saved
    f.save(file_path)

    # To exit the program
    exiting = input('Completed! Press [Enter] to exit.')
