import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Authenticate with the Google Calendar API
creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar'])
service = build('calendar', 'v3', credentials=creds)

# Define the time range to search for events
start_time = datetime.utcnow()
end_time = start_time.replace(hour=23, minute=59, second=59)

# Search for events with conference data within the time range
events_result = service.events().list(calendarId='primary', timeMin=start_time.isoformat(), timeMax=end_time.isoformat(), singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items', [])

# Iterate through the events and join the meeting for the first event with a Google Meet link
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    start_time = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    
    if 'hangoutsMeet' in event['conferenceData']['entryPoints'][0]['entryPointType']:
        meeting_link = event['conferenceData']['entryPoints'][0]['uri']
        meeting_duration = (datetime.fromisoformat(event['end']['dateTime']).replace(tzinfo=timezone.utc) - start_time).seconds

        # Join the meeting
        driver = webdriver.Chrome()
        driver.get(meeting_link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="identifier"]')))
        driver.find_element_by_name('identifier').send_keys('myemail@example.com')
        driver.find_element_by_id('identifierNext').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
        driver.find_element_by_name('password').send_keys('mypassword')
        driver.find_element_by_id('passwordNext').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@jsname="CQylAd"]')))
        join_button = driver.find_element_by_xpath('//div[@jsname="CQylAd"]')
        join_time = start_time - datetime.now(timezone.utc)
        time.sleep(join_time.total_seconds())
        join_button.click()
        time.sleep(meeting_duration)
        driver.quit()
        break