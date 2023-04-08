from html.parser import HTMLParser
from abc import ABC, abstractmethod
from datetime import datetime
from dateutil import tz
import re


class WhiteListHtmlParser(ABC, HTMLParser):
    def __init__(self, allowed_url=[], date_pattern="%Y-%m-%dT%H:%M:%S"):
        super().__init__()
        self.__readable_tags = self.readable_tags()
        self.allowed_url = allowed_url
        self.current_data = ""
        self.should_read = False
        self.tag_status = []
        self.date_pattern = date_pattern

    def __get_attrs_value_by_name(self, lst, attrs_name):
        for elem in lst:
            if elem[0] == attrs_name:
                return elem[1]
        return None

    def handle_starttag(self, tag, attrs):
        if(tag not in self.__readable_tags):
            self.tag_status.append(False)
            return
        readable_classes = self.__readable_tags[tag]
        if(len(readable_classes) == 0):
            self.tag_status.append(True)
            self.should_read = self.start_new_tag(tag, dict(attrs))
            return
        attrs_class_name = self.__get_attrs_value_by_name(attrs, "class")
        if(attrs_class_name is None or attrs_class_name not in readable_classes):
            self.tag_status.append(False)
            return
        self.tag_status.append(True)
        self.should_read = self.start_new_tag(tag, dict(attrs))
        self.current_data = ""

    def handle_endtag(self, tag):
        if(self.tag_status.pop() == True):
            self.end_tag(tag)

    def handle_data(self, data):
        if(not self.should_read):
            return
        self.current_data += data

    def is_url_allowed(self, url):
        if(len(self.allowed_url) == 0):
            return True
        for current_url in self.allowed_url:
            if url.startswith(current_url):
                return True
        return False

    @ abstractmethod
    def start_new_tag(self, tag, attrs) -> bool:
        pass

    @ abstractmethod
    def end_tag(self, tag) -> None:
        pass

    @ abstractmethod
    def readable_tags(self) -> dict:
        pass

    def get_formatted_data(self):
        return re.sub(r"\s{4,}", " ", self.current_data.strip())

    def format_date(self, date_str):
        dt = datetime.strptime(date_str, self.date_pattern)
        dt_local = dt.replace(tzinfo=tz.tzlocal())
        return dt_local.strftime("%Y-%m-%dT%H:%M:%S")
