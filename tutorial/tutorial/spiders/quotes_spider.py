import scrapy
class QuotesSpider(scrapy.Spider): # spider subclass
    name = "quotes"
    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        # Using spider arguments
        # You can use this to make your spider fetch only quotes with a specific tag, building the URL based on the argument
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author': quote.css('span.text::text').get(),
                'text': quote.css('span.text::text').get()
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
# Run command: scrapy crawl quotes -O quotes-humor.json -a tag=humor