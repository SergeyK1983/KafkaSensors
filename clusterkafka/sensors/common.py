class AsIterator:
    """ Асинхронный итератор """

    def __init__(self, count: int):
        self.count = count
        self.counter = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.counter >= self.count:
            raise StopAsyncIteration
        self.counter += 1
        return self.counter

