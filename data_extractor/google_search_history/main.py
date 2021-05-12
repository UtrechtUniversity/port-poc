"Main program to test google_semantic_location history script"
from pathlib import Path
import pandas as pd
import io

from google_search_history import process


if __name__ == '__main__':
    """ Process zipfile (file_data) by extracting pre, during, and post event X website clicks """

    file_data = list(Path('.').glob('*.zip'))[0]
    result = process(file_data)
    data_frame = pd.read_csv(io.StringIO(result["data"]), sep=",")
    print(data_frame)
