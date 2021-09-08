"""Test data extraction from simulated Google Browser History .json file"""

import random

from pathlib import Path
from pandas.testing import assert_frame_equal
from faker import Faker

from google_search_history import process
from google_search_history.simulation_gsh import __create_website, __create_date, \
    __create_bins, __create_zip, browserhistory

import pandas as pd

SEED = 123

PERIODS = {'before': ["20-10-2020 13:30:00", "23-01-2021 20:59:59"],
           'during': ["23-01-2021 21:00:00", "28-04-2021 04:29:59"]}

URLS_PRE = ['https://macias.com/', 'https://davis.info/', 'https://schaefer.org/',
            'http://jackson-robertson.biz/', 'https://johnston.com/',
            'https://johnson-simmons.com/', 'https://nieuws.nl/',
            'http://www.becker.com/', 'http://adams.com/',
            'https://telegraaf.nl/']

URLS = ['https://johnson-simmons.com/', 'https://davis.info/', 'https://macias.com/',
        'https://nos.nl/', 'https://johnston.com/', 'https://nieuws.nl/',
        'https://schaefer.org/', 'https://telegraaf.nl/', 'http://www.becker.com/',
        'http://adams.com/']

DATES_PRE = [1603514795402199, 1603631814184174, 1603918582202212,
             1604087511327018, 1604515419677343, 1605936247715030,
             1606554235516584, 1607616223263477, 1610217532454797,
             1610621971858733]

DATES = [1611746498925448, 1611864413000000, 1612736624846266,
         1613433337849162, 1614142545833878, 1614155572967477,
         1614183443314904, 1615804895407218, 1618378912170921,
         1618779108275678]

PARTS = {'before': 6, 'during': 7, 'after': 7}

EXPECTED = [
    {'morning': 0, 'afternoon': 0, 'evening': 0,
        'night': 0, 'Curfew': 'before', 'Website': 'news'},
    {'morning': 0, 'afternoon': 1, 'evening': 1,
        'night': 0, 'Curfew': 'during', 'Website': 'news'},
    {'morning': 0, 'afternoon': 0, 'evening': 0,
        'night': 0, 'Curfew': 'post', 'Website': 'news'},
    {'morning': 1, 'afternoon': 0, 'evening': 1,
        'night': 0, 'Curfew': 'before', 'Website': 'other'},
    {'morning': 2, 'afternoon': 0, 'evening': 1,
        'night': 1, 'Curfew': 'during', 'Website': 'other'},
    {'morning': 1, 'afternoon': 1, 'evening': 2,
        'night': 0, 'Curfew': 'post', 'Website': 'other'}
]


def __set_seed():
    random.seed(SEED)
    Faker.seed(str(SEED))


def __create_browserfile():
    __set_seed()
    browserfile = browserhistory(
        num=20, site_diff=0.15, time_diff=0.2, seed=0, fake=True)
    return browserfile


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


def test_create_website_pre():
    __set_seed()
    urls_pre = __create_website(num=10, perc=0.15, fake=True)
    assert urls_pre == URLS_PRE


def test_create_website_during():
    __set_seed()
    urls = __create_website(num=10, perc=0.30, fake=True)
    assert urls == URLS


def test_create_date_pre():
    __set_seed()
    dates_pre = __create_date(num=10, start=PERIODS['before'][0],
                              end=PERIODS['before'][1], time_perc=0)
    assert dates_pre == DATES_PRE


def test_create_date_during():
    __set_seed()
    dates = __create_date(num=10, start=PERIODS['during'][0],
                          end=PERIODS['during'][1], time_perc=0.2)
    assert dates == DATES


def test_create_bins():
    __set_seed()
    parts = __create_bins(20)
    assert parts == PARTS


def test_browserfile():
    file_data = __create_zip(__create_browserfile())
    result = process(file_data)
    expected = __reshape_expected()
    assert_frame_equal(result["data_frames"][0], expected)
