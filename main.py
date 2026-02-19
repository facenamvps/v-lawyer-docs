import asyncio
import os
import random
import re
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
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import pyperclip
from selenium.webdriver.common.keys import Keys
import requests

############## ---------------Telegram API credentials
API_ID = "20231368"
API_HASH = "2194800680038835631408bb6fccd16d"
BOT_TOKEN = "8092099688:AAEgP5w17zotUFW3ScdznvJEpHviG0j0XOM"

# Channels
# SOURCE_CHANNEL = "onchain_meme"  # Source channel to listen to
# SOURCE_CHANNEL = -1002572353866  # Source channel to listen to
SOURCE_CHANNEL = "postintweet"  # Source channel to listen to
footer_path = f"C:/Users/Administrator/Downloads/changetext/footer.txt"
bio_path = f"C:/Users/Administrator/Downloads/changetext/bio.txt"
header_path = f"C:/Users/Administrator/Downloads/changetext/header.txt"
found_path = f"C:/Users/Administrator/Downloads/changetext/found.txt"
advice_path = f"C:/Users/Administrator/Downloads/changetext/advice.txt"
group_path = f"C:/Users/Administrator/Downloads/changetext/group.txt"
comment_path = f"C:/Users/Administrator/Downloads/changetext/comment.txt"

DESTINATION_CHANNEL_ID = "@onchain_meme"  # Destination channel to repost to
client = TelegramClient("session_name", API_ID, API_HASH)


profiles = [
    {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2JmMjUxYWViYTc5YzlhYTNhZjMzOTEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2JmMjgwNjIxZGRiZjM3OGNjNDVjMmMifQ.ZB7qnD0J5e7TW_WEJflotqTx_CRwwccAImS36JHDLEs',
        'profile_id': '67c2db00cf918ba0d64151bc'  # Profile 1 ID
    },
    {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2JmMjUxYWViYTc5YzlhYTNhZjMzOTEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2JmMjgwNjIxZGRiZjM3OGNjNDVjMmMifQ.ZB7qnD0J5e7TW_WEJflotqTx_CRwwccAImS36JHDLEs',
        'profile_id': '68161df91435710135d75ff9'  # Replace with your Profile 2 ID
    },
    {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2JmMjUxYWViYTc5YzlhYTNhZjMzOTEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2JmMjgwNjIxZGRiZjM3OGNjNDVjMmMifQ.ZB7qnD0J5e7TW_WEJflotqTx_CRwwccAImS36JHDLEs',
        'profile_id': '6819b216385b45dde088860f'  # Replace with your Profile 3 ID
    }
]

cookies = {
        "auth-refresh-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWZyZXNoVG9rZW5JZCI6IjQxNWJkOTI0LTAxYTctNDU5Ny1iZjBhLWFhNzVhMzJlMTAwOCIsImlhdCI6MTc0NTM5MDA4MH0.XZYgGlmNLOhXhcwwVE8LTgFzmpVcwy2esJO9mFMbeao",
        "auth-access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoZW50aWNhdGVkVXNlcklkIjoiZTczNGVlMjEtMGYyNy00ODI4LWI2MmUtYjczZDlkZTZhNWVkIiwiaWF0IjoxNzQ1NTQwOTI0LCJleHAiOjE3NDU1NDE4ODR9.HmsRMsKkgMRgRekuBF1fTDXnq2WAyyeFabuUf-NvyKs"
    }

chrome_driver_path = f"C:/Users/Administrator/Downloads/chromedriver-win64/chromedriver.exe"
chrome_driver_chart_path = f"C:/Users/Administrator/Downloads/chromedriver-win64-chart/chromedriver.exe"

# create new driver for chart screen shot
chrome_options_chart = Options()
chrome_options_chart.add_argument("--start-maximized")

# Set up the driver (update the path to your chromedriver)
service_chart = Service(executable_path=chrome_driver_chart_path)
driver_chart = webdriver.Chrome(service=service_chart, options=chrome_options_chart)


BASE_PORT = 3500
MAX_RETRIES = 3

