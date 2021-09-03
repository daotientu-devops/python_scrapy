import scrapy
class QuotesSpider(scrapy.Spider): # spider subclass
    # Define some attributes and methods
    name = 'quotes' # identifies the spider. It must be unique within a project. You can't set the same name for different spiders
    # This list will then be used by the default implementation of start_requests() to create the initial requests for your spider
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]
    def parse(self, response): # parse(): a method that will be called to handle the response downloaded for each of the requests made
        # The response parameter is an instance of TextResponse that holds the page content and has further helpful methods to handle it
        # The parse() method usually parses the responsem extracting the scraped data as dicts and aslo finding new URLs to follow and creating new requests (Request) from them
        for quote in  response.css('div.quote'):
            # Spider typically generates many dictionaries containing the data extracted from the page. To do that, we use the yield keyword in the callback
            yield {
                'text': quote.css("span.text::text").get(),
                'author': quote.css("small.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall(),
            }
        # A shortcut for creating Requests
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # Unlike scrapy.Request, response.follow supports relative URLs directly - no need to call urljoin
            yield response.follow(next_page, callback=self.parse)
        # Pass a selector to response.follow instead of a string, this selector should extract necessary attributes
        for href in response.css('ul.pager a::attr(href)'):
            yield response.follow(href, callback=self.parse)
        # For <a> elements there is a shortcut: response.follow uses their href attributes automatically. So the code can be shortened further
        for href in response.css('ul.pager a'):
            yield response.follow(a, callback=self.parse)
        # To create multiple requests from an iterable, you can use response.follow_all instead
        anchors = response.css('ul.pager a')
        yield from response.follow_all(anchors, callback=self.parse)
        # Or shortening it further
        yield from response.follow_all(css='ul.pager a', callback=self.parse)