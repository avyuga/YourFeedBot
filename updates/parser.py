from bs4 import BeautifulSoup
import requests
import datetime


def is_protected(channel_link):
    return


def check_updates(channel_link, last_message_time: datetime.datetime):
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
    result = ""
    new_date = None
    for message in messages:
        tag_text = message.find("div", {"class": "tgme_widget_message_text"})
        tag_date = message.find("time", {"class": "time"})
        time_string = tag_date['datetime']
        if new_date is None: new_date = time_string
        timing = datetime.datetime.strptime(time_string, f"%Y-%m-%dT%H:%M:%S+{time_string[-5:]}")
        if timing <= last_message_time: break
        print(f"Channel: {URL}, Message: {tag_text.get_text()}, Time: {timing}")
        str_time = datetime.datetime.strftime(timing, "%d.%m.%Y, %H:%M:%S")
        result += f"*\u2022At {str_time}:* \n{tag_text.get_text()}\n"
    if result != '':
        result = f"*Channel {URL} has sent:*\n" + result
    return result, new_date

