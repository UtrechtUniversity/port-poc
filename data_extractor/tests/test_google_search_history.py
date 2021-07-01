"""Test data extraction from Google Browser History .json file"""

import json
from datetime import datetime
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
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

EXPECTED = [
    {'morning': 0, 'afternoon': 0, 'evening': 1,
        'night': 0, 'Curfew': 'before', 'Website': 'news'},
    {'morning': 0, 'afternoon': 0, 'evening': 0,
        'night': 0, 'Curfew': 'during', 'Website': 'news'},
    {'morning': 0, 'afternoon': 1, 'evening': 0,
        'night': 0, 'Curfew': 'post', 'Website': 'news'},
    {'morning': 0, 'afternoon': 1, 'evening': 0,
        'night': 2, 'Curfew': 'before', 'Website': 'other'},
    {'morning': 1, 'afternoon': 0, 'evening': 0,
        'night': 0, 'Curfew': 'during', 'Website': 'other'},
    {'morning': 0, 'afternoon': 0, 'evening': 2,
        'night': 0, 'Curfew': 'post', 'Website': 'other'}
]


def __create_zip():
    """
    returns: zip archive
    """
    archive = BytesIO()
    data = DATA
    with ZipFile(archive, 'w') as zip_archive:
        with zip_archive.open('Takeout/Chrome/BrowserHistory.json', 'w') as file:
            file.write(json.dumps(data).encode('utf-8'))
    return archive


def __reshape_expected():
    """
    returns: excpeted outcome to sorted dataframe
    """
    df_expected = pd.melt(pd.DataFrame(EXPECTED),
                          ["Curfew", "Website"],
                          var_name="Time",
                          value_name="Searches")
    expected = df_expected.sort_values(
        ['Curfew', 'Website']).reset_index(drop=True)
    return expected


def test_extract():
    """checks if output of __extract function is as expected
    returns: if no AssertionError, outputs are the same
    """
    result = __extract(DATA)
    assert result[0] == EXPECTED


def test_process():
    """ checks if output of process function is as expected
    returns: if no AssertionError, dataframes are the same
    """
    result = process(__create_zip())
    expected = __reshape_expected()
    assert_frame_equal(result["data_frames"][0], expected)
