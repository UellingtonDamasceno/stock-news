from services.info_money_service import InfoMoneyService
from services.money_times_service import MoneyTimesService
import json


def save_news(filename, news):
    with open(filename, "w") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)


def processInfoMoney():
    info_money_seeds = "seeds/info_money.txt"
    info_money_service = InfoMoneyService(info_money_seeds)
    save_news("news/infomoney.json", info_money_service.process())


def processMoneyTimes():
    money_times_seeds = "seeds/money_times.txt"
    money_times_service = MoneyTimesService(money_times_seeds)
    save_news("news/moneytimes.json", money_times_service.process())


if __name__ == "__main__":
    processInfoMoney()
    processMoneyTimes()
