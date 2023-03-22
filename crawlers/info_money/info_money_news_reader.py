from crawlers.white_list_html_parser import WhiteListHtmlParser
import re


class InfoMoneyNewsReader(WhiteListHtmlParser):
    def __init__(self):
        super().__init__()
        self.content_news = dict()
        self.in_author_tag = False
        self.current_tag = None

    def start_new_tag(self, tag, attrs):
        if tag == "span":
            self.in_author_tag = True
            return False

        if tag == "a" and self.in_author_tag:
            return True

        # print("Tag: ", tag)
        # print("Attrs: ")
        # for key, value in attrs.items():
        #     print("  ", key, ":", value)

        return True

    def end_tag(self, tag):
        if(tag == "span"):
            self.in_author_tag = False
        if tag == "a" and self.in_author_tag:
            self.content_news["author"] = self.get_formatted_data()

    def readable_tags(self):
        readable_tags = {}
        span_tag = readable_tags.setdefault("span", set())
        a_tag = readable_tags.setdefault("a", set())

        span_tag.add("typography__body--5")

        return readable_tags

    def get_formatted_data(self):
        return re.sub(r"\s{4,}", " ", self.current_data.strip())
