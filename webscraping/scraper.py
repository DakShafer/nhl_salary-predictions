

import requests
from bs4 import BeautifulSoup
from pandas import (
    DataFrame,
    read_html,
    concat
)


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

    response = requests.get(URL)

    soup = BeautifulSoup(response.text)

    pages = soup.find(attrs={'class': 'r', 'style': 'margin:0 4px 0 0'}).text

    max_page = int(pages[-2:]) + 1

    df = DataFrame()
    for page in range(1, max_page):
        df1 = read_html(url + f'&p={page}')[0]
        df = concat([df, df1], sort=False, ignore_index=True)

    df.to_csv('../data/raw_data/scraped_data.csv', index=False)



