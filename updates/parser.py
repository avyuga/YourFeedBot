from bs4 import BeautifulSoup
import requests
import datetime


def check_updates(channel_link, last_message: datetime.datetime):
    URL = f"https://t.me/s/{channel_link}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    history = soup.find("section", {"class": "tgme_channel_history"})
    # todo вынести случай, когда канал защищен от копирования - в изначальную проверку
    # если истории нет, то канал защищен от копирования
    if history.is_empty_element:
        return None
    messages = history.find_all("div", {"class": 'tgme_widget_message_wrap'})
    messages = messages[::-1]
    result = []
    for message in messages:
        tag_text = message.find("div", {"class": "tgme_widget_message_text"})
        tag_date = message.find("time", {"class": "time"})
        time_string = tag_date['datetime']
        timing = datetime.datetime.strptime(time_string, f"%Y-%m-%dT%H:%M:%S+{time_string[-5:]}")
        if timing >= last_message: break
        print(f"Message: {tag_text.get_text()}, Time: {timing}")
        result += [{tag_text.get_text(), timing}]
    return result

