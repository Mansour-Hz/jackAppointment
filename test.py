import requests

def notify_user():
    bot_token = '7002542991:AAHAWKTKY1aJ_gCZS8sZ6PpUrGQO2Frtsxw'
    channel_id = '-876461439'
    message = 'Appointments are available!'

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': channel_id,
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
        
        if True:
            print("Appointments are available!")
            notify_user()
        else:
            print("No appointments available.")
    except Exception as e:
        print(f"Error: {str(e)}")

check_appointments()

