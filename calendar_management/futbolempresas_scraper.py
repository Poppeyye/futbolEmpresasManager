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

        dates = soup.find_all('time', class_='widget-game-result__date')

        venues = soup.find_all('div', class_='widget-game-result__venue')

        score_links = soup.find_all('a', class_='widget-game-result__score')

        result_list = []

        for date, venue, score_link in zip(dates, venues, score_links):
            date_value = date.get_text(strip=True)
            date_match = re.search(r'(\d{2}/\d{2}/\d{4})', date_value)
            extracted_date = date_match.group(1)
            time_value = date.find('span', class_='event-time-status').get_text(strip=True)

            # Obtener el título del enlace y parsearlo
            score_title = score_link.get('href')
            vs_index = score_title.find('vs')

            # Formatear el título adecuadamente
            if vs_index != -1:
                team1 = score_title[:vs_index].split('/')[-1].replace('-', ' ').title()
                team2 = score_title[vs_index + 2:].split('/')[-2].replace('-', ' ').title()
                title_value = f"{team1} vs {team2}"
            else:
                title_value = ""

            location_value = venue.get_text(strip=True)

            result_dict = {
                "date": extracted_date,
                "time": time_value,
                "title": title_value,
                "location": location_value
            }

            result_list.append(result_dict)

        return result_list