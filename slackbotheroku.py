import os
import datetime
import pytz
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# .env 파일에서 환경변수 불러오기
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
if not SLACK_BOT_TOKEN:
    print("에러: SLACK_BOT_TOKEN이 .env 파일에 설정되지 않았습니다.")
    exit(1)

CHANNEL_ID = "C08NQGXKCT0"  # 회의록 채널 ID

client = WebClient(token=SLACK_BOT_TOKEN)

def is_workday(date):
    return date.weekday() < 5  # 월~금만 True

def schedule_daily_message():
    today = datetime.date.today()
    if not is_workday(today):
        print("오늘은 워크데이가 아닙니다. 스케줄링 건너뜀.")
        return

    kst = pytz.timezone("Asia/Seoul")
    scheduled_time = kst.localize(datetime.datetime.combine(today, datetime.time(hour=9, minute=0)))
    schedule_timestamp = int(scheduled_time.timestamp())
    message_date = today.strftime("%Y-%m-%d")

    try:
        result = client.chat_scheduleMessage(
            channel=CHANNEL_ID,
            text=f"[{message_date}] 회의록",
            post_at=schedule_timestamp
        )
        print(f"메시지 스케줄링 성공: [{message_date}] 회의록")
    except SlackApiError as e:
        print(f"에러: {e.response['error']}")

if __name__ == "__main__":
    schedule_daily_message()
