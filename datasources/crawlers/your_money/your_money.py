from datasources.crawlers.white_list_html_parser import WhiteListHtmlParser
import re


class YourMoneyParser(WhiteListHtmlParser):
    def __init__(self, allowed_urls: list):
        super().__init__(allowed_url=allowed_urls)
        self.news = list()
        self.current_news = dict()
        self.is_first_news = True
        self.in_div_content = False
        self.in_div_image_feed = False
        self.in_div_content_hat = False

    def __reset_attrs(self):
        self.current_news = dict()
        self.is_first_news = True
        self.in_div_content = False
        self.in_div_image_feed = False
        self.in_div_content_hat = False

    def __remove_unsable_info(self, data: str) -> str:
        return re.sub(r",.*o/", "/", data)

    def start_new_tag(self, tag, attrs) -> bool:
        if tag == "div":
            tag_class = attrs.get("class")
            if tag_class == "stream stream-home":
                self.in_div_content = True
                return True
            if tag_class == "stream-item-container t-ultimas sd-ultimas feed":
                self.current_news["published_at"] = attrs.get("data-time")
                if self.is_first_news:
                    self.is_first_news = False
                else:
                    self.news.append(self.current_news)
                    self.current_news = dict()
                return True
            if tag_class == "feed_content_hat":
                self.in_div_content_hat = True
            elif tag_class == "ultimas_right":
                self.__reset_attrs()
            elif tag_class == "feed_image":
                self.in_div_image_feed = True
            return False
        if tag == "a" and self.in_div_content_hat:
            self.current_news["link"] = attrs.get("href")
            return True
        if tag == "img" and self.in_div_image_feed:
            self.current_news["image"] = self.__remove_unsable_info(
                attrs.get("src"))
            self.in_div_image_feed = False
            return False
        return True

    def end_tag(self, tag) -> None:
        if tag == "a" and self.in_div_content_hat:
            self.current_news["tag"] = self.get_formatted_data()
            self.in_div_content_hat = False
            return
        if tag == "h2" and self.in_div_content:
            self.current_news["title"] = self.get_formatted_data()
            return

    def readable_tags(self) -> dict:
        readable_tags = dict()
        div_tag = readable_tags.setdefault("div", set())
        a_tag = readable_tags.setdefault("a", set())
        img_tag = readable_tags.setdefault("img", set())
        h2_tag = readable_tags.setdefault("h2", set())

        div_tag.add("stream stream-home")
        div_tag.add("stream-item-container t-ultimas sd-ultimas feed")
        div_tag.add("feed_image")
        div_tag.add("ultimas_right")
        div_tag.add("feed_content_hat")
        h2_tag.add("feed_content_title")

        return readable_tags
