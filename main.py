import os
import random
import time

import unicodedata
from gologin import GoLogin
from selenium import webdriver
from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from telethon import TelegramClient, events
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telethon.tl.types import MessageMediaPhoto

############## ---------------Telegram API credentials
API_ID = "20231368"
API_HASH = "2194800680038835631408bb6fccd16d"
BOT_TOKEN = "8092099688:AAEgP5w17zotUFW3ScdznvJEpHviG0j0XOM"

# Channels
SOURCE_CHANNEL = "onchain_meme"  # Source channel to listen to
# SOURCE_CHANNEL = "onchaintestmeme"  # Source channel to listen to
footer_path = f"C:/Users/Administrator/Downloads/changetext/footer.txt"
bio_path = f"C:/Users/Administrator/Downloads/changetext/bio.txt"
header_path = f"C:/Users/Administrator/Downloads/changetext/header.txt"
found_path = f"C:/Users/Administrator/Downloads/changetext/found.txt"
now_path = f"C:/Users/Administrator/Downloads/changetext/now.txt"

DESTINATION_CHANNEL_ID = "@onchain_meme"  # Destination channel to repost to
client = TelegramClient("session_name", API_ID, API_HASH)


profiles = [
    {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2JmMjUxYWViYTc5YzlhYTNhZjMzOTEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2JmMjgwNjIxZGRiZjM3OGNjNDVjMmMifQ.ZB7qnD0J5e7TW_WEJflotqTx_CRwwccAImS36JHDLEs',
        'profile_id': '67c2db00cf918ba0d64151bc'  # Profile 1 ID
    },
    {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2JmMjUxYWViYTc5YzlhYTNhZjMzOTEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2JmMjgwNjIxZGRiZjM3OGNjNDVjMmMifQ.ZB7qnD0J5e7TW_WEJflotqTx_CRwwccAImS36JHDLEs',
        'profile_id': '67c55399aca4931781ed65f2'  # Replace with your Profile 2 ID
    },
    {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2JmMjUxYWViYTc5YzlhYTNhZjMzOTEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2JmMjgwNjIxZGRiZjM3OGNjNDVjMmMifQ.ZB7qnD0J5e7TW_WEJflotqTx_CRwwccAImS36JHDLEs',
        'profile_id': '67c64b4dd858809e6118a287'  # Replace with your Profile 3 ID
    }
]

chrome_driver_path = f"C:/Users/Administrator/Downloads/chromedriver-win64/chromedriver.exe"

BASE_PORT = 3500

drivers = []
gl_instances = []
# Create a Telegram client
for i, profile in enumerate(profiles):
    port = BASE_PORT + i
    gl = GoLogin({
        'token': profile['token'],
        'profile_id': profile['profile_id'],
        'port': port
    })
    # gl_instances.append(gl_instance)
    #
    # # Start the profile and get its debugger address.
    # debugger_address = gl_instance.start()
    # time.sleep(5)
    #
    # chrome_options = Options()
    # chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    # service = Service(executable_path=chrome_driver_path)
    # driver_instance = webdriver.Chrome(service=service, options=chrome_options)
    # drivers.append(driver_instance)
    #
    # print(f"Initialized driver for profile {profile['profile_id']} with debugger address {debugger_address}")

    debugger_address = gl.start()
    time.sleep(5)  # Increased delay to ensure profile fully starts

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    service = Service(executable_path=chrome_driver_path)
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        drivers.append(driver)
        gl_instances.append(gl)
    except Exception as e:
        print(f"Failed to initialize driver {i} for profile {profile['profile_id']}: {e}")

####################### ------------------- TWITTER ------------------- ###########################

def get_random_line(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
        return random.choice(lines) if lines else ""
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return ""

def format_message_comment(message):

    lines = message.split("\n")
    token_message = lines[0].strip()
    header = get_random_line(header_path)
    bio = get_random_line(bio_path)

    return f"{header} - {token_message} - {bio}"

def format_message(message):
    header = get_random_line(header_path)
    footer = get_random_line(footer_path)
    bio = get_random_line(bio_path)
    found = get_random_line(found_path)
    now = get_random_line(now_path)
    updated_message = message.replace("Market found:", found).replace("Market Now:", now)

    return f"{header}\n{updated_message}\n{bio}"

def remove_last_line(text):
    lines = text.split('\n')  # Split the message into lines
    lines = lines[:-1]  # Remove the last line
    return '\n'.join(lines)  # Rejoin the lines back into a single string

def remove_unsupported_characters(text):
    # Remove characters outside BMP (e.g., emojis)
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if ord(c) <= 0xFFFF)


