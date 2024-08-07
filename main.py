import getAppointment

def main():
    url = "https://appointment.bmeia.gv.at/?fromSpecificInfo=True"
    payload = {
        "Language": "en",
        "Office": "TEHERAN",
        "CalendarId": "23369141",
        "PersonCount": "1",
        "Command": "Next"
    }

    available_appointments = getAppointment.check_appointments(url, payload)

    # print(available_appointments)

    if available_appointments != []:

        isAnyTime = getAppointment.chooseDate(available_appointments)
        if isAnyTime:
            print("Omadim Ta Inja")

if __name__ == "__main__":
    main()
