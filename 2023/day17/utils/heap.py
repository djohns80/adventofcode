#!/usr/bin/env python3

import heapq
import itertools


# From https://docs.python.org/3/library/heapq.html, sorry Algo profs :(
class HeapQueue:
    def __init__(self):
        self.queue = []
        self.data = {}
        self.removed = ""
        self.counter = itertools.count()
        self.length = 0

    def insert(self, key, value):
        if key in self.data:
            self.remove(key)
        new_count = next(self.counter)
        entry = [value, new_count, key]
        self.data[key] = entry
        heapq.heappush(self.queue, entry)
        self.length += 1

    def remove(self, key):
        entry = self.data.pop(key)
        entry[-1] = self.removed
        self.length -= 1

    def pop(self):
        while self.queue:
            _, _, key = heapq.heappop(self.queue)
            if key != self.removed:
                self.length -= 1
                del self.data[key]
                return key
        raise ValueError("Cannot pop from empty queue")

    def len(self):
        return self.length
