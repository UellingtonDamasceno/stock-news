from services.crawler_service import CrawlerService
from crawlers.money_times.money_times import MoneyTimesParser
from crawlers.money_times.money_times_news_reader import MoneyTimesNewsReader


class MoneyTimesService(CrawlerService):
    def __init__(self, seeds):
        super().__init__(seed_file=seeds)
        self.seeds = self.read_lines_from_file()
        self.parser = MoneyTimesParser(allowed_urls=self.seeds)
        self.news_reader = MoneyTimesNewsReader()
        self.all_news = []

    def process(self):
        print("Processing MoneyTimes")
        for seed in self.seeds:
            print("Processing seed: ", seed)
            self.parser.feed(self.parser_page(seed))
            self.all_news.extend(self.parser.news)
        return self.all_news
