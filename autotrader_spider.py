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

        for title, car_stats, price, link in zip(titles, stats, prices, links):
            car_stats = car_stats.xpath('li/text()').extract()

            stats_dict = dict()
            stats_dict['year'] = car_stats[0]
            stats_dict['style'] = car_stats[1]
            stats_dict['milage'] = car_stats[2]
            stats_dict['transmission'] = car_stats[3]
            stats_dict['size'] = car_stats[4]
            stats_dict['fuel'] = car_stats[5]

            stats_dict = self.format_stats(stats_dict)

            price = price.replace('£', '').replace(',', '')
            yield {'car': (title, stats_dict, price, link)}

    def format_stats(self, stats_dict):

        stats_dict['year'] = int(stats_dict['year'][:4])
        stats_dict['milage'] = int(stats_dict['milage'].replace('miles', '').replace(',', '').strip())

        return stats_dict
