import json
import re
import sys
import time
from urllib.parse import urlparse

import pandas as pd
import questionary
import requests
from bs4 import BeautifulSoup

api_url = "https://cardfight.fandom.com/api.php"
collected_card_names = []
card_data = []

def get_html(card_name):
    params = {
        "action": "parse",
        "page": card_name,
        "format": "json",
        "prop": "text"
    }

    headers = {
        "User-Agent": "VGBinderApp/1.0"
    }

    response = requests.get(api_url, params=params, headers=headers)
    data = response.json()

    html_content = data["parse"]["text"]["*"]

    soup = BeautifulSoup(html_content, "html.parser")

    return soup

def check_url(url):
    check_url = True
    if "cardfight" in url:
        print("URL is valid")
    else:
        check_url = False
        print("URL is no valid")
    return check_url

def get_name(input_url):
    path = urlparse(input_url).path
    extracted_result = path.strip("/").split("/")[-1]

    if ":" in extracted_result:
        print("Found a colon in the result!")
        names = extract_name(input_url)
        if names:
            collected_card_names.extend(names)
    else:
            collected_card_names.append(extracted_result)


def extract_name(web_url):
    soup = get_html(web_url)

    card_names = []

    for table in soup.find_all("table"):
        headers = [
            th.get_text(strip=True).lower() for th in table.find_all("th")
        ]

        if "name" in headers:
            name_index = headers.index("name")

            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) > name_index:
                    card_name = cells[name_index].get_text(strip=True)

                    clean_name = re.sub(
                        r"\s*[\(\[\{]?\d+[\)\]\}]?\s*$", "", card_name
                    )
                    clean_name = re.sub(r"^\d+x?\s*", "", clean_name).strip()

                    if clean_name and clean_name not in card_names:
                        card_names.append(clean_name)

        collected_card_names.extend(card_names)


def extract_content(card_name):
    soup = get_html(card_name)

    item_to_extract = ["name", "power", "critical", "clan"]
    extract_data = {}

    for row in soup.find_all("tr"):
        first_td = row.find("td")
        if first_td:
            row_label = first_td.get_text().lower()
            for item in item_to_extract:
                if item in row_label:
                    tds = row.find_all("td")
                    if len(tds) >= 2:
                        extract_data[item] = tds[1].get_text(" ", strip=True)

    effect_header = soup.find(
        lambda tag: tag.name in ["th", "td"] and "Card Effect(s)" in tag.text
    )

    if effect_header:
        header_tr = effect_header.find_parent("tr")
        next_tr = header_tr.find_next_sibling("tr") if header_tr else None

        if next_tr:
            extract_data["effect"] = next_tr.get_text("\n", strip=True)
        else:
            extract_data["effect"] = None
    else:
        extract_data["effect"] = None

    return extract_data

def save_as_csv():
    fieldnames = ["name", "power", "critical", "clan", "effect"]

    df = pd.DataFrame(card_data, columns=fieldnames)

    df.to_csv("output_test.csv", index=False, encoding="utf-8")

    print("File save")

def save_as_json():
    with open("data.json", "w") as file:
        json.dump(card_data, file)
    print("File save")

def json_to_csv():
    df = pd.read_json('data.json')
    df.to_csv('output.csv', index=False , encoding='utf-8')
    print("converted")

def main():
    start = questionary.select(
    'Select Option',
    choices=[
        "Start",
        "Exit",
    ]).ask()

    match start:
        case "Start":
            print("Starting")
            extract = questionary.select(
            'Select Option',
            choices=[
                "Content Only",
                "Exit",
            ]).ask()

            match extract:
                case "Content Only":
                   answer = questionary.text("URL pls?").ask()
                   if check_url(answer):
                       get_name(answer)
                       time.sleep(1)
                       for i in collected_card_names:
                           card_data.append(extract_content(i))
                           time.sleep(0.5)
                   else:
                       print("Incorrect URl")
                case "Exit":
                    sys.exit(0)
        case "Exit":
            sys.exit(0)

    testing = questionary.select(
    'Select Option',
    choices=[
        "CSV",
        "JSON",
    ]).ask()

    match testing:
        case "CSV":
            save_as_csv()
        case "JSON":
            save_as_json()

if __name__ == "__main__":
    main()
