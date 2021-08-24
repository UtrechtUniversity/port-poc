from datetime import datetime, timezone
from google_semantic_location_history.simulation_gslh import create_places, update_data, fake_data


ACTIVITY_DATA = {
    "timelineObjects" : [ {
        "activitySegment" : {
            "duration" : {
                "startTimestampMs" : "86400000",
                "endTimestampMs" : "302400000"
            },
			'startLocation': {
				'latitudeE7': 1,
				'longitudeE7': 2
			},
			'endLocation': {
				'latitudeE7': 3,
				'longitudeE7': 4
			},            
            "distance" : 1000,
        }
    }, {
        "activitySegment" : {
            "duration" : {
                "startTimestampMs" : "0",
                "endTimestampMs" : "43200000"
            },
			'startLocation': {
				'latitudeE7': 1,
				'longitudeE7': 1
			},
			'endLocation': {
				'latitudeE7': 2,
				'longitudeE7': 2
			},              
            "distance" : 500,
        }
    },
]}

VISIT_DATA = {
    "timelineObjects" : [ {
        "placeVisit" : {
            "location" : {
                "placeId" : "placeX"
            },
            "duration" : {
                "startTimestampMs" : "0",
                "endTimestampMs" : "86400000"
            }
        }
    }, {
        "placeVisit" : {
            "location" : {
                "placeId" : "placeZ"
            },
            "duration" : {
                "startTimestampMs" : "0",
                "endTimestampMs" : "21600000"
            }
        }
    }, {
        "placeVisit" : {
            "location" : {
                "placeId" : "placeY"
            },
            "duration" : {
                "startTimestampMs" : "0",
                "endTimestampMs" : "43200000"
            }
        }
    }, {
        "placeVisit" : {
            "location" : {
                "placeId" : "placeA"
            },
            "duration" : {
                "startTimestampMs" : "0",
                "endTimestampMs" : "10000000"
            }
        }
    }
]}

PLACES = {
        'b1-5003748L': {'name': 'Reimes BV', 'address': 'Hannahring 17\n1669SC\nKruiningen', 'latitude': 51.45581, 'longitude': 5.550007},
        'V1-2419116P': {'name': 'Medtronic', 'address': 'Aylinhof 7\n8533SB\nRidderkerk', 'latitude': 51.463845, 'longitude': 5.4707}
    }


def test_create_places():
    result = create_places(total=2, seed=1)

    assert result == PLACES


def test_update_data_visit():

    result = update_data(VISIT_DATA, datetime(2020, 1, 1, tzinfo=timezone.utc), PLACES, seed=1)
    expected = {
        'timelineObjects': [{
            'placeVisit': {
                'location': {
                    'placeId': 'b1-5003748L',
                    'address': 'Hannahring 17\n1669SC\nKruiningen',
                    'name': 'Reimes BV',
                    'latitudeE7': 514558100,
                    'longitudeE7': 55500070
                },
                'duration': {
                    'startTimestampMs': '1577836800000',
                    'endTimestampMs': '1577841085440'
                }
            }
        }, {
            'placeVisit': {
                'location': {
                    'placeId': 'V1-2419116P',
                    'address': 'Aylinhof 7\n8533SB\nRidderkerk',
                    'name': 'Medtronic',
                    'latitudeE7': 514638450,
                    'longitudeE7': 54707000
                },
                'duration': {
                    'startTimestampMs': '1577841085440',
                    'endTimestampMs': '1577845370880'
                }
            }
        }, {
            'placeVisit': {
                'location': {
                    'placeId': 'V1-2419116P',
                    'address': 'Aylinhof 7\n8533SB\nRidderkerk',
                    'name': 'Medtronic',
                    'latitudeE7': 514638450,
                    'longitudeE7': 54707000
                },
                'duration': {
                    'startTimestampMs': '1577845370880',
                    'endTimestampMs': '1577849656320'
                }
            }
        }, {
            'placeVisit': {
                'location': {
                    'placeId': 'b1-5003748L',
                    'address': 'Hannahring 17\n1669SC\nKruiningen',
                    'name': 'Reimes BV',
                    'latitudeE7': 514558100,
                    'longitudeE7': 55500070
                },
                'duration': {
                    'startTimestampMs': '1577849656320',
                    'endTimestampMs': '1577853941760'
                }
            }
        }]
    }

    assert result == expected


def test_update_data_activity():

    result = update_data(ACTIVITY_DATA, datetime(2020, 1, 1, tzinfo=timezone.utc), PLACES, seed=1)

    expected = {
        'timelineObjects': [{
            'activitySegment': {
                'duration': {
                    'startTimestampMs': '1577836800000',
                    'endTimestampMs': '1577837871360',
                    'activityType': 'IN_VEHICLE'
                },
                'startLocation': {
                    'latitudeE7': 514558100,
                    'longitudeE7': 55500070
                },
                'endLocation': {
                    'latitudeE7': 514638450,
                    'longitudeE7': 514638450
                },
                'distance': 5583
            }
        }, {
            'activitySegment': {
                'duration': {
                    'startTimestampMs': '1577837871360',
                    'endTimestampMs': '1577838942720',
                    'activityType': 'WALKING'
                },
                'startLocation': {
                    'latitudeE7': 514638450,
                    'longitudeE7': 54707000
                },
                'endLocation': {
                    'latitudeE7': 514558100,
                    'longitudeE7': 514558100
                },
                'distance': 5583
            }
        }]
    }

    assert result == expected
