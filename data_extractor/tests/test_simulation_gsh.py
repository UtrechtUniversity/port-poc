"""Test data extraction from simulated Google Browser History .json file"""

import json
from pathlib import Path
import pandas as pd
from google_search_history import process
from google_search_history.simulation_gsh import browserhistory, __create_zip

PAGE_TRANSITIONS = ['RELOAD', 'GENERATED', 'GENERATED', 'RELOAD',
                    'RELOAD', 'GENERATED', 'LINK', 'LINK', 'RELOAD', 'LINK']

TITLE = ['Explain general put put final sea.',
         'Course child mean increase professional red.',
         'Even land almost few.',
         'Friend send exist.',
         'Management tonight board group page prepare life attention.',
         'Staff author woman large.',
         'Relationship full per leader song whole.',
         'Why at big standard population new population.',
         'Everybody necessary start trade speech person his.',
         'Again notice finally attack threat.']

URL = ['https://king.com/', 'https://ramirez.com/', 'http://www.williams.net/',
       'https://smith-douglas.com/', 'https://news.google.com/', 'https://allen-harrison.com/',
       'http://gomez.net/', 'http://elliott-cook.org/', 'http://www.haney.net/',
       'http://gray.info/']

CLIENT_ID = ['R738M6HFFD', '9TZVFDC4LU', 'PV68R5J2TA', 'L5GUI82QCL', '9RKKEL7H2T',
             'QVNUKGGWXR', 'YEFBCZ3Y4S', '6V8UQX972C', 'EVMGAJZNGP', 'DFZBU6TYAW']

TIME_USEC = [1603873656000000, 1606231079000000, 1610803011000000, 1616108005000000,
             1616787414000000, 1617212190000000, 1618088203000000, 1622865152000000,
             1623528389000000, 1626249594000000]


def __create_browser_file():
    file_data = browserhistory(
        num=10, site_diff=0.15, time_diff=0.2, seed=0, fake=True)
    return file_data


def __read_browser_file():
    file_data = __create_browser_file()
    browser_file = json.loads(file_data)
    return browser_file


def test_zip_file():
    file_data = __create_zip(__create_browser_file())
    assert file_data == Path('tests/data/Takeout.zip')
    assert isinstance(process(file_data)['data_frames'][0], pd.DataFrame)


def test_page_transition():
    browser_file = __read_browser_file()
    page_transitions = [f['page_transition'] for f in browser_file['Browser History']]
    assert page_transitions == PAGE_TRANSITIONS


def test_title():
    browser_file = __read_browser_file()
    title = [f['title'] for f in browser_file['Browser History']]
    assert title == TITLE


def test_url():
    browser_file = __read_browser_file()
    url = [f['url'] for f in browser_file['Browser History']]
    assert url == URL


def test_client_id():
    browser_file = __read_browser_file()
    client_id = [f['client_id'] for f in browser_file['Browser History']]
    assert client_id == CLIENT_ID


def test_time_usec():
    browser_file = __read_browser_file()
    time_usec = [f['time_usec'] for f in browser_file['Browser History']]
    assert time_usec == TIME_USEC
