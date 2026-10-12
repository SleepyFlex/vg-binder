import json

import pandas as pd

"""
Script to save or convert into various file format
"""

def save_as_csv(card_data):
    """
    Save card data as csv

    Parameter:
    card_data (list): list of card items

    Output:
    csv file saved to current dir
    """
    title = ["name", "power", "critical", "clan", "effect"]

    df = pd.DataFrame(card_data, columns=title)

    df.to_csv("output_test.csv", index=False, encoding="utf-8")

    print("File save")

def save_as_json(card_data):
    """
    Save card data as json

    Parameter:
    card_data (list): list of card items

    Output:
    json file saved to current dir
    """
    with open("output.json", "w") as file:
        json.dump(card_data, file)
    print("File save")

def json_to_csv(filename):
    # TODO: Create a function to convert file type
    pass

def main():
    """Example execution"""

    # Sample data
    card_name = [{'name': 'Flogal', 'power': '5000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': None}]

    # Save file as csv
    save_as_csv(card_name)

    # Save file as json
    save_as_json(card_name)

if __name__ == "__main__":
    main()
