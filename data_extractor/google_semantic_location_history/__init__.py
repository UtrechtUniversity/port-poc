"""Script to extract data from Google Semantic History Location zipfile"""
__version__ = '0.1.0'

import json
import itertools
import re
import zipfile

import pandas as pd
import matplotlib.pyplot as plt 


#######
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
#######

# years and months to extract data for
YEARS = [2016, 2017, 2018, 2019, 2020, 2021]
####### MONTHS = ["JANUARY"]
MONTHS = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]


TEXT = "This study examines the total amount of time spent in activities before and during the COVID-19 pandemic. \
We therefore examined your Google semantic Location History data for 2016, 2017, 2018, 2019, \
2020, and 2021. To be precise, we extracted per month and per year the total hours spent in activities as those were \
recorded by Google such as walking, cycling and running. Also, we extracted \
the number of days spent and the distance in km per activity type. \
All the information we extracted is visible on the following table. On the plot \
you can see the top 5 activities in terms of the overall time spent since 2016 per quarter (Q1 refers to January, February, March)\
Q2 refers to April, May, June, Q3 to July, August, September and Q4 to October, November, December"

def _activityType_duration(data):
    """Get duration per activity type
    Args:
        data (dict): Google Semantic Location History data
    Returns:
        dict: duration per activity type in hours
    """
    activityType_duration = []
    for data_unit in data["timelineObjects"]:
        if "activitySegment" in data_unit.keys():
            try:
                activityType = data_unit["activitySegment"]["activityType"]
                start_time = data_unit["activitySegment"]["duration"]["startTimestampMs"]
                end_time = data_unit["activitySegment"]["duration"]["endTimestampMs"]
                activityType_duration.append(
                    {activityType: (int(end_time) - int(start_time))/(1e3*60*60)})
            except:
                continue
            
    
    # list of activity types
    activities_list = {next(iter(duration)) for duration in activityType_duration}

    # dict of time spend per activity type
    activities = {}
    for activity in activities_list:
        activities[activity] = round(sum(
            [duration[activity] for duration in activityType_duration
                if activity == list(duration.keys())[0]]), 3)

    return activities

def _activity_duration(data):
    """Get total duration of activities
    Args:
        data (dict): Google Semantic Location History data
    Returns:
        float: duration of actitvities in days
    """
    activity_duration = 0.0
    for data_unit in data["timelineObjects"]:
        if "activitySegment" in data_unit.keys():
            start_time = data_unit["activitySegment"]["duration"]["startTimestampMs"]
            end_time = data_unit["activitySegment"]["duration"]["endTimestampMs"]
            activity_duration += (int(end_time) - int(start_time))/(1e3*24*60*60)
    return activity_duration


def _activity_distance(data):
    """Get total distance of activities
    Args:
        data (dict): Google Semantic Location History data
    Returns:
        float: distance of actitvities in km
    """
    activity_distance = 0.0
    for data_unit in data["timelineObjects"]:
        if "activitySegment" in data_unit.keys():
            try:
                activity_distance += int(data_unit["activitySegment"]["distance"])/1000.0
            except:
                continue

    return activity_distance

# This is the new process function
def process(file_data):
    """Return relevant data from zipfile for years and months
    Args:
        file_data: zip file or object

    Returns:
        dict: dict with summary and DataFrame with extracted data
    """
    results = []
    filenames = []

    # Extract info from selected years and months
    with zipfile.ZipFile(file_data) as zfile:
        file_list = zfile.namelist()
        for year in YEARS:
            for month in MONTHS:
                for name in file_list:
                    monthfile = f"{year}_{month}.json"
                    if re.search(monthfile, name) is not None:
                        filenames.append(monthfile)
                        data = json.loads(zfile.read(name).decode("utf8"))

                        activities = _activityType_duration(data)
                        results.append({
                            "Year": year,
                            "Month": month,
                            "Type": dict(itertools.islice(activities.items(), 50)),
                            "Activity Duration [days]": round(_activity_duration(data), 3),
                            "Activity Distance [km]": round(_activity_distance(data), 3)
                        })
                        break

    # Put results in DataFrame
    data_frame = pd.json_normalize(results)

    #output results in a csv file
    #data_frame.fillna(0).to_csv("result.csv")

    return {
        "summary": TEXT,
        "data_frames": [
            data_frame.fillna(0)
        ]
    }

#### This function takes as an input a dataframe, sums the values per column and returns the top columns based on the sum

def top_cols(dftemp,ncols):
    """Get top activities based on the overall time spent
    Args:
        dftemp (dataframe)
    Returns:
        dataframe: dataframe with only the data of the top activities
    """
    dfsum = dftemp.sum().to_frame().reset_index()
    dfsum = dfsum.sort_values(by=0,ascending=False, inplace=False).head(ncols)
    top_cols = dfsum['index'].tolist()
    
    return dftemp[top_cols]

#This function takes as input the resulting dataFrame and prints a barplot of time spent per activity per year
# def activitiesPerYear(dataFrame):
#     """Plot time spent in hours per activity per year
#     Args:
#         dftemp (dataframe)
#     Returns:
#         prints the plot
#     """
    
#     df = dataFrame.drop(columns=['Activity Duration [days]', 'Activity Distance [km]'])
#     actitvities = df.loc[:,df.columns.str.startswith("Type.")].columns
    
#     df = df.groupby(['Year'], as_index =False).sum()
#     print(df)
    
#     df.plot(x="Year", y=actitvities, kind="barh",figsize=(9,8))
#     plt.xlabel("hours")
#     plt.show()
    
    
#This function takes as input the resulting dataFrame and prints a barplot of time spent per top N activity per quarter
def activitiesPerQuarter(dataFrame, N):
    """Plot time spent in hours per top activities (overall top) per quarter
    Args:
        dftemp (dataframe)
    Returns:
        prints the plot
    """
    df = dataFrame.drop(columns=['Activity Duration [days]', 'Activity Distance [km]'])
    
    #Q1 refers to the first three months, that is January, February and March
    #Q2 refers to the April, May, June
    #Q3 refers to July, August, September
    #Q4 refers to October, November and December
    
    Q1 = MONTHS[0:3]
    Q2 = MONTHS[3:6]
    Q3 = MONTHS[6:9]
    Q4 = MONTHS[9:12]
    
    df['Quarter'] = df['Month']
                             
    df['Quarter'].loc[df['Quarter'].isin(Q1)] = 'Q1'
    df['Quarter'].loc[df['Quarter'].isin(Q2)] = 'Q2'
    df['Quarter'].loc[df['Quarter'].isin(Q3)] = 'Q3'
    df['Quarter'].loc[df['Quarter'].isin(Q4)] = 'Q4'
    
    df['Year_quarter'] = df['Month']
    df['Year_quarter'] = df['Year'].astype(str)+'_'+df['Quarter']
        
    df = df.groupby(['Year_quarter'], as_index =False).sum()
    yearQuarter = df['Year_quarter']
    
    #keep only the top N activities based on the time spent overall
    df = top_cols(df.iloc[:, 2:], N)
    topActivities = df.columns
    df = df.join(yearQuarter) 
            
    df.plot(x="Year_quarter", y=topActivities, kind="barh",figsize=(15, 15), width=0.7)
    plt.xlabel("hours")
    plt.show()


