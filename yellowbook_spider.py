import scrapy
from scrapy.crawler import CrawlerProcess
from random import randrange

URL = "https://www.yellowbook.com/s/restaurants/henderson-nv/?page="
pages = 30

class Playbook(scrapy.Spider):
    name = "PostcodesSpider"

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'Data.csv',
        'CONCURRENT_REQUESTS': '1',
        # 'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def start_requests(self):
        for i in range(15, pages):
            yield scrapy.Request(url=URL + str(i),
                             callback=self.parse, dont_filter=True,
                             headers={
                                 'USER-AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                               "like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                             },
                             )

    def parse(self, response):
        cards = response.css("ol.c > li")
        for card in cards:
            name = card.css("h2 > a::text").extract_first()
            phone = card.css("div.phone-number::text").extract_first()
            address = card.css("div.address > div::text").extract()
            address = ". ".join(address)
            website = card.css("ul.l > li > a::attr(href)").extract_first()
            if not website:
                website = "N/A"

            yield {
                "Name": name.strip(),
                "Phone": phone.strip(),
                "Website": website.strip(),
                "Address": address.strip(),
            }


process = CrawlerProcess()
process.crawl(Playbook)
process.start()
