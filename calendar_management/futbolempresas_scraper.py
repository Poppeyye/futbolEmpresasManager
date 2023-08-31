import os

import requests
from bs4 import BeautifulSoup
import re

TEAM_NAME_DASHED = os.getenv('team')
TEAM_NAME = TEAM_NAME_DASHED.replace("-", " ").capitalize() # review this with different team names

def get_calendar_fe():
    url = f'https://www.futbolempresas.es/calendario/{TEAM_NAME_DASHED}/'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        card_contents = soup.find_all('div', class_='card__content')

        for card_content in card_contents:
            text = card_content.get_text(strip=True)

            date_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
            date = date_match.group(1) if date_match else "Date not found"

            time_match = re.search(r'(\d{2}:\d{2})', text)
            time = time_match.group(1) if time_match else "Time not found"

            parts = text.split(time)
            location_title = parts[1].strip()

            title, location = location_title.split('-') if '-' in location_title else (location_title, "")
            title = title.replace(TEAM_NAME, f" {TEAM_NAME}").strip()

            print("Date:", date)
            print("Time:", time)
            print("Title:", title)
            print("Location:", location)
            print("------")
            return {"date": date,
                    "time": time,
                    "title": title,
                    "location": location}
    else:
        print("Failed to fetch the URL. Status code:", response.status_code)