drivers = []
gl_instances = []
valid_profiles = {}
# Create a Telegram client
for i, profile in enumerate(profiles):
    port = BASE_PORT + i
    gl = GoLogin({
        'token': profile['token'],
        'profile_id': profile['profile_id'],
        'port': port
    })

    debugger_address = None
    retries = 0
    while retries < MAX_RETRIES:
        try:
            print(f"Starting profile {profile['profile_id']} (attempt {retries + 1})...")

            debugger_address = gl.start()
            # asyncio.sleep(5)  # Ensure the profile fully starts

            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", debugger_address)
            service = Service(executable_path=chrome_driver_path)

            driver = webdriver.Chrome(service=service, options=chrome_options)
            drivers.append(driver)
            gl_instances.append(gl)
            valid_profiles[i] = profile['profile_id']

            print(f"✅ Successfully started driver for profile {profile['profile_id']}")
            break  # Exit retry loop if successful
        except Exception as e:
            print(f"❌ Failed to start driver for profile {profile['profile_id']}: {e}")
            retries += 1
            asyncio.sleep(3)  # Wait before retrying

    if not debugger_address:
        print(f"⚠️ Skipping profile {profile['profile_id']} due to repeated failures.")

    print(f"\n✅ Total drivers started: {len(valid_profiles)}/{len(profiles)}")

    # Stop script if no drivers started
    if not drivers:
        print("❌ No drivers started successfully. Exiting...")
        exit()

####################### ------------------- TWITTER ------------------- ###########################

def get_last_line(message_text):
    lines = message_text.split("\n")
    profile_id = lines[-1].strip()  # Get the last line
    return profile_id

def extract_token_id(message_text):
    lines = message_text.splitlines()
    token_id = lines[1].strip()
    return token_id

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

def format_message(token_id, token_name):
    header = get_random_line(header_path)
    footer = get_random_line(footer_path)
    quick_buy = f"Quick Buy: https://t.me/onchain_meme"
    found = get_random_line(found_path)
    # updated_message = message.replace("Market found:", token_id).replace(" Market Now:", "")
    bio = get_random_line(bio_path)
    footer_tag = "#SOL #BNB #ETH #MEMECoin #ONCHAIN_MEME"
    # format token_name
    if len(token_name) > 6 or re.search(r'\d', token_name):
        message_token_name = f"I'm done Pnl #{token_name}"
    else:
        message_token_name = f"I'm done Pnl ${token_name}"
    return f"{header} \n\n {message_token_name} \n\n {token_id} \n\n {quick_buy} \n\n {footer_tag}"

def remove_last_line(text):
    lines = text.split('\n')  # Split the message into lines
    lines = lines[:-1]  # Remove the last line
    return '\n'.join(lines)  # Rejoin the lines back into a single string

def remove_unsupported_characters(text):
    # Remove characters outside BMP (e.g., emojis)
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if ord(c) <= 0xFFFF)


async def like_twitter(message, token_id, i):
    # Use the first driver instance (adjust if necessary)
    driver = drivers[i]
    driver.execute_script("window.focus();")
    driver.get(f"https://x.com/search?q={token_id}&src=typed_query&f=live")
    await asyncio.sleep(10)

    for _ in range(2):

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(5)

        try:
            like_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="like"]'))
            )

            driver.execute_script("arguments[0].click();", like_button)
            await asyncio.sleep(5)
        except (StaleElementReferenceException, NoSuchElementException):
            continue

async def get_pair_token(token_id):
    # URL for the request
    url = f"https://api3.axiom.trade/search?searchQuery={token_id}&isOg=false&isPumpOnly=false"

    # Headers to send with the request
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }

    # Send the GET request
    response = requests.get(url, headers=headers, cookies=cookies)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the 'pairAddress' from the first element (assuming the structure is consistent)
        pair_address = data[0].get("pairAddress", None)

        if pair_address:
            return pair_address
        else:
            print("Pair address not found.")
    else:
        print(f"Request failed with status code {response.status_code}")

async def snapshot_chart(driver, token_id):
    # Get pair_token
    pair_token = await get_pair_token(token_id)

    axiom_url = f"https://axiom.trade/meme/{pair_token}"
    driver.get(axiom_url)

    await asyncio.sleep(10)

    element = driver.find_element(By.CSS_SELECTOR, ".flex.flex-1.flex-row.min-h-0.overflow-hidden.relative")
    image_capture_path = "chart_screenshot.png"
    # Take a screenshot of the specific element
    return element.screenshot(image_capture_path)

