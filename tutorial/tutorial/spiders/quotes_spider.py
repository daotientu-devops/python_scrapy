import scrapy
class QuotesSpider(scrapy.Spider): # spider subclass
    # Define some attributes and methods
    name = 'quotes' # identifies the spider. It must be unique within a project. You can't set the same name for different spiders
    def start_requests(self): # start_requests(): must return an iterable of Requests (you can return a list of requests or write a generator function) which the spider will begin to crawl from
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response): # parse(): a method that will be called to handle the response downloaded for each of the requests made
        # The response parameter is an instance of TextResponse that holds the page content and has further helpful methods to handle it
        # The parse() method usually parses the responsem extracting the scraped data as dicts and aslo finding new URLs to follow and creating new requests (Request) from them
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')