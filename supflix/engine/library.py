from collections import defaultdict


class MediaLibrary:

    def __init__(self):
        self.library = {}

    def add(self, media):

        key = (
            media.title.lower(),
            media.year,
            media.type,
            media.season
        )

        if key not in self.library:

            self.library[key] = {
                "media": media,
                "qualities": {}
            }

        self.library[key]["qualities"][media.quality] = media

    def get(self, title):

        for item in self.library.values():

            if item["media"].title.lower() == title.lower():
                return item

        return None

    def all(self):
        return list(self.library.values())