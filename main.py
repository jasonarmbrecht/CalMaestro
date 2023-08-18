# ==========================================================
# CalMaestro v0.1
# 
# ==========================================================
import re
import requests
import icalendar

# Settings

# Personal URL from AM - CHANGE TO 'HTTPS://...'
HTTP_URL = '<REPLACE ME WITH HTTPS URL>'

# TZ API URL for FLDB - Don't change
API_URL = "https://api.flightplandatabase.com/nav/airport/{}"

# Connect to AM webcals feed and return raw data
def get_current_feed():
    try:
        response = requests.get(HTTP_URL)
        if response.status_code != 200:
            raise ValueError(f"Unexpected status code: {response.status_code}")

        ics_content = response.text
        if not ics_content:
            raise ValueError("The fetched content is empty!")
    
        cal = icalendar.Calendar.from_ical(ics_content)
        return cal

    except Exception as e:
        print(f"An error occurred: {e}")   

# Todo: 
# Match regex patterns and create dict for relevant data

# Make adjustments based on deserialised DESCRIPTION with Route.

# Correct TZ using FPDB function

# Validate and export back to ical. 

# Feed to self-hosted CalDAV server for publishing.

# API to take input of ICAO airport code and return timezone
# Using FPDB until I can create something better
def get_standard_timezone_offset(icao_code):
    response = requests.get(API_URL.format(icao_code))

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        timezone = data.get("timezone", {})
        offset_seconds = timezone.get("offset", None)
        
        # Convert the offset in seconds to hours and minutes
        if offset_seconds is not None:
            hours, remainder = divmod(offset_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            if hours == 0 and minutes == 0:
                return "Z"
            else:
                sign = "+" if hours >= 0 else "-"
                return f"UTC{sign}{abs(hours):02}:{minutes:02}"
        else:
            return None
    else:
        print(f"Error fetching data for ICAO code {icao_code}. Status Code: {response.status_code}")
        return None



# TEST SECTION
# TZ offset example usage:
icao_code = "YPXM"
offset = get_standard_timezone_offset(icao_code)
print(offset)  # expected UTC+07:00