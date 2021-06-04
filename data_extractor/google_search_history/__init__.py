""" Script to extract info from Google Browser History """

__version__ = '0.1.0'

import json
from datetime import datetime
import numpy as np
import pandas as pd
import re
import zipfile


def __calculate(dates):
    """Per moment-website combination, count web searches per time unit (morning, afternoon, evening, night)
    Args: 
        dates: Dictionary with dates per website (news vs. other) per moment (pre, during, post curfew)
    Returns:
        results: Dictionary with number of times websites are visted per unit of time
    """
    results = []
    for category in dates.keys():
        sub = {'morning': 0, 'afternoon': 0,
               'evening': 0, 'night': 0}
        sub['Curfew'], sub['Website'] = category.split('_')
        for date in dates[category]:
            hour = date.hour
            if 0 <= hour < 6:
                sub['night'] += 1
            elif 6 <= hour < 12:
                sub['morning'] += 1
            elif 12 <= hour < 18:
                sub['afternoon'] += 1
            elif 18 <= hour < 24:
                sub['evening'] += 1
        results.append(sub)
    return results


def __extract(data):
    """Return relevant data from browser history pre, during, and post specific date (in this case 'Dutch curfew')
    Args:
        data: BrowserHistory.json file
    Returns:
        results: List with aggregated extracted data
        earliest: Datetime object of earliest web search
        latest: Datetime object of latest web search
    """
    # Enter date of event X (in this case 'avondklok')
    date = {'start_curfew': datetime(2021, 1, 23, 21),
            'end_curfew': datetime(2021, 4, 28, 4, 30)}
    # Enter news sites
    newssites = 'news.google.com|nieuws.nl|nos.nl|www.rtlnieuws.nl|nu.nl|at5.nl|ad.nl|bd.nl|telegraaf.nl|volkskrant.nl' \
        '|parool.nl|metronieuws.nl|nd.nl|nrc.nl|rd.nl|trouw.nl'
    # Count number of news vs. other websites per moment (pre/during/after event X)
    dates = {'before_news': [], 'during_news': [], 'post_news': [],
             'before_other': [], 'during_other': [], 'post_other': []}
    earliest = datetime.today()
    latest = datetime(2000, 1, 1)
    for data_unit in data["Browser History"]:
        time = datetime.fromtimestamp(data_unit["time_usec"]/1e6)
        if time < earliest:
            earliest = time
        if time > latest:
            latest = time
        if time < date['start_curfew'] and re.findall(newssites, data_unit["url"]):
            dates['before_news'].append(time)
        elif time > date['end_curfew'] and re.findall(newssites, data_unit["url"]):
            dates['post_news'].append(time)
        elif time < date['start_curfew'] and not re.findall(newssites, data_unit["url"]):
            dates['before_other'].append(time)
        elif time > date['end_curfew'] and not re.findall(newssites, data_unit["url"]):
            dates['post_other'].append(time)
        elif re.findall(newssites, data_unit["url"]):
            dates['during_news'].append(time)
        elif not re.findall(newssites, data_unit["url"]):
            dates['during_other'].append(time)
    # Calculate times visited per week
    results = __calculate(dates)
    return results, earliest, latest


def process(file_data):
    """ Open BrowserHistory.json and return relevant data pre, during, and post specific date (in this case 'Dutch curfew')
    Args:
        file_data: Takeout zipfile
    Returns:
        summary: summary of read file(s), earliest and latest websearch
        data: csv file (data_csv) with extracted data
    """
    # Read BrowserHistory.json
    with zipfile.ZipFile(file_data) as zfile:
        file_list = zfile.namelist()
        for name in file_list:
            if re.search('BrowserHistory.json', name):
                data = json.loads(zfile.read(name).decode("utf8"))
    # Message to participant:
    print(f""" 
    With this research we want to invesitgate how news consumption has changed during/after the COVID-19 related Dutch 
    curfew. To examine this, we looked at your Google Search History. First, we divided your browser history into three 
    periods: before the start of the curfew (before {datetime(2021, 1, 23, 21).date()}), during the curfew (between {datetime(2021, 1, 23, 21).date()} and {datetime(2021, 4, 28, 4, 30).date()})
    and post curfew (after {datetime(2021, 4, 28, 4, 30).date()}). For each period, we counted how many times you searched for a news website
    versus any another type of website (i.e., news/other). While counting, we also took the time of day 
    (i.e., morning/afternoon/evening/night) into account. 
    """)
    # Extract pre/during/post website searches, earliest webclick and latest webclick
    results, earliest, latest = __extract(data)
    # Make tidy dataframe of webclicks
    data_frame = pd.melt(pd.DataFrame(results), [
                         "Curfew", "Website"], var_name="Time", value_name="Searches")
    # Save dataframe as csv
    data_csv = data_frame.sort_values(
        ['Curfew', 'Website']).to_csv(index=False)
    print(data_frame.groupby(['Website', 'Curfew', 'Time']).sum())
    print(f"""
    Your earliest web search was on {earliest.date()}, 
    The Dutch curfew took place between {datetime(2021, 1, 23, 21).date()} and {datetime(2021, 4, 28, 4, 30).date()},
    Your latest web search was on {latest.date()}.
    """)
    # Output
    return {
        "summary": {"read_files": "BrowserHistory.json",
                    "earliest_search": earliest.date(),
                    "start_curfew": datetime(2021, 1, 23, 21).date(),
                    "end_curfew": datetime(2021, 4, 28, 4, 30).date(),
                    "latest_search": latest.date()},
        "data": data_csv
    }
