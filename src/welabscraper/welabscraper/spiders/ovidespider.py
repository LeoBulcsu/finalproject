import scrapy


class OvideSpider(scrapy.Spider):

    name = 'ovidecameraSpider'
    start_urls = ['https://www.ovide.com/alquiler/cine/camaras/']

    def parse(self, response):

        for camera in response.css('div.product-grid-item'):

            yield {
                'CATEGORY': 'CAMERAS',
                'TYPE': 'Cine Digital',
                'BRAND': camera.css('div.basel-product-brands-links > a ::text').get(), 
                'NAME': camera.css('h3.product-title > a ::text').get(),
                'PRICE a day': 'Pedir presupuesto',
                'RENTAL': 'OVIDE',
                'LINK': camera.css('h3.product-title > a').attrib['href'] 
                }


class OvideSpider_2(scrapy.Spider):

    name = 'ovidevideocameraSpider'
    start_urls = ['https://www.ovide.com/alquiler/video/video-camaras/']

    def parse(self, response):

        for camera in response.css('div.product-grid-item'):

            yield {
                'CATEGORY': 'CAMERAS',
                'TYPE': 'Video Digital',
                'BRAND': camera.css('div.basel-product-brands-links > a ::text').get(), 
                'NAME': camera.css('h3.product-title > a ::text').get(),
                'PRICE a day': 'Pedir presupuesto',
                'RENTAL': 'OVIDE',
                'LINK': camera.css('h3.product-title > a').attrib['href'] 
                }



class OvideSpider_3(scrapy.Spider):

    name = 'ovidelensSpider'
    start_urls = ['https://www.ovide.com/alquiler/cine/objetivos/']

    def parse(self, response):

        for lens in response.css('div.product-grid-item'):

            yield {
                'CATEGORY': 'LENSES',
                'BRAND': lens.css('div.basel-product-brands-links > a ::text').get(), 
                'TYPE': 'CINE PL MOUNT',
                'NAME': lens.css('h3.product-title > a ::text').get(),
                'PRICE a day': 'Pedir presupuesto',
                'RENTAL': 'OVIDE',
                'LINK': lens.css('h3.product-title > a').attrib['href'] 
                }
        
        next_page = response.css('a.next.page-numbers').attrib['href']
        if next_page is not None:

            yield response.follow(next_page, callback = self.parse)



class OvideSpider_4(scrapy.Spider):

    name = 'ovidevideolensSpider'
    start_urls = ['https://www.ovide.com/alquiler/video/objetivos-video/']

    def parse(self, response):

        for lens in response.css('div.product-grid-item'):

            yield {
                'CATEGORY': 'LENSES',
                'BRAND': lens.css('div.basel-product-brands-links > a ::text').get(), 
                'TYPE': 'VIDEO MOUNT E-EF-PL',
                'NAME': lens.css('h3.product-title > a ::text').get(),
                'PRICE a day': 'Pedir presupuesto',
                'RENTAL': 'OVIDE',
                'LINK': lens.css('h3.product-title > a').attrib['href'] 
                }
        
        next_page = response.css('a.next.page-numbers').attrib['href']
        if next_page is not None:

            yield response.follow(next_page, callback = self.parse)

    

class OvideSpider_5(scrapy.Spider):

    name = 'ovideaudiolensSpider'
    start_urls = ['https://www.ovide.com/alquiler/audio/']

    def parse(self, response):

        for category in response.css('div.category-content'):

            category_url = category.css('a').attrib['href']

            yield scrapy.Request(category_url, callback=self.parse_products)

    
    def parse_products(self, response):
        # Parse product information within brands

        products = response.css('div.product-grid-item')

        for product in products:

            yield {
                'CATEGORY': 'Audio',
                'BRAND': product.css('div.basel-product-brands-links > a ::text').get(), 
                'TYPE': response.css('h1.entry-title::text').get(),
                'NAME': product.css('h3.product-title > a ::text').get(),
                'PRICE a day': 'Pedir presupuesto',
                'RENTAL': 'OVIDE',
                'LINK': product.css('h3.product-title > a').attrib['href'] 
                }
        
        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page is not None:

            yield response.follow(next_page, callback = self.parse_products)



class OvideSpider_6(scrapy.Spider):

    name = 'ovidelightSpider'
    start_urls = ['https://www.ovide.com/alquiler/video/iluminacion/']

    def parse(self, response):

        for product in response.css('div.product-grid-item'):

            yield {
                'CATEGORY': 'ILUMINACION',
                'Subcategory': product.css('h3.product-title > a ::text').get().split(' ')[0],
                'BRAND': product.css('div.basel-product-brands-links > a ::text').get(), 
                'TYPE': 'ACCESORIOS',
                'NAME': product.css('h3.product-title > a ::text').get(),
                'PRICE a day': 'Pedir presupuesto',
                'RENTAL': 'OVIDE',
                'LINK': product.css('h3.product-title > a').attrib['href'] 
                }
        
        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page is not None:

            yield response.follow(next_page, callback = self.parse)