import json

from ugc.ugc_provider import UGCProvider
from models.model import Bookmark


class UGCBookmark(UGCProvider):
    def __init__(self):
        self.label = 'Bookmark'

    def generate(self, limit):
        counter = 0

        while counter <= limit:
            counter = counter + 1
            yield Bookmark.random()
