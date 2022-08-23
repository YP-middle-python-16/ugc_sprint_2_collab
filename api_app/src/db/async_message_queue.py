from abc import ABC, abstractmethod


class AsyncMessageQueue(ABC):
    @abstractmethod
    async def send(self, topic: str, key: str, value: str):
        pass
