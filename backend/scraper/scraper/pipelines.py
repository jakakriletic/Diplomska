# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from bs4 import BeautifulSoup

class ScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        html = adapter.get("html")
        
        element_key_words = [
    "cookie", "cookies", "cookienotice", "cookie-notice", "cookieconsent", "cookie-consent", "cookiebanner", "cookie-banner", "cookiebar", "cookie-bar",
    "piškot", "piškotek", "piškotki", "piskot", "piskotek", "piskotki", "gdpr", "consent", "copyright", "piškotki", 
    "search", "search-form", "searchbox", "search-box", "iskanje", "login", "signin", "sign-in", "register", "registration",
    "prijava", "registracija", "newsletter", "subscribe", "subscription", "social", "socials", "social-links", "share", "sharing",
    "facebook", "instagram", "linkedin", "twitter", "youtube", "tiktok", "tracking", "analytics", "gtm", "google-analytics",
    "googletagmanager", "fb-pixel", "pixel", "modal", "popup", "pop-up", "overlay"
]

        if isinstance(html, str):
            soup = BeautifulSoup(html, "html.parser")
            for element_type in soup(['style', 'script', 'noscript', 'svg', 'iframe', 'nav', 'header', 'footer', 'aside', 'form']):
                element_type.decompose()

            array_to_delete = []
            for element in soup.find_all(True):
                element_id = element.get("id", "")
                element_class = " ".join(element.get("class", []))

                joined = f"{element_id} {element_class}".lower()

                if any(find in joined for find in element_key_words):
                    array_to_delete.append(element)

            for element in array_to_delete:
                element.decompose()

            adapter["html"] = ' '.join(soup.stripped_strings)

        return item