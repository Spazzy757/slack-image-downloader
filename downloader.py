import os
import json
import requests
import time
from datetime import datetime, timedelta

SLACK_TOKEN = "Bearer %s" % os.getenv("AUTHORIZATION_TOKEN")
SLACK_BASE_URL = os.getenv("SLACK_BASE_URL", "https://slack.com/api")
DAYS = int(os.getenv("DAYS_BACK", "365"))
WRITE_DIR = os.getenv("WRITE_DIR", "images/")

def main():
    channel_type = os.getenv("CHANNEL_TYPE")
    channel_name = os.getenv("CHANNEL_NAME")
    get_images_from_channel(channel_name, channel_type)


def get_images_from_channel(channel, mode):
    res = requests.get(
        "%s/conversations.list" % SLACK_BASE_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": SLACK_TOKEN
        },
        params={
            "types": mode
        }
    )
    if res.status_code == 200:
        data = res.json().get("channels")
        oldest = time.mktime((datetime.now() - timedelta(days=DAYS)).timetuple())
        for ch in data:
            if ch.get("name") == channel:
                count = 0
                print(ch.get("name"))
                cursor = ""
                while cursor is not None:
                    res = requests.get(
                        "%s/conversations.history?channel=%s&oldest=%s&limit=10000&cursor=%s" % (SLACK_BASE_URL, ch.get("id"), oldest, cursor),
                        headers={
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Authorization": SLACK_TOKEN
                        }
                    )
                    if res.status_code == 200:
                        cursor = res.json().get("response_metadata", {}).get("next_cursor")
                        for p in res.json().get("messages"):
                            if p.get("files"):
                                for fs in  p.get("files"):
                                    if fs.get('url_private_download'):
                                        r = requests.get(
                                            fs.get('url_private_download'),
                                            headers={
                                                "Authorization": SLACK_TOKEN
                                            },
                                            allow_redirects=True
                                        )
                                        if r.status_code == 200:
                                            count += 1
                                            open(os.path.join(WRITE_DIR, "%s-%s" % (fs.get("id"),fs.get("name"))), "wb").write(r.content)
                print(count)


if __name__ == "__main__":
    main()

