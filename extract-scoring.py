#!/usr/bin/env python3
import bs4
import sys
import json
import re

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
        src = fd.read()
        url = re.search('<link rel="canonical" href="(.*?)" />', src, re.DOTALL).group(1)
        scores = [int(t) for t in re.findall('<div class="score">([0-9]+)</div>', src, re.DOTALL)]
        table_src = re.search('<table[^>]*id="scoring".*?>.*?</table>', src, re.DOTALL).group(0)
        soup = bs4.BeautifulSoup(table_src, features="lxml")
        rows = soup.find('tbody').find_all('tr')
        result = {
            'url': url,
            'scores': scores,
            'rows': [convert_row(row) for row in rows]
        }
        #data += [result]
        json.dump(result, sys.stdout)
        print()

#json.dump(data, sys.stdout)
