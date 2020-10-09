import scrapy


class PropertySpider(scrapy.Spider):
    name = "xe.gr property scan"

    def __init__(self, starting_url='', **kwargs):
        self.start = starting_url
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.start, callback=self.parse)

    def parse(self, response):
        houses_urls_on_page = response.css('.articleLink::attr(href)').extract()
        for house_url in houses_urls_on_page:
            yield scrapy.Request(response.urljoin(house_url), callback=self.parse_house)
        # parse next page if exists
        if len(response.css('div.pager td > a::attr(title)').extract()) == 1:
            yield scrapy.Request(response.urljoin(response.css('div.pager td > a::attr(href)').extract()[-1]), callback=self.parse)

    def parse_house(self, response):
        home_info = {}
        home_info["type"] = response.css("div.info-title > h1::text").extract_first()
        home_info["region"], home_info["location"] = response.css("div.info-title > span::text").extract_first().strip().split(" - ")
        home_info["price"] = int(response.css(".price > h1::text").extract_first().strip().replace(' €', '').replace('.', ''))
        home_info["area"] = int(response.css(".area > h1::text").extract_first().strip().replace(' sq.m', ''))
        home_info["bedrooms"], home_info["baths"] = response.css('.baths > h1::text').extract()
        home_info["url"] = response.url
        ## Ading date
        yield home_info

        
