import urllib.parse


def create_payload(appointments):
    
    monday_time = "8/19/2024 12:00:00 AM"
    
    for day in appointments:
        date = day[1].strip()
        times = day[2]
        
        for time in times:
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
            
            return urllib.parse.urlencode(payload)

print(payload)