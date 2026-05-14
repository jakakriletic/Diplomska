import scrapy


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["fei.uni-nm.si"]
    start_urls = ["https://fei.uni-nm.si/"]

    def parse(self, response):
        yield {
            "url": response.url,
            "depth": 0,
            "html": response.text,
            
        }
        links = response.xpath("//a/@href").getall()

        for link in links:
            full_url = response.urljoin(link)
            yield scrapy.Request(full_url, callback=self.parse_detail, meta={"depth_level": 1})

    def parse_detail(self, response):
            depth = response.meta.get("depth_level", 0)
            yield {
                "url": response.url,
                "depth": depth,
                "html": response.text,
            }
            
            if depth < 2:
                 links = response.xpath("//a/@href").getall()
                 for link in links:
                      full_url = response.urljoin(link)
                      yield scrapy.Request(full_url, callback=self.parse_detail, meta={"depth_level": depth + 1})
            