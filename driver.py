import time
import datetime
import bs4

while True:
    now = datetime.datetime.now()
    now_index = str(now.month) + '/' + str(now.day) + '/' + str(now.year) + ' ' + str(now.hour) + ':' + str(now.minute) + 'AM EDT'
    if now.hour == 6:
        exec(open('covid19.py').read())
        with open('index.html') as file:
            txt = file.read()
            soup = bs4.BeautifulSoup(txt, features='lxml')
        for p_tag in soup.find_all('p'):
            if 'Last Updated:' in p_tag.contents[0]:
                p_tag.string = 'Last Updated: ' + now_index
                hi = 0
                with open('index.html', 'w') as f:
                    f.write(str(soup))
    time.sleep(3550)