from ugc.ugc_provider import UGCProvider
from models.model import Bookmark


class UGCBookmark(UGCProvider):
    def __init__(self):
        pass

    def generate(self):
        while True:
            yield Bookmark.random()
