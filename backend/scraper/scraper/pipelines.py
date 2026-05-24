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
        
        
        


        
        
        
        
        
        
        '''
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        lowercase_keys = ["category", "product_type"]
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        price_keys = ["price", "price_excl_tax", "price_incl_tax", "tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace("£", "")
            adapter[price_key] = float(value)

        availability_string = adapter.get("availability")
        split_string_array = availability_string.split("(")
        if len(split_string_array) < 2:
            adapter["availability"] = 0
        else:
            availability_array = split_string_array[1].split(" ")
            adapter["availability"] = int(availability_array[0])
            
        num_reviews_string = adapter.get("num_reviews")
        adapter["num_reviews"] = int(num_reviews_string)

        stars_string = adapter.get("stars")
        split_stars_array = stars_string.split(" ")
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter["stars"] = 0
        elif stars_text_value == "one":
            adapter["stars"] = 1
        elif stars_text_value == "two":
            adapter["stars"] = 2
        elif stars_text_value == "three":
            adapter["stars"] = 3
        elif stars_text_value == "four":
            adapter["stars"] = 4
        elif stars_text_value == "five":
            adapter["stars"] = 5
            
        return item
'''