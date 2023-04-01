from services.crawler_service import CrawlerService
from datasources.crawlers.your_money.your_money import YourMoneyParser
from datasources.crawlers.your_money.your_money_news_reader import YourMoneyNewsReader


class YourMoneyService(CrawlerService):
    def __init__(self, seeds):
        super().__init__(seeds)
        self.seeds = self.read_lines_from_file()
        self.your_money_parser = YourMoneyParser(self.seeds)
        self.your_money_news_reader = YourMoneyNewsReader()
        self.all_news = []

    def process(self):
        print("Processing Your Money")
        for url in self.seeds:
            print("Parsing URL: ", url)
            page = self.parser_page(url)
            self.your_money_parser.feed(page)
            for current_news in self.your_money_parser.news:
                print("Parsing News: ", current_news["link"])
                news_page = self.parser_page(current_news["link"])
                self.your_money_news_reader.feed(news_page)
                current_news["uuid"] = self.generate_uuid()
                current_news["author"] = self.your_money_news_reader.content_news["author"]
                self.all_news.append(current_news)
                current_news["content"] = self.your_money_news_reader.content_news["content"]
                self.your_money_news_reader.content_news = dict()
            self.all_news.extend(self.your_money_parser.news)
            self.your_money_parser.news = []
        return self.all_news
