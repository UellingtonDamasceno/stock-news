from datasources.crawlers.white_list_html_parser import WhiteListHtmlParser


class MoneyTimesNewsReader(WhiteListHtmlParser):
    def __init__(self):
        super().__init__()
        self.content_news = dict()
        self.paragraphs = ""
        self.in_content_tag = False
        self.in_author_tag = False
        self.is_first_image = True

    def start_new_tag(self, tag, attrs):
        if tag == "div":
            class_name = attrs.get("class")
            if class_name == "single__text":
                self.in_content_tag = True
                return True
            if class_name == "single-meta__author":
                self.in_author_tag = True
                return False
        if tag == "img" and self.is_first_image and self.in_content_tag:
            self.content_news["image"] = attrs.get("src")
            self.is_first_image = False
            return False
        if tag == "p" and self.in_content_tag:
            self.current_data = ""
            return True
        return True

    def end_tag(self, tag):
        if tag == "a" and self.in_author_tag:
            self.content_news["author"] = self.current_data
            self.in_author_tag = False
        if tag == "p" and self.in_content_tag:
            self.paragraphs += self.get_formatted_data()
        if tag == "article":
            self.content_news["content"] = self.paragraphs
            self.paragraphs = ""
            self.in_content_tag = False
            self.is_first_image = True

    def readable_tags(self) -> dict:
        readable_tags = dict()
        img_tag = readable_tags.setdefault("img", set())
        div_tag = readable_tags.setdefault("div", set())
        a_tag = readable_tags.setdefault("a", set())

        div_tag.add("single__text")
        div_tag.add("single-meta__author")
        return readable_tags
