from services.crawler_service import CrawlerService
from datasources.crawlers.money_times.money_times import MoneyTimesParser
from datasources.crawlers.money_times.money_times_news_reader import MoneyTimesNewsReader


class MoneyTimesService(CrawlerService):
    def __init__(self, seeds):
        super().__init__(seed_file=seeds)
        self.seeds = self.read_lines_from_file()
        self.parser = MoneyTimesParser(allowed_urls=self.seeds)
        self.news_reader = MoneyTimesNewsReader()
        self.all_news = []

    def process(self):
        url = "https://www.moneytimes.com.br/page/"
        print("Processing MoneyTimes")
        for i in range(1, 2):
            print("Processing seed: ", url, str(i))
            self.parser.feed(self.parser_page(url + str(i)))
            for news in self.parser.news:
                print("Processing news: ", news["link"])
                news_page = self.parser_page(news["link"])
                self.news_reader.feed(news_page)
                news["uuid"] = self.generate_uuid()
                news["author"] = self.news_reader.content_news["author"]
                news["image"] = self.news_reader.content_news.get(
                    "image", "")
                news["content"] = self.news_reader.content_news.get(
                    "content")
                self.all_news.extend(self.parser.news)
                self.parser.news = []
        return self.all_news
