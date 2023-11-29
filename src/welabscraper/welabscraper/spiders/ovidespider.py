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



class OvideSpider(scrapy.Spider):

    name = 'ovidelensSpider'
    start_urls = ['https://www.ovide.com/alquiler/cine/objetivos/']

    def parse(self, response):

        for lens in response.css('div.product-grid-item'):

            yield {
                'CATEGORY': 'CAMERAS',
                'TYPE': 'Cine Digital',
                'BRAND': lens.css('div.basel-product-brands-links > a ::text').get(), 
                'NAME': lens.css('h3.product-title > a ::text').get(),
                'PRICE a day': 'Pedir presupuesto',
                'RENTAL': 'OVIDE',
                'LINK': lens.css('h3.product-title > a').attrib['href'] 
                }

