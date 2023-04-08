from datasources.crawlers.white_list_html_parser import WhiteListHtmlParser
import re


class InfoMoneyNewsReader(WhiteListHtmlParser):
    def __init__(self):
        super().__init__(date_pattern="%Y-%m-%dT%H:%M:%S%z")
        self.content_news = dict()
        self.paragraphs = ""
        self.in_author_tag = False
        self.in_content_tag = False
        self.current_tag = None

    def start_new_tag(self, tag, attrs):
        if tag == "span":
            self.in_author_tag = True
            return False
        if tag == "time":
            date = attrs.get("datetime")
            self.content_news["published_at"] = self.format_date(date)
            return False
        if tag == "img":
            self.content_news["image"] = attrs.get("src")
            return False
        if tag == "a":
            if self.in_author_tag:
                return True
            elif not self.in_author_tag:
                return False
        if tag == "div":
            self.in_content_tag = True
            return True
        if tag == "p":
            if not self.in_content_tag:
                return False
            self.current_data = ""
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
        if tag == "div" and self.in_content_tag:
            self.content_news["content"] = self.paragraphs
            self.paragraphs = ""
            self.in_content_tag = False
        if tag == "p" and self.in_content_tag:
            self.paragraphs += " " + self.get_formatted_data()
            self.current_data = ""

            # print(paragraphs)

    def readable_tags(self):
        readable_tags = {}
        span_tag = readable_tags.setdefault("span", set())
        time_tag = readable_tags.setdefault("time", set())
        img_tag = readable_tags.setdefault("img", set())
        div_tag = readable_tags.setdefault("div", set())

        a_tag = readable_tags.setdefault("a", set())
        p_tag = readable_tags.setdefault("p", set())

        span_tag.add("typography__body--5")
        img_tag.add("imds__aspect-ratio-image wp-post-image")
        time_tag.add("entry-date published")
        time_tag.add("entry-date published updated")
        div_tag.add("element-border--bottom spacing--pb4")

        return readable_tags

    def get_formatted_data(self):
        return re.sub(r"\s{4,}", " ", self.current_data.strip())
