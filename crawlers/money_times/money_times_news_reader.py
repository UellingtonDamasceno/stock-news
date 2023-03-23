from crawlers.white_list_html_parser import WhiteListHtmlParser


class MoneyTimesNewsReader(WhiteListHtmlParser):
    def __init__(self):
        super().__init__()
        self.content_news = dict()

    def start_new_tag(self, tag, attrs):
        pass

    def end_tag(self, tag):
        pass

    def readable_tags(self) -> dict:
        pass
