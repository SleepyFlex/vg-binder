import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from rich.progress import track

'''
This script helps scrape content from the web based on user url
'''

api_url = "https://cardfight.fandom.com/api.php"
card_data = []
card_names = []

def get_html(title) -> BeautifulSoup:
    """
    Get the whole html content of the page

    Parameter:
    title (str): the last part of the page url link

    Returns:
    BeautifulSoup: the parsed HTML content of the page
    """

    params = {
        "action": "parse",
        "page": title,
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

    time.sleep(0.4)

    return soup

def check_url(page_url) -> bool:
    # TODO: Add more error proofing for diff problem
    """
    Check if the URL is valid for scraping

    Parameter:
    page_url (str): the page url link
    """

    check_url = True
    if "cardfight" in page_url:
        print("URL is valid")
    else:
        check_url = False
        print("URL is no valid")
    return check_url

def extract_last_element(page_url):
    """
    Get the last element of the url

    Parameter:
    page_url (str): the page url link

    Return:
    str: the last part of the url string
    """

    path = urlparse(page_url).path
    extracted_result = path.strip("/").split("/")[-1]

    return extracted_result


def extract_name(title) -> list:
    """
    Get all the names of the card from the page

    Parameter:
    title (str): the last part of the page url link

    Return:
    list: contain the card names
    """

    soup = get_html(title)

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

    return card_names

def extract_content(card_name) -> dict:
    """
    Base on the card name retrive the info specified

    Parameter:
    card_name (str): name of the card

    Return:
    dict: name, power, critical and clan
    """
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

    time.sleep(0.4)
    return extract_data


def scrape(page_url):
    """
    Combine all the function to web scrape

    Parameter:
    page_url (str): The page url link

    Return
    list-dict: card data
    """
    if check_url(page_url):
        last_element = extract_last_element(page_url)
        if ":" in last_element:
            names = extract_name(last_element)
            if names:
                card_names.extend(names)
        else:
            card_names.append(last_element)

        for name in track(card_names, description="[cyan]Collecting card data..."):
            card_info = extract_content(name)
            if card_info:
                card_data.append(card_info)

    else:
        print("Somthing Went Wrong somewhere pls try again")

    return card_data

def main():
    """Example execution"""

    # URL sample
    page_url = "https://cardfight.fandom.com/wiki/Trial_Deck_1:_Blaster_Blade"

    # Run the pipeline
    scrape(page_url)

    # Check result of the list
    print(card_data)

if __name__ == "__main__":
    main()
