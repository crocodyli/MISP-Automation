import time
import requests
from pymisp import PyMISP
from datetime import datetime, timedelta
import urllib3

# Suppress unverified HTTPS warnings (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# MISP Settings
misp_url = 'URL MISP'
misp_key = 'Authkey MISP'
misp_verifycert = False  # Set to True if you want to verify the certificate

# Telegram Settings
bot_token = 'XXX:XXXXX'
chat_id = '-XXXXX'

# Function to send message via Telegram
def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

# Function to check events in MISP
def check_misp_events(misp, tags, published):
    # Calculate the time range of the last 24 hours
    last_24_hours = datetime.now() - timedelta(hours=24)
    timestamp = last_24_hours.strftime('%Y-%m-%dT%H:%M:%S')
    result = misp.search(tags=tags, published=published, date_from=timestamp)
    return result

misp = PyMISP(misp_url, misp_key, misp_verifycert)

# Tags to look for
tags = ['XXX','XXX']

# Loop to check for new events periodically
while True:
    # Check published events
    published_events = check_misp_events(misp, tags, True)
    if published_events:
        for event in published_events:
            event_info = event['Event'].get('info', 'Untitled')
            event_id = event['Event'].get('id', 'No ID')
            event_date = event['Event'].get('date', 'No date')
            # Count the number of attributes
            attribute_count = len(event['Event'].get('Attribute', []))
            message = f"🚨 New event published on MISP 🚨\n**Título:** {event_info}\n**Event ID:** {event_id}\n**Date Created:** {event_date}\n**Number of Attributes:** {attribute_count}"
            send_telegram_message(bot_token, chat_id, message)
    else:
        message = f"⚠️ No events have been published on MISP with the tags '{', '.join(tags)}' in the last 24 hours."
        send_telegram_message(bot_token, chat_id, message)

    #Check for unpublished events
    unpublished_events = check_misp_events(misp, tags, False)
    if unpublished_events:
        for event in unpublished_events:
            event_info = event['Event'].get('info', 'Untitled')
            event_id = event['Event'].get('id', 'No ID')
            event_date = event['Event'].get('date', 'No date')
            # Count the amount of attributes
            attribute_count = len(event['Event'].get('Attribute', []))
            message = f"🔔 Event not published in MISP 🔔\n**Title:** {event_info}\n**Event ID:** {event_id}\n**Date Created:** {event_date}\n**Number of Attributes:** {attribute_count}"
            send_telegram_message(bot_token, chat_id, message)

    # Please wait 12 hours before checking again.
    time.sleep(43200)
