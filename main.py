import json
import webbrowser
import time
import os
from dotenv import load_dotenv
import random
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert


load_dotenv()


# Authenticate with the Google Calendar API and retrieve the next meeting event
creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar'])
service = build('calendar', 'v3', credentials=creds)
now = datetime.utcnow().isoformat() + 'Z'
events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
event = events_result.get('items', [])[0]

USE_FAILSAFE_PERCAUTIONS = True
options = Options()


options.add_argument('--disable-notifications')
options.add_argument('--start-maximized')
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)

def turnOffMicCam():
    # turn off Microphone
    time.sleep(2)
    driver.find_element(By.XPATH,
        '//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[1]/div/div/div').click()
    driver.implicitly_wait(3000)
 
    # turn off camera
    time.sleep(1)
    driver.find_element(By.XPATH,
        '//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[2]/div/div').click()
    driver.implicitly_wait(3000)
 
 
def joinNow():
    # Join meet
    print(1)
    time.sleep(5)
    driver.implicitly_wait(2000)
    driver.find_element(By.CSS_SELECTOR,
        'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
    print(1)
 
 
def AskToJoin():
    # Ask to Join meet
    time.sleep(5)
    driver.implicitly_wait(2000)
    driver.find_element(By.CSS_SELECTOR,
        'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
    # Ask to join and join now buttons have same xpaths
 
def join_now():
    join_button = WebDriverWait(driver, 36).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Join now')]")))
    driver.execute_script("arguments[0].click();", join_button)
def ask_to_join():
    join_button = WebDriverWait(driver, 36).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Ask to join')]")))
    driver.execute_script("arguments[0].click();", join_button)
meetings = []
for event in events_result['items']:
    print("The meeting title " , event.get('summary'))
    meeting_link = event.get('hangoutLink')
    print(meeting_link)
    if meeting_link and event.get('summary') != "Lunch Break":
        meetings.append(meeting_link) 
        
        #  '''
        #  The following will be used to fetch the data from our local user data of chrome service running on local machine
         
        #     options = webdriver.ChromeOptions()
        #     options.add_argument(r"--user-data-dir=	C:\Users\KINFISH\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
        #     options.add_argument(r'--profile-directory=	C:\Users\KINFISH\AppData\Local\Google\Chrome\User Data\Profile 2') #e.g. Profile 3
         
        #  '''
        # driver = webdriver.Chrome(executable_path=r'C:\path\to\chromedriver.exe', chrome_options=options)
        # driver = webdriver.Chrome(options=options)
    # driver.get("https://www.google.co.in")


meeting_link = meetings[0]


def join_meeting(meeting_link):

    username =  os.getenv('EMAIL_ID')
    password = os.getenv('PASSWORD')

    # Configure the Selenium web driver
    
    #Navigate to the Google login page
    driver.get('https://accounts.google.com/')
    time.sleep(4)

    # Enter your username and click Next
    email_field = driver.find_element(by='name' ,value= 'identifier')
    email_field.send_keys(username)
    email_field.send_keys(Keys.RETURN)
    time.sleep(6)

    # Enter your password and click Next
    password_field = driver.find_element(by='name' , value= 'Passwd')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(6)

    # Open the Meet link in a new tab
    driver.execute_script("window.open('" + meeting_link + "', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(15)
    # notification_prompt = driver.find_element(by='xpath' , value='//button[@aria-label="Allow"]')
    # notification_prompt.click()
    for i in range(6):
        try:


            time.sleep(2)
            options.add_argument('--disable-notifications')
            join_now()
            options.add_argument('--disable-notifications')
            driver = webdriver.Chrome(options=options)
                    
            # join_button = driver.find_element(by='xpath' ,value='//span[contains(text(), "Join now")]')
            # join_button.click()

        except selenium.common.exceptions.TimeoutException:
            options.add_argument('--disable-notifications')
            ask_to_join()
            options.add_argument('--disable-notifications')
            driver = webdriver.Chrome(options=options)
            # alert = Alert(driver)/
            # alert = driver.switch_to.alert
            
            print('ERROS HAS OCCURED')


    #     time.sleep(5)
            

    # for i in range(6):
    #     try:
    #         WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Join now')]")))

    #         time.sleep(2)
    #         turn_off_mic_action = ActionChains(driver)
    #         turn_off_mic_action.key_down(Keys.CONTROL).send_keys("d").key_up(Keys.CONTROL).perform();
    #         turn_off_camera_action = ActionChains(driver)
    #         turn_off_camera_action.key_down(Keys.CONTROL).send_keys("e").key_up(Keys.CONTROL).perform();
    #         print("Sucessfully found landmark...turned off camera and microphone.")
    #         break
    #     except selenium.common.exceptions.TimeoutException:
    #         try:
    #             WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Ask to join')]")))

    #             time.sleep(2)
    #             turn_off_mic_action = ActionChains(driver)
    #             turn_off_mic_action.key_down(Keys.CONTROL).send_keys("d").key_up(Keys.CONTROL).perform();
    #             turn_off_camera_action = ActionChains(driver)
    #             turn_off_camera_action.key_down(Keys.CONTROL).send_keys("e").key_up(Keys.CONTROL).perform();
    #             print("Sucessfully found landmark...turned off camera and microphone.")
                
    #             break
    #         except selenium.common.exceptions.TimeoutException:
    #             print("[ERROR]: Attempting to find landmark...")
    #             if USE_FAILSAFE_PERCAUTIONS: time.sleep(6)
    #             else: driver.implicitly_wait(6)

    # try:
    #     join_button = WebDriverWait(driver, 36).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Join now')]")))
    #     driver.execute_script("arguments[0].click();", join_button)
        

    # except selenium.common.exceptions.TimeoutException:
    #     try:
    #         join_button = WebDriverWait(driver, 36).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Ask to join')]")))
    #         driver.execute_script("arguments[0].click();", join_button)
    #     except selenium.common.exceptions.TimeoutException:
    #         print("Couldn't join Google Meet. Are you sure you have the right code?")
            # join_button = driver.find_element(by="name" , value='.VfPpkd-LgbsSe-OWXEXe-k8QpJ')
    # join_button.click()
    # camera_button = driver.find_element(by='css selector', value='.dP0OSd > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)')
    # camera_button.click()
    # time.sleep(1)
    # mic_button = driver.find_element(by='css selector', value='.DPvwYc.JnDFsc.dMzo5')
    # mic_button.click()




    # driver.switch_to.window(driver.window_handles[-1])
    # join_button = driver.find_element(by='css selector', value='.VfPpkd-LgbsSe-OWXEXe-k8QpJ > div:nth-child(3)')
    # join_button.click()
    # time.sleep(2)
    

    # The above works by turning of both the camera and mic


    # driver.switch_to.window(driver.window_handles[-1])
    # print(driver.window_handles)
    # time.sleep(10)
    # .NPEfkd
    # join_button = driver.find_element(by="css selector" ,  value=".NPEfkd")
    # join_button.click()
    # driver.find_element(by='css selector', value='.sUZ4id > div:nth-child(1)').click()
    # time.sleep(2)
    # driver.find_element(by='css selector', value='.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
        # print(event.get('hangoutLink'))


# for event in events:
# for
# Join the meeting
# driver = webdriver.Chrome()
# driver.get(event.get('hangoutLink'))
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="identifier"]')))
# driver.find_element_by_name('identifier').send_keys('kinfemichael.tariku@a2sv.com')
# driver.find_element_by_id('identifierNext').click()
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
# driver.find_element_by_name('password').send_keys('strongypassword191425')
# driver.find_element_by_id('passwordNext').click()
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@jsname="CQylAd"]')))
# driver.find_element_by_xpath('//div[@jsname="CQylAd"]').click()



join_meeting(meeting_link)
turnOffMicCam()