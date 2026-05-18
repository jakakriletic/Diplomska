import scrapy
from urllib.parse import urlparse


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    
    blocked_domains = [
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "youtube.com",
    "google.com",
    "x.com",
    "twitter.com",
    ]
    blocked_extensions = [
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg",
    ".zip", ".rar", ".doc", ".docx", ".xls", ".xlsx",
    ]
    def parse(self, response):
        yield {
            "url": response.url,
            "depth": 0,
            "html": response.text,
            
        }
        links = response.xpath("//a/@href").getall()

        for link in links:
            full_url = response.urljoin(link)
            if self.blacklist(full_url):
                continue
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
                      if self.blacklist(full_url):
                          continue
                      yield scrapy.Request(full_url, callback=self.parse_detail, meta={"depth_level": depth + 1})
                      
    def blacklist(self, url):
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        
        if parsed.scheme not in ["http", "https"]:
            return True
        if path.endswith(tuple(self.blocked_extensions)):
            return True 
        for blocked in self.blocked_domains:
            if domain == blocked or domain.endswith("." + blocked):
                return True

        return False
            