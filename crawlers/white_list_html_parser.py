from html.parser import HTMLParser
from abc import ABC, abstractmethod


class WhiteListHtmlParser(ABC, HTMLParser):
    def __init__(self):
        super().__init__()
        self.__readable_tags = self.readable_tags()
        self.current_data = ""
        self.should_read = False

    def __get_attrs_value_by_name(self, lst, attrs_name):
        for elem in lst:
            if elem[0] == attrs_name:
                return elem[1]
        return None

    def handle_starttag(self, tag, attrs):
        if(tag not in self.__readable_tags):
            return
        readable_classes = self.__readable_tags[tag]
        attrs_class_name = self.__get_attrs_value_by_name(attrs, "class")
        if (attrs_class_name is None or attrs_class_name not in readable_classes):
            return
        self.should_read = self.start_new_tag(tag, dict(attrs))
        self.current_data = ""

    def handle_endtag(self, tag):
        self.end_tag(tag)

    def handle_data(self, data):
        if(not self.should_read):
            return
        self.current_data += data

    @ abstractmethod
    def start_new_tag(self, tag, attrs) -> bool:
        pass

    @ abstractmethod
    def end_tag(self, tag) -> None:
        pass

    @ abstractmethod
    def readable_tags(self) -> dict:
        pass
