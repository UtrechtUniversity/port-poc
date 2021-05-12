"""Test data extraction from Google Browser History .json file"""

import json
import datetime
import numpy as np
import pandas as pd
import re
from zipfile import ZipFile
from io import BytesIO

from google_search_history import __extract
from google_search_history import process

DATA = {
    "Browser History": [
        {
            "page_transition": "LINK",
            "title": "title1",
            "url": "https://www.nu.nl/onderwerp/6131452/titel.html",
            "client_id": "client_id1",
            "time_usec": 1611262800000000},
        {
            "page_transition": "LINK",
            "title": "title1",
            "url": "https://canarias.mediamarkt.es/computer",
            "client_id": "client_id1",
            "time_usec": 1611259200000000},
        {
            "page_transition": "LINK",
            "title": "title1",
            "url": "https://nederland.fm/",
            "client_id": "client_id1",
            "time_usec": 1611432000000000},
        {
            "page_transition": "LINK",
            "title": "title2",
            "url": "https://www.uu.nl/",
            "client_id": "client_id2",
            "time_usec": 1611349200000000},
        {
            "page_transition": "LINK",
            "title": "title3",
            "url": "https://nos.nl/artikel/artikeltitel",
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
            "url": "https://www.nrc.nl/nieuws/2021/05/03/blogX",
            "client_id": "client_id5",
            "time_usec": 1619816400000000},
        {
            "page_transition": "LINK",
            "title": "title6",
            "url": "https://www.bol.com/nl/test",
            "client_id": "client_id6",
            "time_usec": 1619730000000000},
        {
            "page_transition": "LINK",
            "title": "title6",
            "url": "https://www.wehkamp.com/nl/product1",
            "client_id": "client_id6",
            "time_usec": 1619730000000000}
    ]
}


EXPECTED = [
    {'Moment': 'Voor avondklok', 'Website': 'Anders', 'Aantal': 3},
    {'Moment': 'Voor avondklok', 'Website': 'Nieuws', 'Aantal': 1},
    {'Moment': 'Tijdens avondklok', 'Website': 'Anders', 'Aantal': 0},
    {'Moment': 'Tijdens avondklok', 'Website': 'Nieuws', 'Aantal': 1},
    {'Moment': 'Na avondklok', 'Website': 'Anders', 'Aantal': 2},
    {'Moment': 'Na avondklok', 'Website': 'Nieuws', 'Aantal': 1}
]


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
