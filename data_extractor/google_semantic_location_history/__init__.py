__version__ = '0.1.0'

import json
import collections
import itertools
import re
import zipfile

import pandas as pd

def process(file_data):
    """Return relevant data from zipfile for years and months
    Args:
        file_data: zip file or object

    Returns:
        pd.DataFrame: DataFrame with relevant info
    """
    years = [2020, 2021]
    months = ["JANUARY"]
    results = []
    filenames = []

    # Extract info from selected years and months
    with zipfile.ZipFile(file_data) as zfile:
        for year in years:
            for month in months:
                for name in zfile.namelist():
                    monthfile = f"{year}_{month}.json"
                    if re.search(monthfile, name) is not None:
                        filenames.append(monthfile)
                        break
                data = json.loads(zfile.read(name).decode("utf8"))
                placevisit_duration = []
                activity_duration = 0.0
                for data_unit in data["timelineObjects"]:
                    if "placeVisit" in data_unit.keys():
                        address = data_unit["placeVisit"]["location"]["placeId"]
                        start_time = data_unit["placeVisit"]["duration"]["startTimestampMs"]
                        end_time = data_unit["placeVisit"]["duration"]["endTimestampMs"]
                        placevisit_duration.append(
                            {address: (int(end_time) - int(start_time))/(1e3*24*60*60)})
                    if "activitySegment" in data_unit.keys():
                        start_time = data_unit["activitySegment"]["duration"]["startTimestampMs"]
                        end_time = data_unit["activitySegment"]["duration"]["endTimestampMs"]
                        activity_duration += (int(end_time) - int(start_time))/(1e3*24*60*60)

                # total time spend visiting places
                place_duration_total = sum(
                    [list(duration.values())[0] for duration in placevisit_duration])

                # list of places visited
                address_list = set([list(duration.keys())[0] for duration in placevisit_duration])

                # dict of time spend per place
                places = {}
                for address in address_list:
                    places[address] = round(sum(
                        [duration[address] for duration in placevisit_duration \
                            if address == list(duration.keys())[0]]), 3)

                # Sort places to amount of time spend
                sorted_places = collections.OrderedDict(
                    sorted(places.items(), key=lambda kv: kv[1], reverse=True))

                results.append({
                    "Year": year,
                    "Month": month,
                    "Top Places": dict(itertools.islice(sorted_places.items(), 3)),
                    "Number of Places": len(address_list),
                    "Places Duration": round(place_duration_total, 3),
                    "Activity Duration": round(activity_duration, 3)
                })

    # Put results in DataFrame
    df = pd.json_normalize(results)

    # Anonymize by replace PlaceIds with numbers
    number = 0
    for column in df.columns:
        if column.split(".")[0] == "Top Places":
            number += 1
            df.rename(columns = {column: f"Place {number}"}, inplace = True )

    return {
        "summary": f"The following files where read: {', '.join(filenames)}.",
        "data": df
    }

if __name__ == '__main__':

    result = process("tests/data/takeout-test.zip")
    print(result)