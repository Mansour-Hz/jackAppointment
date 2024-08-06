import requests
import pytz
from datetime import datetime

def notify_user(message):
    bot_token = '7002542991:AAHAWKTKY1aJ_gCZS8sZ6PpUrGQO2Frtsxw'
    chat_id = '-4129556338'  # Updated chat ID

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Notification sent successfully!")
        else:
            print(f"Failed to send notification: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

def check_appointments():
    url = "https://appointment.bmeia.gv.at/?fromSpecificInfo=True"
    payload = {
        "Language": "en",
        "Office": "TEHERAN",
        "CalendarId": "23134510",
        "PersonCount": "1",
        "Command": "Next"
    }
    error_message = '<p class="message-error">For your selection there are unfortunately no appointments available</p>'

    try:
        response = requests.post(url, data=payload)
        
        if error_message not in response.text:
            print("Appointments are available!")
            notify_user("Appointments are available!")
        else:
            print("No appointments available.")
    except Exception as e:
        print(f"Error: {str(e)}")

def should_send_status_update():
    # Tehran timezone
    tehran_tz = pytz.timezone('Asia/Tehran')
    current_time = datetime.now(tehran_tz)
    current_hour = current_time.hour

    # Notify at 08:00, 16:00, or 00:00 Tehran time
    return current_hour in [2, 8, 16, 0]

def main():
    check_appointments()
    if should_send_status_update():
        notify_user("The bot is still checking for appointments.")

main()
