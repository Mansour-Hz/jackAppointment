import requests
import time

AVAIL_SIGN = '<h2>Appointments available for'
error_message = '<p class="message-error">For your selection there are unfortunately no appointments available</p>'


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
            print("Failed to send notification: ", response.status_code,  " - ",  response.json())
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

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Check if the request was successful
        response_text = response.text

        if AVAIL_SIGN in response_text and error_message not in response_text:
            print(response.text)
            # notify_user("سریع نوبت رو بگیر علی")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    

while True:
    check_appointments()
    time.sleep(4)
