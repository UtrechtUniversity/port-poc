"Main program to test google_semantic_location history script"
##### from google_semantic_location_history import process
from __init__ import *


if __name__ == '__main__':
    result = process("tests/data/Location History_Person3.zip")
    #result = process("../tests/data/Person3.zip")
    
    print("Summary:\n", result["summary"])
    print("Dataframe\n", result["data_frames"])
    
    ## code to output the plot
    ## plots the top N activities per quarter (overall top N)
    ## We set N to 5
    print()
    print("Visualisation\n")
    activitiesPerQuarter(result["data_frames"][0], 5)
