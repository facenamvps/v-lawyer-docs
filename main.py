import time
import unicodedata
from telethon import TelegramClient, events
from selenium import webdriver
from selenium.webdriver.common.by import By
from gologin import GoLogin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

############## ---------------Telegram API credentials
API_ID = "20231368"
API_HASH = "2194800680038835631408bb6fccd16d"
BOT_TOKEN = "8092099688:AAEgP5w17zotUFW3ScdznvJEpHviG0j0XOM"

# Channels
# SOURCE_CHANNEL = "onchain_meme"  # Source channel to listen to
SOURCE_CHANNEL = "onchaintestmeme"  # Source channel to listen to

DESTINATION_CHANNEL_ID = "@onchain_meme"  # Destination channel to repost to

gl = GoLogin({
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2JmMjUxYWViYTc5YzlhYTNhZjMzOTEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2JmMjgwNjIxZGRiZjM3OGNjNDVjMmMifQ.ZB7qnD0J5e7TW_WEJflotqTx_CRwwccAImS36JHDLEs',  # Replace with your API token
    'profile_id': '67bf25e75351cc3a556fc7bb'  # Replace with your profile ID
})

# Create a Telegram client
client = TelegramClient("session_name", API_ID, API_HASH)
debugger_address = gl.start()
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)
chrome_driver_path = f"C:/Users/Administrator/Downloads/chromedriver-win64/chromedriver.exe"  # e.g., './chromedriver' or 'chromedriver.exe'
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
####################### ------------------- TWITTER ------------------- ###########################

def remove_unsupported_characters(text):
    # Remove characters outside BMP (e.g., emojis)
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if ord(c) <= 0xFFFF)

def post_to_twitter(message):
    try:

        driver.get("https://x.com/home")
        time.sleep(5)

        # link = " t.me/onchain_meme"
        normalized_message = remove_unsupported_characters(message)
        # Click the "Post" button to open the tweet box
        post_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="SideNav_NewTweet_Button"]')
        post_button.click()
        time.sleep(2)  # Wait for the tweet box to load

        normalized_message = normalized_message
        # Find the tweet box and enter the message
        tweet_box = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
        tweet_box.send_keys(normalized_message)

        # Find and click the "Tweet" button
        tweet_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButton"]')
        time.sleep(2)
        tweet_button.click()

        print("Tweet posted successfully!")
    except Exception as e:
        print(f"Error while posting to Twitter: {e}")


# @client.on(events.NewMessage(chats=SOURCE_CHANNEL))
# async def handler(event):
#     message_text = event.message.message
#     message_reply = event.message.reply_to_msg_id
#
#     if message_reply:
#         # call_api()
#         post_to_twitter(message_text)

@client.on(events.MessageEdited(chats=SOURCE_CHANNEL))
async def edited_handler(event):
    message_text = event.message.message

    post_to_twitter(message_text)

# Start the Telegram client
client.start()
print("Listening for messages...")
client.run_until_disconnected()
