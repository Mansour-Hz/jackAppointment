import time
from helpers import check_appointments, notify_user

while True:

    url = "https://appointment.bmeia.gv.at/?fromSpecificInfo=True"

    payload = {
        "Language": "en",
        "Office": "TEHERAN",
        "CalendarId": "23134510",
        "PersonCount": "1",
        "Command": "Next"
    }

    appointments = check_appointments(url, payload)

    if appointments != []:
        notify_user("سریع نوبت رو بگیر علی")
    time.sleep(4)
