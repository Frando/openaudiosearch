import aiohttp
import asyncio
import feedparser
import json


class FeedManager:

    def __init__(self):
        self.store = {}

    def add_feed(self, feed_url):
        feed = self.store.get(feed_url)
        if not feed:
            feed = RSSImport(feed_url)
            self.store[feed_url] = feed
        return feed

    def get_feed(self, feed_url):
        return self.store.get(feed_url)


class RSSImport:
    def __init__(self, url):
        self.url = url
        self.mapping = None
        self.feed = None
        self.keys = None
        self.items = None


    async def pull_feed(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                raw_feed = await response.text()
                self.feed = feedparser.parse(raw_feed)
                self.keys = list(self.feed.entries[0].keys())
                self.items = self.feed.entries

    def get_keys(self):
        if self.keys:
            return self.keys
        else:
            # here should no error happen
            raise Exception("no keys")

    def map_fields(self, mapping):
        for entry in self.feed.entries:
            {
                "headline": entry[json.loads(mapping)["headline"]],
            }
            print()
