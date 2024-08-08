import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys

AVAIL_SIGN = '<h2>Appointments available for'


def check_appointments(url, payload):
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Check if the request was successful
        response_text = response.text

        if AVAIL_SIGN in response_text:

            # Assuming the HTML content is stored in a variable called 'html_content'
            soup = BeautifulSoup(response_text, 'html.parser')

            # Find all table elements that contain the day and time information
            day_tables = soup.find('form',
                                   action="/HomeWeb/Scheduler").find_all('table', class_='no-border')

            # Initialize the result array
            days_and_times = []

            for table in day_tables[2:]:
                # Find the day in the table header
                day_header = table.find('th')
                if day_header:
                    # Extract just the day name
                    day = day_header.text.split(',')[0]
                    date = day_header.text.split(',')[1]
                    # Find all time labels in this table
                    time_labels = table.find_all('label')
                    times = [
                        label.text for label in time_labels if ':' in label.text]

                    # Add this day and its times to the result array
                    if times:  # Only add if there are times available
                        days_and_times.append([day, date, times])

            return days_and_times
        else:
            return []

    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []


def get_initial_session(url="https://appointment.bmeia.gv.at/"):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
    }
    session.get(url, headers=headers)
    return session


def chooseDate(appointments, url="https://appointment.bmeia.gv.at/HomeWeb/Scheduler"):
    session = get_initial_session()
    monday_time = "8/19/2024 12:00:00 AM"

    headers = {

        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "appointment.bmeia.gv.at",
        "Origin": "https://appointment.bmeia.gv.at",
        "Referer": "https://appointment.bmeia.gv.at/?fromSpecificInfo=True",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"'
    }

    for day in reversed(appointments):
        date = day[1].strip()
        times = day[2]

        for time in reversed(times):
            start_time = f"{date} {time}:00 AM"

            payload = {
                "Language": "en",
                "Office": "TEHERAN",
                "CalendarId": "23369141",
                "PersonCount": "1",
                "Monday": monday_time,
                "Start": start_time,
                "Command": "Next"
            }

            encodedPayload = urllib.parse.urlencode(payload)
            # print(encodedPayload)

            try:
                response = session.post(
                    url, data=encodedPayload, headers=headers)
                if response.status_code == 200:
                    return True  #
            except requests.exceptions.RequestException as e:
                print("Error: ", e)

    return session.cookies  # Return cookies in case you need them for further operations
