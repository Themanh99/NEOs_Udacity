"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neos = []
    with open(neo_csv_path, "r") as csvfile:
        data = csv.DictReader(csvfile)
        for line in data:
            try:
                neo = NearEarthObject(
                    designation = line["pdes"],
                    name = line["name"] or None,
                    diameter = float(line["diameter"]) if line["diameter"] else None,
                    hazardous=line["pha"] in ["Y", "y", "1"],
                )
            except Exception as ex:
                print(f"Excetion error: {ex}")
            else:
                neos.append(neo)
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    approaches = []
    with open(cad_json_path, "r") as cadfile:
        data = json.load(cadfile)
        for line in data["data"]:
            try:
                approach = CloseApproach(
                    designation = line[0],
                    time = line[3],
                    velocity = float(line[7]),
                    distance = float(line[4]),
                )
            except Exception as ex:
                print(f"Excetion error: {ex}")
            else:
                approaches.append(approach)
    return approaches
