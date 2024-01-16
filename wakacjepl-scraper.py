import requests
import re
import json
import time

def get_data_from_page(country: str, page: int):
    pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
    url = f"https://www.wakacje.pl/wczasy/{country.lower()}/?str-{page},ocena-malejaco"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
            result = re.search(pattern, text)
            if result:
                found_text = result.group(1)
                json_data = json.loads(found_text)
                items = json_data.get("props", {}).get("stores", {}).get("storeOffers", {}).get("offers", {}).get(
                    "data", [])
                return items
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def save_data_to_file(data, filename):
    with open(filename, "wt") as fd:
        json.dump(data, fd)


country = "zanzibar"
max_pages = 21
result = []
max_attempts = 5

for ix in range(1, max_pages):
    time.sleep(1.7)
    attempts = 0
    part_result = None
    while attempts < max_attempts:
        part_result = get_data_from_page(country, ix)
        if part_result is not None:
            break
        attempts += 1
        time.sleep(30)
    if part_result:
        result.extend(part_result)
        print(f"OK - {country} - {ix}")
    else:
        print(f"No data or Error - {country} - {ix}")

save_data_to_file(result, f"dane-{country}.json")
