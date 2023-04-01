from services.info_money_service import InfoMoneyService
from services.money_times_service import MoneyTimesService
from services.your_money_service import YourMoneyService
from mqtt.publisher import Publisher
from dotenv import load_dotenv
import json
import os


def send_news(news: list, publisher: Publisher):
    for new in news:
        new_json = json.dumps(new, ensure_ascii=False)
        print("Publishing: ", new["title"])
        publisher.publish("stock-news/news", new_json)


def save_news(filename, news):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)


def processInfoMoney(publisher: Publisher):
    info_money_seeds = "seeds/info_money.txt"
    info_money_service = InfoMoneyService(info_money_seeds)
    news = info_money_service.process()
    save_news("news/infomoney.json", news)
    send_news(news, publisher)


def processMoneyTimes(publisher: Publisher):
    money_times_seeds = "seeds/money_times.txt"
    money_times_service = MoneyTimesService(money_times_seeds)
    news = money_times_service.process()
    save_news("news/moneytimes.json", news)
    send_news(news, publisher)


def processYourMoney(publisher: Publisher):
    your_money_seeds = "seeds/your_money.txt"
    your_money_service = YourMoneyService(your_money_seeds)
    news = your_money_service.process()
    save_news("news/yourmoney.json", news)
    send_news(news, publisher)


def create_publisher():
    load_dotenv()
    host = str(os.getenv("MQTT_HOST"))
    port = int(os.getenv("MQTT_PORT"))
    username = str(os.getenv("MQTT_USERNAME"))
    password = str(os.getenv("MQTT_PASSWORD"))
    return Publisher(host, username, password, port)


if __name__ == "__main__":
    publisher = create_publisher()
    publisher.connect()
    processInfoMoney(publisher)
    processMoneyTimes(publisher)
    processYourMoney(publisher)
    publisher.disconnect()
