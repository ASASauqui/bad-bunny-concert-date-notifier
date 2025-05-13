import time
import smtplib
import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
SOURCE_EMAIL = os.getenv("SOURCE_EMAIL")
DESTINATION_EMAILS = os.getenv("DESTINATION_EMAILS")  # Comma-separated list
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

URL = "https://depuertoricopalmundo.com/"
STORAGE_FILE = "known_dates.txt"  # Used for all countries

SUPPORTED_COUNTRIES = [
    "mexico",
    "colombia",
    "chile",
    "argentina",
    "brazil",
    "dominican_republic",
    "costa_rica",
    "peru",
    "australia",
    "japan",
    "spain",
    "portugal",
    "germany",
    "the_netherlands",
    "united_kingdom",
    "france",
    "sweden",
    "poland",
    "italy",
    "belgium",
]


def get_user_selected_countries():
    print("Supported countries:", ", ".join(SUPPORTED_COUNTRIES))
    user_input = input("Which countries do you want to monitor? (comma-separated): ")
    selected = [p.strip().lower() for p in user_input.split(",")]
    filtered = [p for p in selected if p in SUPPORTED_COUNTRIES]

    if not filtered:
        print("No valid countries selected. Exiting.")
        exit(1)
    return filtered


def send_email(date_text, venue, link, country):
    recipients = [
        email.strip() for email in DESTINATION_EMAILS.split(",") if email.strip()
    ]

    msg = EmailMessage()
    msg["Subject"] = f"New Bad Bunny Date in {country.upper()}! {date_text}"
    msg["From"] = SOURCE_EMAIL
    msg["To"] = ", ".join(recipients)
    msg.set_content(
        f"A new Bad Bunny concert date was detected in {country.title()}!\n\nDate: {date_text}\nVenue: {venue}\nTickets: {link}\n\nPage: {URL}"
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SOURCE_EMAIL, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(
            f"[EMAIL SENT] {country.upper()} - {date_text} to {', '.join(recipients)}"
        )
    except Exception as e:
        print(f"Error sending email: {e}")


def load_known_dates():
    if not os.path.exists(STORAGE_FILE):
        return set()
    with open(STORAGE_FILE, "r") as file:
        return set(line.strip() for line in file.readlines())


def save_known_date(date_id):
    with open(STORAGE_FILE, "a") as file:
        file.write(date_id + "\n")


def check_new_dates(countries_to_check):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    known_dates = load_known_dates()
    events = soup.find_all("div", class_="dateWrapper bbsd")

    for event in events:
        try:
            date_id = event.get("id")
            if not date_id:
                continue

            country_prefix = date_id.split("_")[0]
            if country_prefix not in countries_to_check:
                continue

            if date_id in known_dates:
                continue

            date_text = event.find("p", class_="date").text.strip()
            venue = event.find("p", class_="venue").text.strip()
            link_tag = event.find("a")
            link = link_tag.get("href") if link_tag else "No link"

            send_email(date_text, venue, link, country_prefix)
            save_known_date(date_id)
        except Exception as e:
            print(f"[ERROR] Skipping event due to: {e}")


def main():
    countries = get_user_selected_countries()
    print(f"Monitoring dates for: {', '.join(countries).upper()}")
    while True:
        print("[CHECKING FOR NEW DATES...]")
        try:
            check_new_dates(countries)
        except Exception as e:
            print(f"Error during scraping: {e}")
        time.sleep(20 * 60)


if __name__ == "__main__":
    main()
