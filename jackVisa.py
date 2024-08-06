import requests
import pytz
from datetime import datetime
import time
import os

# File to keep track of the last notification time
LAST_NOTIFICATION_FILE = 'last_notification_time.txt'

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
            notify_user("سریع نوبت رو بگیر علی")
        else:
            print("No appointments available.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def should_send_status_update():
    # Tehran timezone
    tehran_tz = pytz.timezone('Asia/Tehran')
    current_time = datetime.now(tehran_tz)
    current_hour = current_time.hour

    # Notify at 08:00, 16:00, or 00:00 Tehran time
    return current_hour in [0, 8, 16]

def get_last_notification_time():
    if os.path.exists(LAST_NOTIFICATION_FILE):
        with open(LAST_NOTIFICATION_FILE, 'r') as file:
            last_time_str = file.read().strip()
            return datetime.fromisoformat(last_time_str)
    return None

def update_last_notification_time():
    with open(LAST_NOTIFICATION_FILE, 'w') as file:
        file.write(datetime.now(pytz.timezone('Asia/Tehran')).isoformat())

def main():
    while True:
        current_time = datetime.now(pytz.timezone('Asia/Tehran'))
        last_notification_time = get_last_notification_time()
        check_appointments()
        if should_send_status_update():
            if last_notification_time is None or (current_time - last_notification_time).total_seconds() >= 3600:
                notify_user("من هنوز دارم سایتو چک میکنم لاشی")
                update_last_notification_time()
        
        # Wait for 5 seconds before running the check again
        time.sleep(5)

main()
