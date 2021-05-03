from google_semantic_location_history import process
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data"

def test_gslh():
    result = process(DATA_PATH.joinpath("takeout-test.zip").open("rb"))
    assert result["summary"] == 'The following files where read: 2020_JANUARY.json, 2021_JANUARY.json.'