def comment_twitter(message_text, i):
    # Use the first driver instance (adjust if necessary)
    driver = drivers[i]
    driver.execute_script("window.focus();")
    for _ in range(2):
        driver.get("https://x.com/home")
        time.sleep(15)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        # --- PART 1: Click the Tweet-User-Avatar in the second cell element ---
        cell_divs = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')
        first_post = cell_divs[2]
        # print(f"find first_post is ok")

        try:
            tweet_user = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetText"]'))
            )

            driver.execute_script("arguments[0].scrollIntoView(true);", tweet_user)
            time.sleep(2)
        except (StaleElementReferenceException, NoSuchElementException):
            continue

        if tweet_user:
            driver.execute_script("arguments[0].click();", tweet_user)
            # print(f"click tweet_user is ok")

        time.sleep(10)

        # Find tweet textarea and enter temporary text
        try:
            tweet_text_area = driver.find_element(By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']")
            # print(f"find tweet_text_area is ok")
        except (StaleElementReferenceException, NoSuchElementException):
            continue

        if tweet_text_area:
            tweet_text_area.send_keys(message_text)

        time.sleep(5)

        try:
            tweet_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="tweetButtonInline"]')
            # print(f"find tweet_button is ok")
        except (StaleElementReferenceException, NoSuchElementException):
            continue

        if tweet_button:
            # tweet_button.click()
            # print(f"click tweet_button is ok")
            driver.execute_script("arguments[0].click();", tweet_button)
        # else:
        #     print("Tweet reply button not found or error updating tweet textarea.")

        time.sleep(5)  # Additional delay before closing the reply dialog



    # Remove this feature
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #
    # time.sleep(5)
    #
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #
    # time.sleep(5)
    # # --- PART 2: Loop through cells and reply to tweets ---
    # cell_divs_2 = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    #
    # size_cell_divs_2 = len(cell_divs_2)
    # print(f"size of cell_divs_2 {size_cell_divs_2}")
    #
    # if not cell_divs_2:
    #     print("No cell elements found.")
    #     return
    #
    # first_href = cell_divs_2[0].find_element(By.CSS_SELECTOR, 'a[href]').get_attribute('href')
    #
    # count = 0
    # count_comment = 0
    #
    # for cell in cell_divs_2:
    #     if count_comment == 5:
    #         break
    #
    #     count += 1
    #     if count == 1:
    #         continue  # Skip the first matching cell
    #
    #     # try:
    #     #     a_element = cell.find_element(By.CSS_SELECTOR, 'a[href]')
    #     #     a_href = a_element.get_attribute('href')
    #     # except (StaleElementReferenceException, NoSuchElementException):
    #     #     print(f"Skipping cell {count} due to stale element or missing link.")
    #     #     continue
    #     #
    #     #     # If the cell's link matches the first_href, skip it.
    #     # if a_href == first_href:
    #     #     print(f"Cell {count} contains target value, skipping.")
    #     #     continue
    #
    #     # Only process cells that contain the verified icon
    #     # verified_icon = cell.find_element(By.CSS_SELECTOR, '[data-testid="icon-verified"]')
    #     # if not verified_icon:
    #     #     continue
    #
    #     try:
    #         verified_icons = cell.find_element(By.CSS_SELECTOR, 'svg[data-testid="icon-verified"]')
    #     except (NoSuchElementException, StaleElementReferenceException):
    #         continue
    #
    #     if not verified_icons:
    #         continue
    #
    #     try:
    #         reply_button = cell.find_element(By.CSS_SELECTOR, 'button[data-testid="reply"]')
    #     except (NoSuchElementException, StaleElementReferenceException):
    #         continue
    #
    #
    #     # Click the reply button
    #     reply_button.click()
    #     print(f"Clicked reply button for matching cell number {count}")
    #
    #     time.sleep(2)  # Delay of 2 seconds
    #
    #     # Find tweet textarea and enter temporary text
    #     tweet_text_area = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
    #     if tweet_text_area:
    #         tweet_text_area.send_keys(message_text)
    #         print("Entered text in tweet textarea.")
    #     else:
    #         print("Tweet textarea not found.")
    #         continue
    #
    #     time.sleep(5)
    #
    #     tweet_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="tweetButton"]')
    #     if tweet_button:
    #         tweet_button.click()  # Click and focus again
    #     else:
    #         print("Tweet reply button not found or error updating tweet textarea.")
    #
    #     time.sleep(5)  # Additional delay before closing the reply dialog
    #     count_comment += 1

def post_to_twitter(message, image_path, i):
    # Sequential posting
    driver = drivers[i]
    driver.execute_script("window.focus();")
    profile_id = profiles[i]['profile_id']
    try:
        driver.get("https://x.com/home")
        time.sleep(20)
        current_url = driver.current_url
        print(f"Driver {i} navigated to: {current_url}")
        if "x.com/home" not in current_url:
            raise Exception(f"Failed to navigate to https://x.com/home. Current URL: {current_url}")

        if image_path:
            absolute_image_path = os.path.abspath(image_path)
            upload_image = driver.find_element(By.CSS_SELECTOR, '[data-testid="fileInput"]')
            upload_image.send_keys(absolute_image_path)

        time.sleep(2)

        tweet_box = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
        tweet_box.send_keys(format_message(remove_unsupported_characters(message)))
        time.sleep(5)

        tweet_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]')
        tweet_button.click()
        print(f"Tweet posted by driver {i}")

    except Exception as e:
        print(f"Error with driver {i} (profile {profile_id}): {e}")
    time.sleep(10)  # Delay between posts


@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    image_path = None
    message_text = event.message.message
    message_reply = event.message.reply_to_msg_id
    full_message = event.message

    if message_reply:
        root_message = await client.get_messages(SOURCE_CHANNEL, ids=full_message.reply_to_msg_id)
        if root_message.media and isinstance(root_message.media, MessageMediaPhoto):
            image_path = await root_message.download_media()

        for i in range(len(drivers)):
            try:
                comment_twitter(format_message_comment(remove_unsupported_characters(message_text)), i)
                post_to_twitter(message_text, image_path, i)
            except Exception as e:
                profile_id = profiles[i]['profile_id']
                print(f"Error processing profile {profile_id}: {e}")

        try:
            os.remove(image_path)
        except Exception as e:
            print(f"Error removing file {image_path}: {e}")

try:
    client.start()
    print("Listening for messages...")
    client.run_until_disconnected()
finally:
    # Cleanup: Stop all GoLogin instances and close drivers
    for driver in drivers:
        driver.quit()
    for gl_instance in gl_instances:
        gl_instance.stop()
    print("Cleaned up resources.")
