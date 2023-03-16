from crawlers.white_list_html_parser import WhiteListHtmlParser
import re


class InfoMoneyParser(WhiteListHtmlParser):

    def __init__(self, category="S/C"):
        super().__init__()
        self.category = category
        self.current_news = dict()
        self.current_tag = None
        self.news = []
        self.in_article = False
        self.in_section = False

    def start_new_tag(self, tag, attrs):
        if(tag == "section"):
            self.in_section = True
        elif(tag == "article"):
            self.in_article = True
        elif(tag == "a"):
            self.current_news["link"] = attrs.get("href")
            self.current_news["tag"] = self.get_formatted_data()
        elif(tag == "h3"):
            self.current_news["title"] = self.get_formatted_data()

        self.current_news["category"] = self.category
        # print("Tag: ", tag)
        # print("Attrs: ")
        # for key, value in attrs.items():
        #     print("  ", key, ":", value)

        return True

    def end_tag(self, tag):
        if(tag == "article" and self.in_section):
            self.current_news["title"] = self.get_formatted_data()
            self.news.append(self.current_news)
            self.current_news = dict()

        if(tag == "section"):
            self.in_section = False

    def readable_tags(self):
        readable_tags = {}
        a_tag = readable_tags.setdefault("a", set())
        h3_tag = readable_tags.setdefault("h3", set())
        article_tag = readable_tags.setdefault("article", set())
        section_tag = readable_tags.setdefault("section", set())

        a_tag.add("article-card__headline-link")
        a_tag.add("article-card__asset-link")
        h3_tag.add("article-card__headline")
        article_tag.add("article-card")
        section_tag.add("articlespack-list")

        return readable_tags

    def get_formatted_data(self):
        return re.sub(r"\s{4,}", " ", self.current_data.strip())
