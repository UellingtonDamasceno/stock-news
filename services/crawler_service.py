from abc import ABC, abstractmethod
import urllib.request
import uuid
from datetime import datetime


class CrawlerService(ABC):
    def __init__(self, seed_file: str):
        self.seed_file = seed_file
        self.visited_links = set()

    @abstractmethod
    def process(self):
        pass

    def generate_uuid(self) -> str:
        return str(uuid.uuid4())

    def get_category_from_url(self, url):
        return url[url.rfind("/") + 1:].replace("\n", "")

    def read_lines_from_file(self):
        lines = []
        print("Reading seeds from file: ", self.seed_file)
        with open(self.seed_file, "r") as f:
            for url in f.readlines():
                lines.append(url.replace("\n", ""))
        return lines

    def parser_page(self, url):
        req = urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0'})
        self.visited_links.add(url)
        return urllib.request.urlopen(req).read().decode("utf-8")

    def get_collected_date(self):
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
