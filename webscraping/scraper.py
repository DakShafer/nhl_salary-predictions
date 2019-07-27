

import requests

from bs4 import BeautifulSoup

from pandas import (
    DataFrame,
    read_html,
    concat
)

from pandas.io.json import json_normalize

import ujson as json


def get_from_capfriendly():
    # the url is very long and annoying but it is necessary
    # in order to retrieve all of the stats

    url = 'https://www.capfriendly.com/browse/active\
           &display=birthday,country,weight,height,weightkg,\
           heightcm,draft,slide-candidate,waivers-exempt,\
           signing-status,expiry-year,performance-bonus,\
           signing-bonus,caphit-percent,aav,length,minors-salary,\
           base-salary,arbitration-eligible,type,signing-age,\
           signing-date,arbitration'

    response = requests.get(url)

    soup = BeautifulSoup(response.text)

    pages = soup.find(attrs={'class': 'r', 'style': 'margin:0 4px 0 0'}).text

    max_page = int(pages[-2:]) + 1

    df = DataFrame()
    for page in range(1, max_page):
        df1 = read_html(url + f'&p={page}')[0]
        df = concat([df, df1],
                    sort=False,
                    ignore_index=True)

    df.to_csv('../data/raw_data/scraped_data.csv',
              index=False)


def roster_by_team_for_year(rosters):
    number_of_teams = len(rosters['teams'])

    output = DataFrame()

    for team in range(number_of_teams):
        data = rosters['teams'][team]

        roster = data['roster']['roster']

        roster = json_normalize(roster, sep='_')

        roster['team'] = data['abbreviation']
        roster['teamFullName'] = data['name']

        output = concat([output, roster],
                        sort=False,
                        ignore_index=True)

    return output


def get_players():
    output = DataFrame()
    for year in range(1990, 2019):
        year_string = str(year) + str(year + 1)
        print(f'scraping --> {year_string}', end='\r')
        try:
            url = f'https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster&season={year_string}'
            resp = requests.get(url=url)
            rosters = json.loads(resp.text)

            all_players = roster_by_team_for_year(rosters)

            all_players['year'] = year_string

            output = concat([output, all_players],
                            sort=False,
                            ignore_index=True)
        except KeyError:
            print(f'SKIPPING LOCKOUT SEASON --> {year_string}')

    return output



