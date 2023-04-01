
from datasources.crawlers.info_money.info_money import InfoMoneyParser
from datasources.crawlers.info_money.info_money_news_reader import InfoMoneyNewsReader
from services.crawler_service import CrawlerService


class InfoMoneyService(CrawlerService):
    def __init__(self, seeds):
        super().__init__(seed_file=seeds)
        self.seeds = self.read_lines_from_file()
        self.parser = InfoMoneyParser(allowed_urls=self.seeds)
        self.news_reader = InfoMoneyNewsReader()
        self.all_news = []

    def process(self) -> list:
        print("Processing InfoMoney")
        for url in self.seeds:
            print("Parsing URL: ", url)
            self.parser.category = self.get_category_from_url(url)
            page = self.parser_page(url)
            self.parser.feed(page)
            print("News found: ", len(self.parser.news))
            for news in self.parser.news:
                print("Parsing news: ", news["link"])
                news_page = self.parser_page(news["link"])
                self.news_reader.feed(news_page)
                news["uuid"] = self.generate_uuid()
                news["published_at"] = self.news_reader.content_news["published_at"]
                news["author"] = self.news_reader.content_news["author"]
                news["image"] = self.news_reader.content_news.get("image", "")
                news["content"] = self.news_reader.content_news.get(
                    "content", [])
                self.news_reader.content_news = dict()
            self.all_news.extend(self.parser.news)
            self.parser.news = []
        return self.all_news
