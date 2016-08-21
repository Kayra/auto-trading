import scrapy
from utils import stats_list_to_dict, format_stats, increase_url_page_number


class AutoTraderSpider(scrapy.Spider):

    name = 'auto-trader'
    start_urls = ['http://www2.autotrader.co.uk/search/used/cars/postcode/se233sx/radius/1500/price-from/1000/page/1/searchcontext/default/sort/default/onesearchad/new%2Cnearlynew%2Cused']

    def parse(self, response):
        for page in range(99):
            next_page_url = increase_url_page_number(response.url, page)
            yield scrapy.Request(next_page_url, callback=self.parse_page)

    def parse_page(self, response):

        titles = response.xpath('//article/div/div[2]/div[1]/h1/a/text()').extract()
        stats = response.xpath('//article/div/div[2]/ul')
        prices = response.xpath('//article/div/div[2]/div[1]/div/text()').extract()
        links = response.xpath('//article/div/div[2]/div[1]/h1/a/@href').extract()

        for title, car_stats, price, link in zip(titles, stats, prices, links):

            car_stats = car_stats.xpath('li/text()').extract()

            try:
                stats_dict = stats_list_to_dict(car_stats)
            except IndexError:
                break

            try:
                stats_dict = format_stats(stats_dict)
            except ValueError:
                break

            stats_dict['price'] = price.replace('£', '').replace(',', '')
            stats_dict['title'] = title
            stats_dict['link'] = link

            yield stats_dict
