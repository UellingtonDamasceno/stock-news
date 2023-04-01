from crawlers.white_list_html_parser import WhiteListHtmlParser


class YourMoneyNewsReader(WhiteListHtmlParser):
    def __init__(self):
        super().__init__()
        self.content_news = dict()
        self.paragraphs = ""
        self.in_content_tag = False
        self.in_author_tag = False
        self.is_first_image = True
        self.in_paragraph_tag = False

    def start_new_tag(self, tag, attrs):
        if tag == "div":
            class_name = attrs.get("class")
            if class_name == "newSingle_author_info_content_title" or class_name == "singlev2_colunista_content_title":
                self.in_author_tag = True
                return True
            if class_name == "newSingle_content_right" or class_name == "singlev2_content_right":
                self.in_content_tag = True
                return True
            if class_name == "single__footer-author":
                self.content_news["content"] = self.paragraphs
                self.paragraphs = ""
                self.in_author_tag = False
                self.in_content_tag = False
                return False
        if tag == "p" and self.in_content_tag:
            self.current_data = " "
            self.in_paragraph_tag = True
            return True

    def end_tag(self, tag):
        if tag == "div" and self.in_author_tag:
            self.content_news["author"] = self.get_formatted_data()
            self.in_author_tag = False
        if tag == "p" and self.in_paragraph_tag:
            self.paragraphs += " " + self.get_formatted_data()
            self.in_paragraph_tag = False

        return

    def readable_tags(self) -> dict:
        readable_tags = dict()
        div_tag = readable_tags.setdefault("div", set())
        p_tag = readable_tags.setdefault("p", set())
        div_tag.add("newSingle_author_info_content_title")
        div_tag.add("singlev2_colunista_content_title")
        div_tag.add("newSingle_content_right")
        div_tag.add("newSingle_content")
        div_tag.add("single__footer-author")
        return readable_tags
