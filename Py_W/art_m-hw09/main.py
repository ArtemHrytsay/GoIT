import json, scrapy, connect

from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field


class QuoteItem(Item):
    tags   = Field()
    author = Field()
    quote  = Field()

class AuthorItem(Item):
    fullname      = Field()
    date_born     = Field()
    location_born = Field()
    bio           = Field()

class QuotesPipline:
    quotes  = list()
    authors = list()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            self.authors.append({
                "fullname"     : adapter["fullname"],
                "date_born"    : adapter["date_born"],
                "location_born": adapter["location_born"],
                "bio"          : adapter["bio"],
            })
        if 'quote' in adapter.keys():
            self.quotes.append({
                "tags":   adapter["tags"],
                "author": adapter["author"],
                "quote":  adapter["quote"],
            })
        return

    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as file:
            json.dump(self.quotes, file, ensure_ascii=False)
        with open('authors.json', 'w', encoding='utf-8') as file:
            json.dump(self.authors, file, ensure_ascii=False)


class QuotesSpider(scrapy.Spider):
    name            = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls      = ['http://quotes.toscrape.com/']
    custom_settings = {"ITEM_PIPELINES": {QuotesPipline: 300}}

    def parse(self, response, *args):
        for quote in response.xpath("/html//div[@class='quote']"):
            tags   = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("span/small/text()").get().strip()
            q      = quote.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(tags=tags, author=author, quote=q)
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get(),
                                  callback=self.nested_parse_author)
        next_link  = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse_author(self, response, *args):
        author        = response.xpath('/html//div[@class="author-details"]')
        fullname      = author.xpath('h3[@class="author-title"]/text()').get().strip()
        date_born     = author.xpath('p/span[@class="author-born-date"]/text()').get().strip()
        location_born = author.xpath('p/span[@class="author-born-location"]/text()').get().strip()
        bio = author.xpath('div[@class="author-description"]/text()').get().strip()
        yield AuthorItem(fullname=fullname, date_born=date_born, location_born=location_born, bio=bio)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
