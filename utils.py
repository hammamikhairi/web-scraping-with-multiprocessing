from requests import get
from datetime import datetime
from os       import environ

def notification(avg):
  token = environ.get("TELEGRAM_TOKEN")
  url = f"https://api.telegram.org/bot{token}"
  params = {"chat_id": "1077335429", "text": f"""Today's ({get_date()}) world temp is {avg}."""}
  r = get(url + "/sendMessage", params=params)
  print(r.ok)


def get_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
