"""Test data extraction from Google Browser History .json file"""

import json
from datetime import datetime
import numpy as np
import pandas as pd
import re
from zipfile import ZipFile
from io import BytesIO

from google_search_history import __extract
from google_search_history import process

DATA = {
    "Browser History": [
        # pre curfew - afternoon (2020-12-1 12:00)
        {
            "page_transition": "LINK",
            "title": "title1",
            "url": "https://canarias.mediamarkt.es/computer",
            "client_id": "client_id1",
            "time_usec": 1606820400000000},
        # pre curfew - night (2020-12-13 02:00)
        {
            "page_transition": "LINK",
            "title": "title1",
            "url": "https://nederland.fm/",
            "client_id": "client_id1",
            "time_usec": 1607821200000000},
        # pre curfew - night (2020-12-20 03:00)
        {
            "page_transition": "LINK",
            "title": "title2",
            "url": "https://www.uu.nl/",
            "client_id": "client_id2",
            "time_usec": 1608429600000000},
        # pre curfew - evening (2021-1-1 19:00)
        {
            "page_transition": "LINK",
            "title": "title3",
            "url": "https://nos.nl/artikel/artikeltitel",
            "client_id": "client_id3",
            "time_usec": 1609524000000000},
        # during curfew - morning (2021-1-24 08:00)
        {
            "page_transition": "LINK",
            "title": "title4",
            "url": "https://www.ns.nl/",
            "client_id": "client_id4",
            "time_usec": 1611471600000000},
        # post curfew - afternoon (2021-4-29 14:00)
        {
            "page_transition": "LINK",
            "title": "title5",
            "url": "https://www.nrc.nl/nieuws/2021/05/03/blogX",
            "client_id": "client_id5",
            "time_usec": 1619697600000000},
        # post curfew - evening (2021-5-1 21:00)
        {
            "page_transition": "LINK",
            "title": "title6",
            "url": "https://www.bol.com/nl/test",
            "client_id": "client_id6",
            "time_usec": 1619895600000000},
        # post curfew - evening (2021-5-10 23:00)
        {
            "page_transition": "LINK",
            "title": "title6",
            "url": "https://www.wehkamp.com/nl/product1",
            "client_id": "client_id6",
            "time_usec": 1620680400000000}
    ]
}

EXPECTED = [{'Morning': 0, 'Afternoon': 0, 'Evening': 1, 'Night': 0,
             'Moment': 'pre', 'Website': 'news', 'Total': 1},
            {'Morning': 0, 'Afternoon': 0, 'Evening': 0, 'Night': 0,
             'Moment': 'during', 'Website': 'news', 'Total': 0},
            {'Morning': 0, 'Afternoon': 1, 'Evening': 0, 'Night': 0,
             'Moment': 'post', 'Website': 'news', 'Total': 1},
            {'Morning': 0, 'Afternoon': 1, 'Evening': 0, 'Night': 2,
             'Moment': 'pre', 'Website': 'other', 'Total': 3},
            {'Morning': 1, 'Afternoon': 0, 'Evening': 0, 'Night': 0,
             'Moment': 'during', 'Website': 'other', 'Total': 1},
            {'Morning': 0, 'Afternoon': 0, 'Evening': 2, 'Night': 0,
             'Moment': 'post', 'Website': 'other', 'Total': 2}]


def __create_zip():
    """
    returns: zip archive
    """
    archive = BytesIO()
    data = DATA
    with ZipFile(archive, 'w') as zip_archive:
        # Create files on zip archive
        with zip_archive.open('Takeout/Chrome/BrowserHistory.json', 'w') as file:
            file.write(json.dumps(data).encode('utf-8'))
    return archive


def test_extract():
    result = __extract(DATA)
    assert result == EXPECTED


def test_process():
    result = process(__create_zip())
    expected = pd.DataFrame(EXPECTED)
    assert result["data"] == expected.to_csv(index=False)
