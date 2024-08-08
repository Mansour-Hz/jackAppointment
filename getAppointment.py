import requests
from bs4 import BeautifulSoup
import urllib.parse

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
                    day = day_header.text.split(',')[0]  # Extract just the day name
                    date = day_header.text.split(',')[1]
                    # Find all time labels in this table
                    time_labels = table.find_all('label')
                    times = [label.text for label in time_labels if ':' in label.text]
                    
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