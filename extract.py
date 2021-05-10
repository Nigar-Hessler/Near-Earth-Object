"""Extract data from CSV and JSON files.

The `load_neos` function extracts NEO data
from a CSV file, formatted as
described in the project instructions,
into a collection of `NearEarthObject`s.

The `load_approaches` function extracts
close approach data from a JSON file,
formatted as described in the project
instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions
with the arguments provided at the command
line, and uses the resulting collections
to build an `NEODatabase`.

You'll edit this file in Task 2.
"""

import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file
    containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # We are making new list of neo collections:
    # open the csv file, skipping the first line of headers,
    # then each row from csv file read into
    # new Near Earth Object, then add this row to collection.
    # Return collection.

    neo_collection = []
    with open(neo_csv_path, 'r') as infile:
        reader = csv.reader(infile)
        next(reader)
        for elem in reader:
            neo = NearEarthObject(elem[3], elem[4], elem[15], elem[7])
            neo_collection.append(neo)
    return neo_collection


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file
    containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # we are making new list of approaches collections:
    # open the json file, each list from the dictionary's
    # key 'data' read into CloseApproach object
    # add into approaches collection. Return list of approaches

    approaches_collection = []
    with open(cad_json_path, 'r') as infile:
        cad_json = json.load(infile)
        for list_of_data in cad_json['data']:
            approach = CloseApproach(list_of_data[0], list_of_data[3], float(
                list_of_data[4]), float(list_of_data[7]))
            approaches_collection.append(approach)
    return approaches_collection
