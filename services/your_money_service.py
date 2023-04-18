from services.crawler_service import CrawlerService
from datasources.crawlers.your_money.your_money import YourMoneyParser
from datasources.crawlers.your_money.your_money_news_reader import YourMoneyNewsReader


class YourMoneyService(CrawlerService):
    def __init__(self, seeds):
        super().__init__(seeds)
        self.seeds = self.read_lines_from_file()
        self.parser = YourMoneyParser(self.seeds)
        self.news_reader = YourMoneyNewsReader()
        self.all_news = []

    def process(self):
        print("Processing Your Money")
        for url in self.seeds:
            print("Parsing URL: ", url)
            if url in self.visited_links:
                self.parser.current_news = dict()
                continue
            page = self.parser_page(url)
            self.parser.feed(page)
            print("News found: ", len(self.parser.news))
            for news in self.parser.news:
                print("Parsing news: ", news["link"])
                if news["link"] in self.visited_links:
                    self.news_reader.content_news = dict()
                    continue
                news_page = self.parser_page(news["link"])
                self.news_reader.feed(news_page)
                news["uuid"] = self.generate_uuid()
                news["author"] = self.news_reader.content_news["author"]
                news["content"] = self.news_reader.content_news["content"]
                news["collected_at"] = self.get_collected_date()
                self.all_news.append(news)

                self.news_reader.content_news = dict()
            self.parser.news = []
        return self.all_news
