import sys
import os
import json
import requests
import logging
from pathlib import Path

# hack to import from top level of repo
print(Path(__file__).parents[2].absolute())
sys.path.append(str(Path(__file__).parents[2].absolute()))
from config import GIT_EXFOR_DICT_URL

def get_latest_dicton(dicton_json):
    # TODO: Update this once there is a release version of the json file
    url = GIT_EXFOR_DICT_URL + '/src/exfor_dictionary/latest.json'

    r = requests.get(url, allow_redirects=True, verify=False)

    if r.status_code == 404:
        logging.error(f"Something wrong with retrieving new dictionary json from the IAEA-NDS.")
        sys.exit()

    open(dicton_json, "wb").write(r.content)
    logging.info(f"dictionary json downloaded")


def get_available_dicton_ids(dicton_file):
    with open(dicton_file, 'r') as f:
        dictons = json.load(f)
        return list(dictons["definitions"].keys())


def extract_survey_list(dicton_json, dicton_id):
    dictons = json.load(f)
    dicton = dictons["dictionaries"].get(dicton_id, {})

    dicton_name = dicton["description"]
    output_filename = f"dicton_{dicton_name.lower().replace(' ', '_')}.md"

    logging.info(f"Extracting description list of {dicton_name}")
    
    descriptions = []

    for d in dicton["codes"].items():

        # Skip non active entries as these can have duplicate descriptions
        if dicton["active"] == False:
            continue

        description = d["description"]

        # sanity check
        if description in descriptions:
            logging.warning(f"Detected duplicate entry '{description}' in '{dicton_name}' dicton.")
            continue
        
        descriptions.append(description)

    item_prefix = "        - "
    descriptions_formatted = "\n".join([item_prefix + d for d in descriptions])

    with open(output_filename, 'w') as f:
        f.writelines(descriptions_formatted)
    logging.info(f"Extracted {dicton_name} dicton as list.")

    return output_filename


def extract_all_survey_lists(dicton_json):
    ids = get_available_dicton_ids(dicton_json)
    return [extract_survey_list(dicton_json, id) for id in ids]


def update():
    dict_filename = "latest_dict.json"
    get_latest_dicton(dict_filename)
    extract_all_survey_lists(dict_filename)


if __name__ == "__main__":
    print(update())

