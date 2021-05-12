""" Script to extract info from Google Browser History """

__version__ = '0.1.0'

import json
from datetime import datetime
import numpy as np
import pandas as pd
import re
import zipfile


def __calculate(dates):
    """Per moment-website combination, count web clicks per time unit (morning, afternoon, evening, night)
    Args: 
        dates: Dictionary with dates per website (news vs. other) per moment (pre, during, post curfew)
    Returns:
        results: Dictionary with number of times websites are visted per unit of time
    """
    results = []
    for category in dates.keys():
        sub = {'Morning': 0, 'Afternoon': 0, 'Evening': 0, 'Night': 0}
        sub['Moment'], sub['Website'] = category.split('_')
        for date in dates[category]:
            hour = date.hour
            if 0 <= hour < 6:
                sub['Night'] += 1
            elif 6 <= hour < 12:
                sub['Morning'] += 1
            elif 12 <= hour < 18:
                sub['Afternoon'] += 1
            elif 18 <= hour < 24:
                sub['Evening'] += 1
        sub['Total'] = len(dates[category])
        results.append(sub)
    return results


def __extract(data):
    """Return relevant data from browser history pre, during, and post specific date (in this case 'Dutch curfew')
    Args:
        data: BrowserHistory.json file
    Returns:
        results: List with aggregated extracted data
    """
    # Enter date of event X (in this case 'avondklok')
    date = {'start_curfew': datetime(2021, 1, 23, 21),
            'end_curfew': datetime(2021, 4, 28, 4, 30)}
    # Enter news sites
    newssites = 'news.google.com|nieuws.nl|nos.nl|www.rtlnieuws.nl|nu.nl|at5.nl|ad.nl|bd.nl|telegraaf.nl|volkskrant.nl' \
        '|parool.nl|metronieuws.nl|nd.nl|nrc.nl|rd.nl|trouw.nl'
    # Count number of news vs. other websites per moment (pre/during/after event X)
    dates = {'pre_news': [], 'during_news': [], 'post_news': [],
             'pre_other': [], 'during_other': [], 'post_other': []}
    for data_unit in data["Browser History"]:
        time = datetime.fromtimestamp(data_unit["time_usec"]/1e6)
        if time < date['start_curfew'] and re.findall(newssites, data_unit["url"]):
            dates['pre_news'].append(time)
        elif time > date['end_curfew'] and re.findall(newssites, data_unit["url"]):
            dates['post_news'].append(time)
        elif time < date['start_curfew'] and not re.findall(newssites, data_unit["url"]):
            dates['pre_other'].append(time)
        elif time > date['end_curfew'] and not re.findall(newssites, data_unit["url"]):
            dates['post_other'].append(time)
        elif re.findall(newssites, data_unit["url"]):
            dates['during_news'].append(time)
        elif not re.findall(newssites, data_unit["url"]):
            dates['during_other'].append(time)
    # Calculate times visited per week
    results = __calculate(dates)
    return results


def process(file_data):
    """ Open BrowserHistory.json and return relevant data pre, during, and post specific date (in this case 'Dutch curfew')
    Args:
        file_data: Takeout zipfile
    Returns:
        data_frame: dictionary with summary and csv file with extracted data
    """
    # Read BrowserHistory.json
    with zipfile.ZipFile(file_data) as zfile:
        file_list = zfile.namelist()
        for name in file_list:
            if re.search('BrowserHistory.json', name):
                data = json.loads(zfile.read(name).decode("utf8"))
    # Extract pre/during/post website clicks in dataframe
    data_frame = pd.DataFrame(__extract(data))
    # Save dataframe as csv
    data_frame = data_frame.to_csv(index=False)
    return {
        "summary": f"The following files where read: BrowserHistory.json.",
        "data": data_frame
    }
