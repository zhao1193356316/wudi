import scrapy


class FristSpider(scrapy.Spider):
    name = "frist"
    allowed_domains = ["www.baidu.com"]
    start_urls = ["https://www.baidu.com"]

    def parse(self, response):
        print("运行结果：",response)
