from bs4 import BeautifulSoup
from typing import Dict, List
from io import StringIO
import pandas as pd
import ast
import re

# Constant variable.
CONVERSION_MILLION = (10 ** 6)


def scrape_statement(html_text: str) -> List[Dict]:
    # Convert BeautifulSoup object.
    soup = BeautifulSoup(html_text, 'html.parser')

    # Create a regular expression to search the variable that holds the data.
    search_pattern = re.compile(r'\boriginalData\s*=\s*(\[\{.*?\}\])\s*;\s*\n')

    # Find the data from the HTML script tag.
    script = soup.find(text=search_pattern)
    if script is None:
        raise ValueError("The web page text does not have the source.")
    
    # Grab the string and convert it into python collection data type.
    matched = search_pattern.search(script).group(1)
    cleaned = matched.replace(r'\/', '/')
    convert_value = ast.literal_eval(cleaned)

    return convert_value


def scrape_quote(html_text: str) -> str:
    # Convert BeautifulSoup object.
    soup = BeautifulSoup(html_text, 'html.parser')

    # Locate the table.
    table = soup.find('div', class_='table-container')
    
    # Convert it to pandas dataframe
    df = pd.read_html(StringIO(str(table)))[0]

    # Fixed the header and remove uncessary rows
    df.columns.values[-2] = 'Adj Close'
    df.columns.values[-3] = 'Close'
    df = df[~df['Open'].str.contains('Dividend', na=False)]

    # Turn it into csv file.
    csv_data = df.to_csv(index=False)

    return csv_data


def fixed_data(raw_data: List[Dict]) -> dict:
    # To be us in lambda mapping.
    def convert_type(value: str) -> int:
        if value != "":
            return round(float(value) * CONVERSION_MILLION, 2)
        return 0

    statement = {}
    for key_criteria in raw_data:
        try: 
            # Grab the label in html skeleton.
            name = key_criteria.pop('field_name').replace(r'</a>', '').replace(r'</span>', '').split('>')[-1].replace(' ', '-')

            # Remove uncessary data.
            del key_criteria['popup_icon']

            # Split the key and value.
            years = list(key_criteria.keys())
            cash = list(key_criteria.values())

            # Turn string number to float type and combine the year and cash.
            fixed_number = list(map(convert_type, cash))
            dataset = dict(zip(years, fixed_number))

            statement[name] = dataset

        except KeyError:
            raise KeyError("The criteria_info might not have one of these key [field_name, popup_icon]")

    return statement
