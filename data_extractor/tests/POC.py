""" Script to create simulated Google Browser History data """

import random
import string
import time
from datetime import datetime
import numpy as np
import pandas as pd

from zipfile import ZipFile
from io import BytesIO
import io
import json

import pingouin as pg
import statsmodels.api as sm
from google_search_history import process
import matplotlib.pyplot as plt
import seaborn as sns


def __createUrl(websites: list):
    """ Place created website into right URL format.
    Args:
        websites: list, created websites
    Return:
        urls: list, created websites in URL format
    """
    url = 'https://{}'
    urls = []
    for website in websites:
        urls.append(url.format(website))
    return urls


def __createWebsite(n: int, perc=0.5):
    """ Create list with n number of random (news) websites. 
    Args:
        n: int, number of websites you want to generate
        perc: float (0-1), percentage of websites that need to be news websites
    Return:
        websites: list, created websites in url format
    """
    urldata = pd.read_csv('data/urldata.csv')
    websites = [random.choice(urldata['url']) for i in range(n)]
    news = ("news.google.com", "nieuws.nl", "nos.nl", "rtlnieuws.nl", "nu.nl", "at5.nl",
            "ad.nl", "bd.nl", "telegraaf.nl", "volkskrant.nl", "parool.nl", "metronieuws.nl",
            "nd.nl", "nrc.nl", "rd.nl", "trouw.nl")
    for i in range(round(n*perc)):
        websites[i] = f"{random.choice(news)}/{'/'.join(websites[i].split('/')[1:])}"
    return __createUrl(websites)


def __randomDate(start: datetime, end: datetime):
    """ Create random date between given start and end time
    Args:
        websites: list, created websites
    Return:
        urls: list, created websites in url format
    """
    frmt = '%d-%m-%Y %H:%M:%S'
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + random.random() * (etime - stime)
    dt = int(time.mktime(time.localtime(ptime)) * 1e6)
    return dt


def __createZip(browser_hist: dict):
    """
    returns: zip archive
    """
    zipped = BytesIO()
    with ZipFile(zipped, 'w') as zip_archive:
        # Create files on zip archive
        with zip_archive.open('Takeout/Chrome/BrowserHistory.json', 'w') as file:
            file.write(json.dumps(browser_hist).encode('utf-8'))
    return zipped


def __createParts(n):
    """ Randomly distribute n over 3 parts (i.e., number of searches before, during, and after curfew)
    Args:
        n = int, total number of searches that should be in the BrowserHistory file
    Returns:
        parts = list, number of searches that will be generated for before, during, and after curfew
    """
    part = int(n*(1/3))
    before = part + random.randint(0, part) * random.randint(-1, 1)
    during = round((n - before)/2)
    after = n - before - during
    parts = {'before': before, 'during': during, 'after': after}
    return parts


def BrowserHistory(n: int):
    """ Create simulated BrowserHistory dictionary
    Args:
        n: int, number of browser searches
    Return:
        browser_hist: dict, simulated BrowserHistory
    """
    transition = ("LINK", "GENERATED", "RELOAD")
    periods = {'before': ["20-10-2020 13:30:00", "23-01-2021 20:59:59"],
               'during': ["23-01-2021 21:00:00", "28-04-2021 04:29:59"],
               'after': ["28-04-2021 04:29:59", "23-07-2021 04:50:34"]}
    parts = __createParts(n)
    results = []
    for moment in periods.keys():
        if moment == 'during':
            perc = 0.8
        else:
            perc = 0.5
        url = __createWebsite(parts[moment], perc)
        for i in range(parts[moment]):
            results.append({'page_transition': random.choice(transition),
                            'title': 'This is the title of the web page',
                            'url': url[i],
                            'client_id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
                            'time_usec': __randomDate(periods[moment][0], periods[moment][1]),
                            })
    browser_hist = {"Browser History": results}
    return __createZip(browser_hist)


if __name__ == "__main__":
    final = pd.DataFrame()
    for i in range(10):
        file_data = BrowserHistory(100)
        overview = pd.read_csv(io.StringIO(
            process(file_data)['data']), sep=",")
        overview['Participant'] = i+1
        final = final.append(overview, ignore_index=True)
    print("Q1: Did news consumption change due to the curfew?")
    sns.pointplot(x='Curfew', y='Searches', hue='Website', data=final)
    plt.show()
    print("""The plot shows that during curfew, as compared to before and after, the searches to news websites increase, 
    while other searches drop.""")
    res_q1 = pg.rm_anova(dv='Searches', within=[
        'Curfew', 'Website'], subject='Participant', data=final, detailed=True)
    res_q1
    print(f"""There's a significant interaction effect of Curfew & Website (T = {res_q1['F'][res_q1['Source'] == 'Curfew * Website'].to_list()[0]}, p = {res_q1['p-unc'][res_q1['Source'] == 'Curfew * Website'].to_list()[0]}). 
    This implies that news consumption has indeed changed due to the curfew""")
    post_hoc = pg.pairwise_ttests(
        dv='Searches', within=['Curfew', 'Website'], subject='Participant', data=final)
    post_hoc
    print(f"""The post-hoc test shows that the number of news searches vs. other searches only significantly differ 
    during the curfew (T = {post_hoc['T'][post_hoc['Curfew'] == 'during'].to_list()[0]}, p = {post_hoc['p-unc'][post_hoc['Curfew'] == 'during'].to_list()[0]}).""")
    # print("Q2: Did the time of news consumption change due to the curfew?")
    # model = sm.MixedLM.from_formula(
    #     "Searches ~ Curfew * Website", groups="Participant", data=final)
    # res_q2 = model.fit()
    # print(res_q2.summary())
