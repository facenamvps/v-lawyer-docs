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
from telethon.tl.types import MessageMediaPhoto
import pyperclip
from selenium.webdriver.common.keys import Keys

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
now_path = f"C:/Users/Administrator/Downloads/changetext/now.txt"
group_path = f"C:/Users/Administrator/Downloads/changetext/group.txt"
comment_path = f"C:/Users/Administrator/Downloads/changetext/comment.txt"

DESTINATION_CHANNEL_ID = "@onchain_meme"  # Destination channel to repost to
client = TelegramClient("session_name", API_ID, API_HASH)


profiles = [
    # {
    #     'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2JmMjUxYWViYTc5YzlhYTNhZjMzOTEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2JmMjgwNjIxZGRiZjM3OGNjNDVjMmMifQ.ZB7qnD0J5e7TW_WEJflotqTx_CRwwccAImS36JHDLEs',
    #     'profile_id': '67c2db00cf918ba0d64151bc'  # Profile 1 ID
    # },
    # {
    #     'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2JmMjUxYWViYTc5YzlhYTNhZjMzOTEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2JmMjgwNjIxZGRiZjM3OGNjNDVjMmMifQ.ZB7qnD0J5e7TW_WEJflotqTx_CRwwccAImS36JHDLEs',
    #     'profile_id': '67c64b4dd858809e6118a287'  # Replace with your Profile 2 ID
    # },
    {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2JmMjUxYWViYTc5YzlhYTNhZjMzOTEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2JmMjgwNjIxZGRiZjM3OGNjNDVjMmMifQ.ZB7qnD0J5e7TW_WEJflotqTx_CRwwccAImS36JHDLEs',
        'profile_id': '67efa30d9d2da139461e2ef9'  # Replace with your Profile 3 ID
    }
]

chrome_driver_path = f"C:/Users/Administrator/Downloads/chromedriver-win64/chromedriver.exe"

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
    now = get_random_line(now_path)
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


async def like_twitter(i):
    # Use the first driver instance (adjust if necessary)
    driver = drivers[i]
    driver.execute_script("window.focus();")
    for _ in range(2):
        driver.get("https://x.com/home")
        await asyncio.sleep(10)

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


async def snapshot_chart(driver, token_id):
    # Open a new tab
    driver.execute_script("window.open();")

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])

    # Navigate to the page
    driver.get(f"https://axiom.trade/meme/{token_id}")
    await asyncio.sleep(5)  # Wait for the page to load

    element = driver.find_element(By.CSS_SELECTOR, ".flex.flex-1.flex-row.min-h-0.overflow-hidden.relative")

    # Take a screenshot of the specific element
    image_path = element.screenshot("chart_screenshot.png")

    # Close the current tab
    driver.close()

    # Switch back to the original tab
    driver.switch_to.window(driver.window_handles[0])

    return image_path

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

async def post_to_twitter(message, image_path, i):
    # Sequential posting
    token_id = extract_token_id(message)
    driver = drivers[i]
    driver.execute_script("window.focus();")
    profile_id = profiles[i]['profile_id']
    # print(message)
    for _ in range(1):
        group = get_random_line(group_path)
        try:
            driver.get("https://x.com/home")
            await asyncio.sleep(10)

            # This feature post in community
            # try:
            #     tweet_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="SideNav_NewTweet_Button"]')
            #     # print(f"find tweet_button is ok")
            # except (StaleElementReferenceException, NoSuchElementException):
            #     # print(f"can not find tweet_button")
            #     continue
            #
            # if tweet_button:
            #     driver.execute_script("arguments[0].click();", tweet_button)
            #     # print(f"click tweet_button is ok")
            #
            # await asyncio.sleep(5)

            if image_path:
                absolute_image_path = os.path.abspath(image_path)

                image_capture_path = await snapshot_chart(driver, token_id)  # This will give you the correct image path

                # Get the absolute paths for the image
                absolute_image_capture = os.path.abspath(image_capture_path)
                # upload_image = driver.find_element(By.CSS_SELECTOR, '[data-testid="fileInput"]')
                upload_image = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="fileInput"]'))
                )

                upload_image.send_keys(f"{absolute_image_capture}\n{absolute_image_path}")

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
    # message_reply = event.message.reply_to_msg_id
    # history = await client.get_messages(SOURCE_CHANNEL, limit=3)

    # if len(history) > 1:
        # previous_message = history[1]  # previous message is at index 1
        # previous_message_1 = history[2]

        # if "/pnl" in previous_message.text:
            # your logic here
            # print("Found '/pnl' in previous message.")
    try:
        image_path = None
        if new_message.media and isinstance(new_message.media, MessageMediaPhoto):
            image_path = await new_message.download_media()

        for i, profile_id in valid_profiles.items():
            try:

                if new_message_text == "comment":
                    await comment_twitter(i)
                elif new_message_text == "like":
                    await like_twitter(i)
                else:
                    await post_to_twitter(new_message_text, image_path, i)
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
