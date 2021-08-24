--------------
Data Extractor
--------------

This is a basic template which can be used to write a data extractor. The
extraction logic should be placed in the ``process`` function within
``data_extractor/__init__.py``. An example has been provided.

The argument that the ``process`` function receives is a file-like object. It can
therefore be used with most regular Python libraries. The example demonstrates
this by usage of the ``zipfile`` module.

This project makes use of `Poetry`_. It makes creating the required Python
Wheel a straigh-forward process. Install Poetry with the following command:
``pip install poetry``.

The behavior of the ``process`` function can be verified by running the tests.
The test are located in the ``tests`` folder. To run the tests execute:
``poetry run pytest``.

To run the extraction code from the browser run: 
``python3 -m http.server`` from the root folder (the one with
``.git``). This will start a webserver on: 
`localhost <http://localhost:8000>`__.

Opening a browser with that URL will initialize the application. After it has
been loaded a file can be selected. The output of the `process` function will
be displayed after a while (depending on the amount of processing required and
the speed of the machine).

.. _Poetry: https://python-poetry.org/

--------------
Google Semantic Location History
--------------
In this example, we first create simulated Google Semantic Location History (GSLH) data and then extract relevant information from the simulated data.

Data simulation
--------------
Command:
``poetry run python google_semantic_location_history/simulation_gslh.py``

This generates fake GSLH data using the python libraries [GenSON](https://pypi.org/project/genson/), [Faker](https://github.com/joke2k/faker), and [faker-schema](https://pypi.org/project/faker-schema/).

First, generate a JSON schema from a JSON object using ``GenSON's SchemaBuilder`` class. The JSON object is derived from an example GSLH data package, downloaded from Google Takeout. The GSLH data package consists of monthly JSON files with information on e.g. geolocations, addresses and time spend in places and in activity. The JSON schema describes the format of the JSON files, and can be used to generate fake data with the same format. This is done by converting the JSON schema to a custom schema expected by ``faker-schema`` in the form of a dictionary, where the keys are field names and the values are the types of the fields. The values represent available data types in `Faker`, packed in so-called providers. ``Faker`` provides a wide variety of data types via providers, for example for names, addresses, and geographical data. This allows us to easily customize the faked data to our specifications.

This creates a zipfile with the simulated Google Semantic Location History data in ``tests/data/Location History.zip``.

Data extraction
--------------
Command:
``poetry run python google_semantic_location_history/main.py``

This extracts and displays the relevant data and summary. It calls the same ``process`` function as the web application would. To use the GSLH data extraction script in the web application, one needs to specify this in ``pyworker.js``.

