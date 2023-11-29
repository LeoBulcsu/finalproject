import scrapy


class OvideSpider(scrapy.Spider):

    name = 'ovidecameraSpider'
    start_urls = ['https://www.ovide.com/alquiler/cine/camaras/']

    def parse(self, response):

        cameras = response.css('')

        for camera in cameras:

            yield {
                'CATEGORY': 'CAMERAS',
                'TYPE': 'Cine -Digital',
                'BRAND': cameras.css('div.basel-product-brands-links > a ::text').get(), 
                'NAME': cameras.css('h3.product-title > a ::text').get(),
                'PRICE a day': 'Pedir presupuesto',
                'RENTAL': 'OVIDE',
                'LINK': cameras.css('h3.product-title > a').attrib['href'] 
                }