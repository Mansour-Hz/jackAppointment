import time
import schedule
import requests
from bs4 import BeautifulSoup
import keys

# Constants
AVAIL_SIGN = '<h2>Appointments available for'
ERROR_MESSAGE = '<p class="message-error">For your selection there are unfortunately no appointments available</p>'
successful_requests = 0

# Helper functions
def notify_user(message):
    bot_token = keys.BOT_TOKEN
    chat_id = keys.CHAT_ID

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            # print("Notification sent successfully!")
            pass
        else:
            try:
                error_message = response.json().get('description', 'No description')
            except ValueError:
                error_message = "No detailed error message available."
            print(f"Failed to send notification: 
                  {response.status_code} - {error_message}")

    except Exception as e:
        print(f"Error: {str(e)}")


def check_appointments(url, payload):
    global successful_requests
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Ensure the request was successful
        successful_requests += 1
        response_text = response.text

        if AVAIL_SIGN in response_text and ERROR_MESSAGE not in response_text:
            soup = BeautifulSoup(response_text, 'html.parser')
            day_tables = soup.find(
                'form', action="/HomeWeb/Scheduler").find_all('table', class_='no-border')

            days_and_times = []

            for table in day_tables[2:]:
                day_header = table.find('th')
                if day_header:
                    day_info = day_header.text.split(',')
                    if len(day_info) < 2:
                        continue  # Skip if the date format isn't as expected
                    day, date = day_info[0], day_info[1]
                    time_labels = table.find_all('label')
                    times = [
                        label.text for label in time_labels if ':' in label.text]

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


# Daily check function
def daily_check():
    notify_user("من بیدارم داداش")


# End of day report
def end_of_day_report():
    global successful_requests
    report_message = f"The bot is still running. Total successful requests today: {
        successful_requests}."
    notify_user(report_message)
    successful_requests = 0  # Reset for the next day


def main():
    global successful_requests

    # Schedule notifications at 08:00, 12:00, and 20:00 Tehran time
    schedule.every().day.at("08:00").do(daily_check)
    schedule.every().day.at("20:00").do(end_of_day_report)

    url = "https://appointment.bmeia.gv.at/?fromSpecificInfo=True"
    payload = {
        "Language": "en",
        "Office": "TEHERAN",
        "CalendarId": "23134510",
        "PersonCount": "1",
        "Command": "Next"
    }

    while True:
        # Run pending scheduled tasks
        schedule.run_pending()

        # Check for appointments
        try:
            appointments = check_appointments(url, payload)
            if appointments:
                message = "Available appointments:\n"
                for day, date, times in appointments:
                    message += f"{day}, {date}: " + ", ".join(times) + "\n"
                notify_user(f"سریع نوبت رو بگیر علی\n{message}")
            time.sleep(4)  # Wait before checking again

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(10)  # Wait longer before retrying if there's an error


if __name__ == "__main__":
    main()
