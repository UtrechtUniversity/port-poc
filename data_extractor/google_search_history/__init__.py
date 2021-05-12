""" Script to extract info from Google Browser History """

__version__ = '0.1.0'

import json
import datetime
import numpy as np
import pandas as pd
import re
import zipfile


def __extract(data):
    """Return relevant data from browser history pre, during, and post specific date (in this case 'Dutch curfew')
    Args:
        data: BrowserHistory.json file
    Returns:
        results: List with aggregated extracted data
    """
    # Enter date of event X (in this case 'avondklok')
    date = {'start_curfew': np.datetime64(datetime.datetime(2021, 1, 23, 21)).view('<i8'),
            'end_curfew': np.datetime64(datetime.datetime(2021, 4, 28, 4, 30)).view('<i8')}

    # Enter news sites
    newssites = 'news.google.com|nieuws.nl|nos.nl|www.rtlnieuws.nl|nu.nl|at5.nl|ad.nl|bd.nl|telegraaf.nl|volkskrant.nl' \
        '|parool.nl|metronieuws.nl|nd.nl|nrc.nl|rd.nl|trouw.nl'

    # Count number of news vs. other websites per moment (pre/during/after event X)
    results = {'Moment': [], 'Website': []}
    pre_news = during_news = post_news = pre_other = during_other = post_other = 0
    for data_unit in data["Browser History"]:
        if data_unit["time_usec"] < date['start_curfew'] and re.findall(newssites, data_unit["url"]):
            pre_news += 1
        elif data_unit["time_usec"] > date['end_curfew'] and re.findall(newssites, data_unit["url"]):
            post_news += 1
        elif data_unit["time_usec"] < date['start_curfew'] and not re.findall(newssites, data_unit["url"]):
            pre_other += 1
        elif data_unit["time_usec"] > date['end_curfew'] and not re.findall(newssites, data_unit["url"]):
            post_other += 1
        elif re.findall(newssites, data_unit["url"]):
            during_news += 1
        elif re.findall(newssites, data_unit["url"]):
            during_other += 1

    # Put results in dictionary
    results = [
        {'Moment': 'Pre curfew', 'Website': 'Anders', 'Count': pre_other},
        {'Moment': 'Pre curfew', 'Website': 'Nieuws', 'Count': pre_news},
        {'Moment': 'During curfew', 'Website': 'Anders', 'Count': during_other},
        {'Moment': 'During curfew', 'Website': 'Nieuws', 'Count': during_news},
        {'Moment': 'Post curfew', 'Website': 'Anders', 'Count': post_other},
        {'Moment': 'Post curfew', 'Website': 'Nieuws', 'Count': post_news}
    ]

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
