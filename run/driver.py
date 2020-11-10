import datetime
import bs4

# We need imports from covid19.py otherwise it throws a NameError
import pandas as pd
import csv
import urllib.request as request
import matplotlib.pyplot as plt
import numpy as np
import datetime
import math


def update_time(filename):
    now = datetime.datetime.now()
    now_index = str(now.month) + '/' + str(now.day) + '/' + str(now.year) + ' ' + str(now.hour - 5) + ':' + str(
        now.minute) + ' EST'
    with open(filename) as file:
        txt = file.read()
        soup = bs4.BeautifulSoup(txt, features='html.parser')
    for p_tag in soup.find_all('p'):
        if 'Last Updated:' in p_tag.contents[0]:
            p_tag.string = 'Last Updated: ' + now_index
            with open(filename, 'w') as f:
                f.write(str(soup))


def main():

    exec(open('run/covid19.py').read())
    update_time('index.html')
    update_time('global.html')

