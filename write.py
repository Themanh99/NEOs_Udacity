"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
import math


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fields = {
                'name': 'Name',
                'designation': 'Designation',
                'distance_au': 'Distance',
                'diameter_km': 'Diameter',
                'datetime_utc': 'Date time',
                'potentially_hazardous': 'hazardous',
                'velocity_km_s': 'Velocity',
            }

    with open(filename, 'w') as fileoutput:
        writer = csv.DictWriter(fileoutput, fields.keys())

        writer.writeheader()

        for result in results:

            cad_data = result.serialize()
            data = {
                'datetime_utc': cad_data['datetime_utc'],'distance_au': cad_data['distance_au'],
                'velocity_km_s': cad_data['velocity_km_s'],'designation': cad_data['neo']['designation'],
                'name': (cad_data['neo']['name'] if cad_data['neo']['name']
                         else 'None'),
                'diameter_km': cad_data['neo']['diameter_km'],'potentially_hazardous': ('True' if cad_data['neo']['potentially_hazardous'] else 'False'),
            }

            writer.writerow(data)

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    data = []
    
    for result in results:
        result_data = result.serialize()
        neo_data = result.neo.serialize()
        
        # Extract necessary information and handle potential None values
        name = neo_data.get('name', '')
        potentially_hazardous = bool(result_data.get('potentially_hazardous'))
        
        # Handle NaN value for diameter_km
        diameter_km = neo_data.get('diameter_km')
        if math.isnan(diameter_km):
            diameter_km = None

        # Create a dictionary with required keys and values
        approach_info = {
            "datetime_utc": result_data['datetime_utc'],
            "distance_au": result_data['distance_au'],
            "velocity_km_s": result_data['velocity_km_s'],
            "neo": {
                "designation": neo_data['designation'],
                "name": name,
                "diameter_km": neo_data['diameter_km'],
                "potentially_hazardous": potentially_hazardous,
            }
        }
        print(neo_data)
        data.append(approach_info)

    # Write the data to the JSON file
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent="\t")