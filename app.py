from datetime import datetime
import logging

from flask import Flask
import requests


ML_ID_URL = "https://mybridge-backend.herokuapp.com/api/v1/skills/mapping/machine-learning"
ML_TOP_URL = "https://mybridge-backend.herokuapp.com/api/v1/knowledge/skills/{id}?offset=0&limit=5&sort="

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)


@app.route("/")
def main():
    with requests.Session() as session:
        session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}

        # get topic ID
        response = session.get(ML_ID_URL)
        data = response.json()

        ml_topic_id = data["body"]["id"]

        # get top 5 trending topics
        response = session.get(ML_TOP_URL.format(id=ml_topic_id))
        data = response.json()

        return [
            {
                "uid": str(topic["id"]),
                "updateDate": datetime.strptime(topic["reg_date"], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%dT%H:%M:%S.%fZ"),  # "2016-04-10T00:00:00.0Z"
                "titleText": topic["title"],
                "mainText": topic["excerpt"],
                "redirectionUrl": topic["externalURL"]
            }
            for topic in data['body']
        ]
