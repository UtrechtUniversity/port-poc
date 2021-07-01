""" Script to create simulated Google Browser History data """

import random
import string
import time
from datetime import datetime
import numpy as np
import pandas as pd
from faker import Faker

from zipfile import ZipFile
from pathlib import Path
import json


def __createWebsite(n: int, perc: float, fake=False):
    """ Create list with n number of random (news) websites. 
    Args:
        n: int, number of websites you want to generate
        perc: float (0-1), percentage of websites that need to be news websites
        fake: bool, if False existing URLs are selected, if True fake URLs are created
    Return:
        websites: list, created websites in url format
    """
    news = ("news.google.com", "nieuws.nl", "nos.nl", "rtlnieuws.nl", "nu.nl", "at5.nl",
            "ad.nl", "bd.nl", "telegraaf.nl", "volkskrant.nl", "parool.nl", "metronieuws.nl",
            "nd.nl", "nrc.nl", "rd.nl", "trouw.nl")
    if fake:
        websites = [Faker().profile()['website'][0] for i in range(n)]
        for i in range(round(n*perc)):
            websites[i] = f"https://{random.choice(news)}/{'/'.join(websites[i].split('/')[3:])}"
    else:
        urldata = pd.read_csv('tests/data/urldata.csv')
        websites = [random.choice(urldata['url']) for i in range(n)]
        for i in range(round(n*perc)):
            websites[i] = f"{random.choice(news)}/{'/'.join(websites[i].split('/')[1:])}"
        url = 'https://{}'
        websites = [url.format(website) for website in websites]
    return websites


def __randomDate(n: int, start: datetime, end: datetime):
    """ Create random date between given start and end time
    Args:
        n: int, number of dates that need to be created
        start: datetime, earliest date
        end: datetime, latest date
        time_diff: boolean, if True the times will be biased towards evening, if False the times will be random 
    Optional args:
        time_perc: float, if time_diff is True, the time will be biased with the size of time_perc
    Return:
        dates: list, created list of dates
    """
    frmt = '%d-%m-%Y %H:%M:%S'
    stime = datetime.strptime(start, frmt)
    etime = datetime.strptime(end, frmt)
    dates = []
    # create n random times
    for i in range(n):
        dates.append(int(Faker().unix_time(
            end_datetime=etime, start_datetime=stime) * 1e6))
    return dates


def __biasedDate(n: int, start: datetime, end: datetime, time_perc=0):
    """ Creates list with random dates between given start and end time with bias towards evening times
    Args:
        n: int, number of dates that need to be created
        start: datetime, earliest date
        end: datetime, latest date
        time_perc: float, size of certain evening times
    Return:
        dates: list, created list of dates
    """
    frmt = '%d-%m-%Y %H:%M:%S'
    stime = datetime.strptime(start, frmt)
    etime = datetime.strptime(end, frmt)
    dates = []
    # create x evening times and n-x random times
    for i in range(int(n*time_perc)):
        eve = Faker().date_between_dates(date_start=stime, date_end=etime)
        eve_time = time.mktime(eve.timetuple())
        eve_time += random.randint(18, 24) * 60 * 60
        dates.append(int(eve_time*1e6))
    for i in range(n-int(n*time_perc)):
        dates.append(int(Faker().unix_time(
            end_datetime=etime, start_datetime=stime) * 1e6))
    random.shuffle(dates)
    return dates


def __createBins(n):
    """ Randomly distribute n over 3 bins (i.e., number of searches before, during, and after curfew)
    Args:
        n = int, total number of searches that should be in the BrowserHistory file
    Returns:
        bins = list, number of searches that will be generated for before, during, and after curfew
    """
    bin_size = int(n*(1/3))
    before = bin_size + random.randint(0, bin_size) * random.randint(-1, 1)
    during = round((n - before)/2)
    after = n - before - during
    bins = {'before': before, 'during': during, 'after': after}
    return bins


def __createZip(browser_hist):
    """ Saves created BrowserHistory in zipped file
    Args:
        browser_history: json.dumps, created browser history dictionary
    """
    with ZipFile('tests/data/takeout.zip', 'w') as zipped_f:
        zipped_f.writestr("Takeout/Chrome/BrowserHistory.json", browser_hist)


def BrowserHistory(n: int, site_diff: float, time_diff: bool, seed: int, fake=False):
    """ Create simulated BrowserHistory dictionary
    Args:
        n: int, number of browser searches
    Return:
        browser_hist: dict, simulated BrowserHistory
    """
    # set seeds
    random.seed(seed)
    Faker.seed(str(seed))
    # determine size of time difference (% more evening)
    if time_diff:
        time_perc = 0.2
    else:
        time_perc = 0
    # provide transition options
    transition = ("LINK", "GENERATED", "RELOAD")
    # determine time periods: before, during, and after curfew
    periods = {'before': ["20-10-2020 13:30:00", "23-01-2021 20:59:59"],
               'during': ["23-01-2021 21:00:00", "28-04-2021 04:29:59"],
               'after': ["28-04-2021 04:29:59", "23-07-2021 04:50:34"]}
    # create random bin sizes for each time period data
    parts = __createBins(n)
    # create browserhistory data
    results = []
    for moment in periods.keys():
        if moment == 'during':
            perc = 0.15+site_diff
            date = __biasedDate(n=parts[moment], start=periods[moment][0],
                                end=periods[moment][1], time_perc=time_perc)
        else:
            perc = 0.15
            date = __randomDate(n=parts[moment], start=periods[moment][0],
                                end=periods[moment][1])
        url = __createWebsite(n=parts[moment], perc=perc, fake=fake)
        for i in range(parts[moment]):
            results.append({'page_transition': random.choice(transition),
                            'title': Faker().sentence(),
                            'url': url[i],
                            'client_id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
                            'time_usec': date[i],
                            })
    browser_hist = {"Browser History": results}
    return json.dumps(browser_hist)


if __name__ == "__main__":
    file_data = BrowserHistory(
        n=1000, site_diff=0.15, time_diff=True, seed=0, fake=False)
    __createZip(file_data)
