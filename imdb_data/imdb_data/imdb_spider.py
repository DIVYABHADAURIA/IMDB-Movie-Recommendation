import scrapy
from items import ImdbDataItem
from scrapy.crawler import CrawlerProcess


class ImdbSpiderSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top']

    custom_settings = { 'FEED_FORMAT':'csv', 'FEED_URL':'IMDB.csv'}

    def parse(self, response):
        for href in response.css("td.titleColumn a::attr(href)").getall():
            yield scrapy.Request(response.urljoin(href),callback=self.parse_movie)

    def parse_movie(self, response):
        item = ImdbDataItem()
        item['title'] = [x.replace('\xa0','') for x in response.css(".title_wrapper h1::text").getall()][0]
        item['directors'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Director:")]/following-sibling::a/text()').getall()
        item['writers'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Writers:")]/following-sibling::a/text()').getall()
        item['stars'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(.,  "Stars")]/following-sibling::a/text()').getall()
        item['popularity'] = response.css(".titleReviewBarSubItem span.subText::text")[2].re('([0-9]+)')
        item['rating'] = response.css(".ratingValue span::text").get()


        return item

            


process = CrawlerProcess()
process.crawl(ImdbSpiderSpider)
process.start()
