"Main program to test google_semantic_location history script"
import io
import pandas as pd
from google_semantic_location_history import process


if __name__ == '__main__':

    result = process("tests/data/Location History.zip")
    data_frame = df = pd.read_csv(io.StringIO(result["data"]), sep=",")
    print(data_frame)
