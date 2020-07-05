import datetime
import bs4


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
