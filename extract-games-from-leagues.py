#!/usr/bin/env python3
import bs4
import urllib.request
import sys
import json

def convert_row(row):
    dat = {}
    cells = row.find_all('td')
    for cell in cells:
        try:
            cell_val = int(cell.text)
        except ValueError:
            cell_val = cell.text
        dat[cell.attrs['data-stat']] = cell_val
        if cell.attrs['data-stat'] == 'boxscore_word' and cell_val == 'boxscore':
            dat['boxscore_url'] = "https://www.pro-football-reference.com" + cell.find('a').attrs['href']
    #dat['boxscore_title'] = str(dat['pts_win']) + "_" + str(dat['pts_lose'])
    if dat['winner'] == "":
        return None
    return dat

data = []

for filename in sys.argv[1:]:
    print(filename, file=sys.stderr)
    with open(filename) as fd:
        soup = bs4.BeautifulSoup(fd, features="lxml")
        #canonical_url = '/'.join(soup.find('link', {'rel': 'canonical'}).attrs['href'].split('/')[0:-1])
        tbody = soup.find_all('tbody')[0]
        rows = tbody.find_all('tr')
        rows = [row for row in rows if 'thead' not in (row.attrs.get('class') or [])]
        data += [convert_row(row) for row in rows]

data = [datum for datum in data if datum is not None]
json.dump(data, sys.stdout)