async def comment_twitter(i):
    # Use the first driver instance (adjust if necessary)
    driver = drivers[i]
    driver.execute_script("window.focus();")
    for _ in range(2):
        driver.get("https://x.com/home")
        await asyncio.sleep(15)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(5)
        # --- PART 1: Click the Tweet-User-Avatar in the second cell element ---
        cell_divs = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')
        first_post = cell_divs[2]
        # print(f"find first_post is ok")

        driver.execute_script("arguments[0].click();", first_post)

        try:
            like_button = WebDriverWait(first_post, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="like"]'))
            )

            driver.execute_script("arguments[0].click();", like_button)
            print(f"click like is ok")
            await asyncio.sleep(5)
        except (StaleElementReferenceException, NoSuchElementException):
            continue

        try:
            tweet_user = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="reply"]'))
            )

            # driver.execute_script("arguments[0].scrollIntoView(true);", tweet_user)
            await asyncio.sleep(2)
        except (StaleElementReferenceException, NoSuchElementException):
            continue

        if tweet_user:
            driver.execute_script("arguments[0].click();", tweet_user)
            print(f"click tweet_user is ok")

        await asyncio.sleep(5)

        # Find tweet textarea and enter temporary text
        try:
            tweet_text_area = driver.find_element(By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']")
            # print(f"find tweet_text_area is ok")
        except (StaleElementReferenceException, NoSuchElementException):
            continue

        comment_text = get_random_line(comment_path)
        if tweet_text_area:
            tweet_text_area.send_keys(comment_text)

        await asyncio.sleep(5)

        try:
            tweet_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="tweetButton"]')
        except (StaleElementReferenceException, NoSuchElementException):
            continue

        if tweet_button:
            # tweet_button.click()
            # print(f"click tweet_button is ok")
            driver.execute_script("arguments[0].click();", tweet_button)
            print(f"find tweet_button is ok")

        # else:
        #     print("Tweet reply button not found or error updating tweet textarea.")

        await asyncio.sleep(5)  # Additional delay before closing the reply dialog
def take_screen_chart(token_id):
    chrome_options_chart = Options()
    chrome_options_chart.add_argument("--start-maximized")

    # Set up the driver (update the path to your chromedriver)
    service_chart = Service('path/to/chromedriver')  # e.g., 'C:/WebDriver/bin/chromedriver.exe'
    driver_chart = webdriver.Chrome(service=service_chart, options=chrome_options_chart)

    # Open the target URL
    driver_chart.get('https://axiom.trade/meme')
async def post_to_twitter(message, token_id, image_path, i):
    # Sequential posting
    driver = drivers[i]
    driver.execute_script("window.focus();")
    profile_id = profiles[i]['profile_id']
    # print(message)
    for _ in range(1):
        group = get_random_line(group_path)
        try:
            pair_token = await get_pair_token(token_id)

            axiom_url = f"https://axiom.trade/meme/{pair_token}"
            driver_chart.get(axiom_url)
            await asyncio.sleep(10)

            driver_chart.execute_script("""
                    const modal = document.querySelector('div.fixed.inset-0');
                    if (modal) {
                        modal.remove();
                    }
                """)

            element = driver_chart.find_element(By.CSS_SELECTOR, ".flex.flex-1.flex-row.min-h-0.overflow-hidden.relative")
            image_chart_path = "chart_screenshot.png"
            # Take a screenshot of the specific element
            element.screenshot(image_chart_path)

            driver.get("https://x.com/home")
            await asyncio.sleep(10)

            if image_path:
                absolute_token_image = os.path.abspath(image_path)

                # Get the absolute paths for the image
                absolute_chart_image = os.path.abspath(image_chart_path)
                # upload_image = driver.find_element(By.CSS_SELECTOR, '[data-testid="fileInput"]')
                upload_image = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="fileInput"]'))
                )

                upload_image.send_keys(f"{absolute_chart_image}\n{absolute_token_image}")
                # upload_image.send_keys(f"{absolute_token_image}")

            await asyncio.sleep(2)

            driver.execute_script("""
                var editor = document.querySelector('div[role="textbox"][data-testid="tweetTextarea_0"]');
                if (editor) {
                    editor.focus();
                    document.execCommand('insertHTML', false, arguments[0]);
                }
            """, message)

            await asyncio.sleep(2)

            # tweet_button_post = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButton"]')

            # Post button in home
            tweet_button_post = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]')
            if tweet_button_post:
                driver.execute_script("arguments[0].click();", tweet_button_post)

        except Exception as e:
            print(f"Error with driver {i} (profile {profile_id}): {e}")
        await asyncio.sleep(10)  # Delay between posts


@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    new_message = event.message
    new_message_text = new_message.message
    random_profile_id = get_last_line(new_message_text)

    try:
        image_path = None

        if new_message.media and isinstance(new_message.media, MessageMediaPhoto):
            image_path = await new_message.download_media()

        for i, profile_id in valid_profiles.items():
            try:

                if new_message_text == "comment":
                    await comment_twitter(None, i)
                elif new_message_text == "like":
                    await like_twitter(i)
                else:
                    if random_profile_id == profile_id:
                        new_message_text = remove_last_line(new_message_text)
                        token_id = get_last_line(new_message_text)
                        new_message_text = remove_last_line(new_message_text)
                        await post_to_twitter(new_message_text,token_id , image_path, i)
                        await like_twitter(new_message_text, token_id, i)
            except Exception as e:
                print(f"Error processing profile {profile_id}: {e}")

        try:
            os.remove(image_path)
        except Exception as e:
            print(f"Error removing file {image_path}: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")



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
