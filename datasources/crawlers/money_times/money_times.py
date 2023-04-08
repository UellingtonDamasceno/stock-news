from datasources.crawlers.white_list_html_parser import WhiteListHtmlParser


class MoneyTimesParser(WhiteListHtmlParser):
    def __init__(self, allowed_urls: list):
        super().__init__(allowed_urls, "%d/%m/%Y - %H:%M")
        self.current_news = dict()
        self.news = []
        self.in_div_news_list = False
        self.in_div_news_item = False
        self.in_div_news_category = False
        self.in_div_meta = False

    def start_new_tag(self, tag, attrs):
        if tag == "div" and attrs.get("class") == "news-list":
            self.in_div_news_list = True
            return True

        if tag == "div":
            att_class = attrs.get("class")
            if att_class == "news-item":
                self.in_div_news_item = True
            elif att_class == "news-item__category":
                self.in_div_news_category = True
            elif att_class == "news-item__meta":
                self.in_div_meta = True
            return True

        if tag == "span" and self.in_div_meta:
            return True

        if tag == "a":
            self.current_news["link"] = attrs.get("href")
            return True

    def end_tag(self, tag):
        if tag == "div" and self.in_div_news_category:
            self.in_div_news_category = False
        elif tag == "div" and self.in_div_news_item:
            self.news.append(self.current_news)
            self.current_news = dict()
            self.in_div_news_item = False
        elif(tag == "a" and self.in_div_news_category):
            self.current_news["tag"] = self.current_data.strip()
        elif tag == "div" and self.in_div_news_list:
            self.in_div_news_list = False
        elif tag == "h2" and self.in_div_news_item:
            self.current_news["title"] = self.current_data.strip()
        elif tag == "span" and self.in_div_meta:
            date = self.current_data.strip()
            self.current_news["published_at"] = self.format_date(date)
            self.in_div_meta = False

    def readable_tags(self) -> dict:
        readable_tags = {}
        div_tag = readable_tags.setdefault("div", set())
        a_tag = readable_tags.setdefault("a", set())
        h2_tag = readable_tags.setdefault("h2", set())
        span_tag = readable_tags.setdefault("span", set())

        div_tag.add("news-item")
        div_tag.add("news-list")
        div_tag.add("news-item__category")
        div_tag.add("news-item__meta")
        h2_tag.add("news-item__title")
        span_tag.add("date")

        return readable_tags
