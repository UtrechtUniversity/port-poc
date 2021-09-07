"""Test data extraction from simulated Google Browser History .json file"""

import json
from pathlib import Path
import pandas as pd
from google_search_history import process
from google_search_history.simulation_gsh import browserhistory, __create_zip

PAGE_TRANSITIONS = ['GENERATED', 'LINK', 'GENERATED', 'LINK',
                    'RELOAD', 'GENERATED', 'RELOAD', 'GENERATED',
                    'LINK', 'LINK']

TITLE = ['Explain general put put final sea.',
         'Course child mean increase professional red.',
         'Even land almost few.',
         'Budget physical participant exist such accept fund car.',
         'Foreign beautiful structure head lawyer wait instead unit.',
         'Hope mouth score.',
         'Consumer certainly history shoulder recognize address no run.',
         'Tell social grow.',
         'Throughout paper spend.',
         'Meeting character peace road should.']

URL = ['https://www.moore.com/',
       'https://king.com/',
       'https://ramirez.com/',
       'http://morgan.info/',
       'http://www.kramer.info/',
       'https://bd.nl/',
       'https://www.garcia.com/',
       'http://www.moore-lopez.biz/',
       'http://www.thompson.info/',
       'http://www.robinson.com/']

CLIENT_ID = ['V6SK1WJ693', 'L06YQDPV68', 'PSC76D4Z2W', 'CLS7DTZT3T', 'TKD2LIG3B9',
             'RD157467TO', 'SSIHY3PJRX', 'VMGAJZNGPC', '4H3W7VCEG3', 'ON9BA8GEH2']

TIME_USEC = [1603526788000000, 1607198614000000, 1611147602000000, 1612988929000000,
             1614081959000000, 1616418103000000, 1616440546000000, 1622232824000000,
             1624780819000000, 1626878285000000]


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
