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
    print(f"Processing {path}", file=sys.stderr)
    with open(path) as fd:
        soup = bs4.BeautifulSoup(fd, features="lxml")
        table = soup.find('table', {'id': 'scoring'})
        #print(table)
        rows = table.find('tbody').find_all('tr')
        result = {
            'url': soup.find('link', {'rel': 'canonical'}).attrs['href'].split('/')[-1],
            'scores': [int(score.text) for score in soup.find_all('div', {'class': 'score'})],
            'rows': [convert_row(row) for row in rows]
        }
        #data += [result]
        json.dump(result, sys.stdout)
        print()

#json.dump(data, sys.stdout)
