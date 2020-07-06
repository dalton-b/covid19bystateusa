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


def update():
    _now = datetime.datetime.now()
    now_index = str(_now.month) + '/' + str(_now.day) + '/' + str(_now.year) + ' ' + str(_now.hour - 4) + ':' + str(
        _now.minute) + ' EDT'
    exec(open('covid19.py').read())
    with open('index.html') as file:
        txt = file.read()
        soup = bs4.BeautifulSoup(txt, features='html5lib')
    for p_tag in soup.find_all('p'):
        if 'Last Updated:' in p_tag.contents[0]:
            p_tag.string = 'Last Updated: ' + now_index
            with open('index.html', 'w') as f:
                f.write(str(soup))


update()
