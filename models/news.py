import json


class News:
    def __init__(self):
        self.category
        self.link
        self.tag
        self.title
        self.content
        self.published_at
        self.author
        self.image

    def toJson(self):
        return json.dumps(self.__dict__)

    @classmethod
    def fromJson(cls, json_string):
        data = json.loads(json_string)
        return cls(**data)
