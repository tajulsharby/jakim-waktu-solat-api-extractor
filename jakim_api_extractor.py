import requests
import csv
from datetime import datetime, timedelta
import logging
from concurrent.futures import ThreadPoolExecutor
import json
import os

# Constants
BASE_URL = "https://www.e-solat.gov.my/index.php"

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler('data_extraction.log')
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def print_intro():
    intro_text = """
    ==========================================================================================
    JAKIM Waktu Solat API Extractor
    Description: Extract JAKIM's prayer times for the whole Malaysia's zone to CSV format
    Created by: TJ Sharby
    Github: https://github.com/tajulsharby/jakim-waktu-solat-api-extractor
    If you like, please treat me a coffee ;-)
    ==========================================================================================
    """
    print(intro_text)

def load_zones(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def fetch_hijri_date(date, zone_code, retries=5):
    params = {
        'r': 'esolatApi/TakwimSolat',
        'period': 'date',
        'date': date.strftime("%Y-%m-%d"),
        'zone': zone_code
    }
    api_url = f"{BASE_URL}?r=esolatApi/TakwimSolat&period=date&zone={zone_code}&date={date.strftime('%Y-%m-%d')}"
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)  # Set timeout to 10 seconds
            response.raise_for_status()  # Raise an exception for HTTP errors
            logging.info(f"Calling API: {api_url}")
            return response.json()
        except requests.exceptions.Timeout:
            attempt += 1
            logging.warning(f"Timeout occurred for {date} in zone {zone_code}. Retrying {attempt}/{retries}...")
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            return None
    logging.error("API request timed out after more than 5 retries.")
    return None

def process_zone(state, zone_code, zone_name, start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        hijri_data_am = fetch_hijri_date(current_date, zone_code)
        hijri_data_pm = fetch_hijri_date(current_date + timedelta(days=1), zone_code)

        if hijri_data_am and 'prayerTime' in hijri_data_am and hijri_data_pm and 'prayerTime' in hijri_data_pm:
            logging.info(f"Processing data for {zone_code} on {current_date}")
            prayer_times_am = hijri_data_am['prayerTime'][0]  # Get the first (and only) entry
            prayer_times_pm = hijri_data_pm['prayerTime'][0]  # Get the first (and only) entry

            yield [
                prayer_times_am.get("date"),
                prayer_times_am.get("hijri"),
                prayer_times_pm.get("hijri"), # Get the next day hijri date
                prayer_times_am.get("day"),
                prayer_times_am.get("imsak"),
                prayer_times_am.get("fajr"),
                prayer_times_am.get("syuruk"),
                prayer_times_am.get("dhuhr"),
                prayer_times_am.get("asr"),
                prayer_times_am.get("maghrib"),
                prayer_times_am.get("isha"),
                state,
                zone_code,
                zone_name
            ]
        current_date += timedelta(days=1)

def main():
    # Print intro message
    print_intro()

    # Date range for 2024
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 30)

    # Load zones from JSON file
    zones_file_path = os.path.join(os.path.dirname(__file__), 'zones.json')
    zones_by_state = load_zones(zones_file_path)

    # Get the current date and time
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")

    # CSV file name
    csv_file_name = f"hijri_date_{formatted_datetime}.csv"

    # Open CSV file for writing
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "date", 
            "hijri_am",
            "hijri_pm", 
            "day", 
            "imsak", 
            "subuh", 
            "syuruk", 
            "zohor", 
            "asar", 
            "maghrib", 
            "isyak", 
            "state", 
            "zone", 
            "name"
        ])

        with ThreadPoolExecutor() as executor:
            futures = []
            for state, zones in zones_by_state.items():
                for zone_code, zone_name in zones.items():
                    futures.append(executor.submit(process_zone, state, zone_code, zone_name, start_date, end_date))

            for future in futures:
                for row in future.result():
                    writer.writerow(row)
                    logging.info(f"Row written to CSV: {row}")

    logging.info("Data extraction process completed.")

if __name__ == "__main__":
    main()
