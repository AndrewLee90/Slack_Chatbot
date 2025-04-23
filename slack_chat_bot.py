from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("xoxb-aaaaaaaaaaaaaaaaaaaaaaaa")
client = WebClient(token=SLACK_BOT_TOKEN)

try:
    result = client.conversations_list()
    for channel in result["channels"]:
        print(f"채널 이름: {channel['name']}, ID: {channel['id']}")
except SlackApiError as e:
    print(f"에러: {e.response['error']}")
