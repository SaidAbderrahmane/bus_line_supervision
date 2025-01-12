import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime

# Mapping French month names to numerical values
month_mapping = {
    "Janvier": "01",
    "Février": "02",
    "Mars": "03",
    "Avril": "04",
    "Mai": "05",
    "Juin": "06",
    "Juillet": "07",
    "Août": "08",
    "Septembre": "09",
    "Octobre": "10",
    "Novembre": "11",
    "Décembre": "12",
}

base_url = "https://www.les-sports.info/ajax_php.php"
params = {"majajax": "resultats_equ", "equipeid": "526", "langage": "fr"}

season_ids = range(319, 327)
with open("results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        ["Date", "equipe1", "score", "equipe2"]
    )  # Adjust column headers as needed

    for season_id in season_ids:
        params["saisonid"] = season_id

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            general_tables = soup.find_all("table", class_="table-style-2")
            for general_table in general_tables:
                rows = general_table.find_all("tr")
                for row in rows:
                    if len(list(row.children)) == 4:
                        cols = [
                            col.text
                            for col in row.find_all("td", class_=re.compile(r"tdcol"))
                        ]
                        # Extract only the date (first part of the text before the time)
                        date_match = re.match(r"(\d{1,2})\s(\w+)\s(\d{4})", cols[0])
                        if date_match:
                            day = date_match.group(1)
                            month_french = date_match.group(2)
                            year = date_match.group(3)
                            # Convert the month from French to numerical value
                            month_number = month_mapping.get(
                                month_french, "01"
                            )  # Default to '01' if not found
                            # Format date to dd/mm/yyyy
                            formatted_date = f"{day.zfill(2)}/{month_number}/{year}"
                            cols[0] = (
                                formatted_date  # Replace the first column with the formatted date
                            )
                        writer.writerow(cols)
        else:
            print(
                f"Failed to fetch data for season ID: {season_id}. Status code: {response.status_code}"
            )
