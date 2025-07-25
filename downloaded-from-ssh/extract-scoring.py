#!/usr/bin/env python3
import bs4
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
    return dat

data = []
for path in sys.argv[1:]:
    #print(path)
    with open(path) as fd:
        soup = bs4.BeautifulSoup(fd, features="lxml")
        table = soup.find('table', {'id': 'scoring'})
        #print(table)
        rows = table.find('tbody').find_all('tr')
        data += [convert_row(row) for row in rows]

json.dump(data, sys.stdout)
