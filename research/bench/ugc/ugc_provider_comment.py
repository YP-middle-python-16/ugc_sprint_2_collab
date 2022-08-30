from ugc.ugc_provider import UGCProvider
from models.model import Comment


class UGCComment(UGCProvider):
    def __init__(self):
        pass

    def generate(self):
        while True:
            yield Comment.random()
