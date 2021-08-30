"""Test data extraction from simulated Google Browser History .json file"""

import json
from google_search_history.simulation_gsh import browserhistory, __create_zip
from pandas.testing import assert_frame_equal

PAGE_TRANSITIONS = ['GENERATED', 'RELOAD', 'RELOAD', 'LINK', 'GENERATED', 'LINK', 'RELOAD', 'GENERATED', 'LINK', 'LINK']

TITLE = ['Explain general put put final sea.',
        'Course child mean increase professional red.',
        'Even land almost few.', 'Friend send exist.',
        'Management tonight board group page prepare life attention.',
        'Staff author woman large.',
        'Relationship full per leader song whole.',
        'Something why at big.',
        'Population new population life.',
        'Necessary start trade speech person.']

URL = ['https://ramirez.com/',
        'http://www.williams.net/',
        'https://king.com/',
        'http://gomez.net/',
        'https://smith-douglas.com/',
        'https://allen-harrison.com/',
        'https://nos.nl/',
        'https://sanders-thompson.com/',
        'https://reynolds-davis.com/',
        'https://www.ross-gonzalez.com/']

CLIENT_ID = ['FD29TZVFDC',
            'LUMLXHTPSC',
            '6D4Z2WW3L0',
            'KKEL7H2TKD',
            'LIG3B9JCYE',
            '7467TOZJ34',
            'V8UQX972CW',
            'PC24H3W7VC',
            'WVUON9BA8G',
            'R0CYTW4CCK']

TIME_USEC = [1603877460000000,
            1606173360000000,
            1605382200000000,
            1616043300000000,
            1618077060000000,
            1617200040000000,
            1618891920000000,
            1623489660000000,
            1624207560000000,
            1622857020000000]


def __create_browser_file():
    file_data = browserhistory(
        num=10, site_diff=0.15, time_diff=True, seed=0, fake=True)
    browser_file = json.loads(file_data)
    return browser_file


def test_page_transition():
    browser_file = __create_browser_file()
    page_transitions = [f['page_transition'] for f in browser_file['Browser History']]
    assert page_transitions == PAGE_TRANSITIONS


def test_title():
    browser_file = __create_browser_file()
    title = [f['title'] for f in browser_file['Browser History']]
    assert title == TITLE


def test_url():
    browser_file = __create_browser_file()
    url = [f['url'] for f in browser_file['Browser History']]
    assert url == URL


def test_client_id():
    browser_file = __create_browser_file()
    client_id = [f['client_id'] for f in browser_file['Browser History']]
    assert client_id == CLIENT_ID


def test_time_usec():
    browser_file = __create_browser_file()
    time_usec = [f['time_usec'] for f in browser_file['Browser History']]
    assert time_usec == TIME_USEC
