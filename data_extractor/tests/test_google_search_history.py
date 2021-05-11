"""Test data extraction from Google Browser History .json file"""

import pandas as pd
from google_search_history import process

DATA = {
    "Browser History": [
        {
            "page_transition": "LINK",
            "title": "title1",
            "url": "https://www.nu.nl/coronavirus/6131452/rivm-afgelopen-week-minder-getest-percentage-positief-stijgt.html",
            "client_id": "client_id1",
            "time_usec": 1611262800000000},
        {
            "page_transition": "LINK",
            "title": "title2",
            "url": "https://www.uu.nl/",
            "client_id": "client_id2",
            "time_usec": 1611349200000000},
        {
            "page_transition": "LINK",
            "title": "title3",
            "url": "https://nos.nl/artikel/2379383-rivm-bezorgd-om-hoge-coronacijfers-onder-40-tot-60-jarigen",
            "client_id": "client_id3",
            "time_usec": 1614373200000000},
        {
            "page_transition": "LINK",
            "title": "title4",
            "url": "https://www.ns.nl/",
            "client_id": "client_id4",
            "time_usec": 1614286800000000},
        {
            "page_transition": "LINK",
            "title": "title5",
            "url": "https://www.nrc.nl/nieuws/2021/05/03/coronablog-4-mei-a4042259",
            "client_id": "client_id5",
            "time_usec": 1619816400000000},
        {
            "page_transition": "LINK",
            "title": "title6",
            "url": "https://www.bol.com/nl/p/jan-van-haasteren-ontbrekende-stukje-puzzel-1000-stukjes/9300000031132593/?bltgh=mjRTtZln6O-wVT40MgZKoA.4_12.13.ProductImage",
            "client_id": "client_id6",
            "time_usec": 1619730000000000}
    ]
}


def test_process():
    result = process(DATA)
    print(result["data"])

    expected = pd.json_normalize([
        {'Moment': 'Na avondklok', 'Website': 'Anders', 'Aantal': 1},
        {'Moment': 'Na avondklok', 'Website': 'Nieuws', 'Aantal': 1},
        {'Moment': 'Tijdens avondklok', 'Website': 'Anders', 'Aantal': 1},
        {'Moment': 'Tijdens avondklok', 'Website': 'Nieuws', 'Aantal': 1},
        {'Moment': 'Voor avondklok', 'Website': 'Anders', 'Aantal': 1},
        {'Moment': 'Voor avondklok', 'Website': 'Nieuws', 'Aantal': 1},
    ])

    assert result["data"] == expected.to_csv(index=False)
