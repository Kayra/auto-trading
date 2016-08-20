import scrapy


class AutoTraderSpider(scrapy.Spider):

    name = 'auto-trader'
    start_urls = ['http://www2.autotrader.co.uk/search/used/cars/postcode/se233sx/radius/1500/price-from/1000/page/1/searchcontext/default/sort/default/onesearchad/new%2Cnearlynew%2Cused']

    def parse(self, response):
        for page in range(99):
            url_list = response.url.split('/')
            page_number_index = url_list.index('page') + 1
            next_page_number = page + 1
            url_list[page_number_index] = str(next_page_number)
            next_page_url = '/'.join(url_list)
            yield scrapy.Request(next_page_url, callback=self.parse_page)

    def parse_page(self, response):

        titles = response.xpath('//article/div/div[2]/div[1]/h1/a/text()').extract()
        stats = response.xpath('//article/div/div[2]/ul')
        prices = response.xpath('//article/div/div[2]/div[1]/div/text()').extract()
        links = response.xpath('//article/div/div[2]/div[1]/h1/a/@href').extract()

        for title, stat, price, link in zip(titles, stats, prices, links):
            yield {'car': (title, stat.xpath('li/text()').extract(), price, link)}
