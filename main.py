import ahocorasick
from services.info_money_service import InfoMoneyService
from services.money_times_service import MoneyTimesService
from services.your_money_service import YourMoneyService
from mqtt.publisher import Publisher
from datasources.brapi.brapi_client import BrapiClient
from dotenv import load_dotenv
import json
import os
import time


def send_news(news: list, publisher: Publisher):
    for new in news:
        new_json = json.dumps(new, ensure_ascii=False)
        print("Publishing: ", new["title"])
        publisher.publish("stock-news/news", new_json)


def save_in_file(filename, news):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)


def processInfoMoney():
    info_money_seeds = "seeds/info_money.txt"
    info_money_service = InfoMoneyService(info_money_seeds)
    return info_money_service.process()


def processMoneyTimes():
    money_times_seeds = "seeds/money_times.txt"
    money_times_service = MoneyTimesService(money_times_seeds)
    return money_times_service.process()


def processYourMoney():
    your_money_seeds = "seeds/your_money.txt"
    your_money_service = YourMoneyService(your_money_seeds)
    return your_money_service.process()


def create_publisher():
    load_dotenv()
    host = str(os.getenv("MQTT_HOST"))
    port = int(os.getenv("MQTT_PORT"))
    username = str(os.getenv("MQTT_USERNAME"))
    password = str(os.getenv("MQTT_PASSWORD"))
    return Publisher(host, username, password, port)


def extract_details(quote):
    return {
        "stock": quote['stock'],
        "name": quote['name'],
        "logo": quote['logo']
    }


def read_all_companies():
    if not os.path.exists("companies.json"):
        brapi_client = BrapiClient("https://brapi.dev")
        stock_list = brapi_client.get_quote_list()["stocks"]
        quotes = list(map(extract_details, stock_list))
        save_in_file("companies.json", quotes)
        return quotes
    with open("companies.json", "r") as f:
        return json.load(f)


def fill_mentioned_companies(news, companies) -> set:
    automaton = ahocorasick.Automaton()
    for i, company in enumerate(companies):
        automaton.add_word(company["stock"], (i, company["stock"]))
    automaton.make_automaton()
    for new in news:
        mentioned_companies = find_companies(new["content"], automaton)
        mentioned_companies.update(find_companies(new["title"], automaton))
        new["mentioned_companies"] = list(mentioned_companies)
    return news


def find_companies(news, automaton) -> set:
    mentioned_companies = set()
    for _, company in automaton.iter(news):
        if len(company) == 0:
            continue
        mentioned_companies.add(company[1])
    return mentioned_companies


if __name__ == "__main__":
    start_time = time.time()
    companies = read_all_companies()
    publisher = create_publisher()
    publisher.connect()
    news = processInfoMoney()
    news.extend(processMoneyTimes())
    news.extend(processYourMoney())
    fill_mentioned_companies(news, companies)
    save_in_file("news/all.json", news)
    send_news(news, publisher)
    publisher.disconnect()
    print("Total time: ", time.time() - start_time)
