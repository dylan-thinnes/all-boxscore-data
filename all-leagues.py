#!/usr/bin/env python3
import csv
import json
import sys

with open('./all-seasons.csv') as fd:
    reader = csv.reader(fd)
    for raw_year, raw_leagues, _ in reader:
        year = int(raw_year)
        leagues = raw_leagues.split(' ')
        for league in leagues:
            print(f"{year} {league}")
            #print(f"https://www.pro-football-reference.com/years/{year}_{league}/games.htm")
