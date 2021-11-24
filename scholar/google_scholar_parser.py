#!/usr/bin/env python3

import sys
import datetime
from bs4 import BeautifulSoup
import urllib.request
import time

BASE_URL='https://scholar.google.com'
SEARCH_URL='https://scholar.google.co.in/citations?hl=en&user={}&view_op=list_works&sortby=pubdate'
RESULT_FMT='''# {title}
 - authors: {authors}
 - published in: {venue}
 - year: {year}
 - {link}
'''

def parse_info(soup):
    paper_box = soup.find_all('a', attrs={'class': 'gsc_a_at'})
    link = [paper['href'] for paper in paper_box]
    paper = [paper.text.strip() for paper in paper_box]
    author_box = soup.find_all('div', attrs={'class': 'gs_gray'})
    author = [author.text.strip() for author in author_box]
    year_box = soup.find_all('span', attrs={'class': 'gsc_a_h gsc_a_hc gs_ibl'})
    year = [year.text.strip() for year in year_box]

    return paper, link, author, year

def print_publications(num, paper, link, author, year):
    for _ in range(num):
        print(RESULT_FMT.format(
            title=paper.pop(0), venue=author.pop(0), authors=author.pop(0), year=year.pop(0), link=BASE_URL+link.pop(0)))

def check_year(time_period, year_list):
    year = []
    for item in year_list:
        if int(item) in time_period:
            year.append(item)

    return year

if __name__ == "__main__":
    author = sys.argv[1]

    time_period = []
    current_year = datetime.datetime.now().year
    time_period.append(current_year)
    time_period.append(current_year - 1)

    quote_page = SEARCH_URL.format(author)

    page = urllib.request.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    paper, link, author, year_list = parse_info(soup)
    year = check_year(time_period, year_list)
    num = len(year)

    print_publications(num, paper, link, author, year)
