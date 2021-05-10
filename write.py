"""Write a stream of close approaches to CSV or JSON.

This module exports two functions: `write_to_csv`
and `write_to_json`, each of
which accept an `results` stream of close approaches
and a path to which to
write the data.

These functions are invoked by the main module
with the output of the `limit`
function and the filename supplied by the user
at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
from helpers import datetime_to_str


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` to a CSV.

    The precise output specification is in `README.md`.
    Roughly, each output row
    corresponds to the information in a single close
    approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach`
    objects.
    :param filename: A Path-like object pointing
    to where the data should be saved.
    """
    # writing results into new csv file using DictWriter
    fieldnames = ('datetime_utc', 'distance_au',
                  'velocity_km_s', 'designation', 'name',
                  'diameter_km', 'potentially_hazardous')
    with open(filename, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        if results:
            for result in results:
                writer.writerow({
                    'datetime_utc': datetime_to_str(result.time),
                    'distance_au': result.distance,
                    'velocity_km_s': result.velocity,
                    'designation': result.designation,
                    'name': result.neo.name,
                    'diameter_km': result.neo.diameter,
                    'potentially_hazardous': str(result.neo.hazardous)})
        else:
            return


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` to JSON.

    The precise output specification is in `README.md`.
    Roughly, the output is a
    list containing dictionaries, each mapping
    `CloseApproach` attributes to
    their values and the 'neo' key mapping to a
    dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach`
    objects.
    :param filename: A Path-like object pointing
    to where the data should be saved.
    """
    # writing results into new json file busing json.dump
    json_list = []
    if results:
        for result in results:
            d = dict()
            d['datetime_utc'] = datetime_to_str(result.time)
            d['distance_au'] = result.distance
            d['velocity_km_s'] = result.velocity
            d['neo'] = dict()
            d['neo']['designation'] = str(result.neo.designation)
            d['neo']['name'] = str(result.neo.name) if result.neo.name else " "
            d['neo']['diameter_km'] = result.neo.diameter
            d['neo']['potentially_hazardous'] = bool(result.neo.hazardous)
            json_list.append(d)
        with open(filename, 'w') as outfile:
            json.dump(json_list, outfile, indent=2)
    else:
        return
