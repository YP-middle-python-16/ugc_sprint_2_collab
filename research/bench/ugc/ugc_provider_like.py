from ugc.ugc_provider import UGCProvider
from models.model import Like


class UGCLike(UGCProvider):
    def __init__(self):
        pass

    def generate(self):
        while True:
            yield Like.random()
