"Main program to test google_search_history script"
from pathlib import Path
import pandas as pd
import io

from google_search_history import process


if __name__ == '__main__':
    """ Process zipfile (file_data) by extracting pre, during, and post event X website clicks """

    file_data = Path('tests/data/takeout.zip')
    result = process(file_data)
    data_frame = result["data_frames"]
    print(data_frame)
