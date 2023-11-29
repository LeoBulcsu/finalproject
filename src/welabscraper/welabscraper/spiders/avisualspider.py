import scrapy 

# AVISUAL SCRAP

class avisualSpider(scrapy.Spider):

    name = "avisualcameraSpider"
    start_urls = ["(https://www.avisualpro.es/categoria-producto/camaras/?location=madrid)"]

    def parse(self, response):
        
        #Parse products

        avisual_products = response.css('ul.children a::attr(href)').getall()
        
        for i in avisual_products:

            category_url = avisual_products[i]

            yield scrapy.Request(category_url, callback=self.parse_products)
            
    def parse_products(self, response):
        # Parse product information within brands

        products = response.css('a.woocommerce-loop-product__link')

        for product in products:
            # Extract product details and yield them or process as needed

            yield {
                    'CATEGORY': response.split('/')[4],
                    'BRAND': response.css('base').attrib['href'].split('/')[-1],
                    'TYPE': response.css('base').attrib['href'].split('/')[-2], 
                    'NAME': product.css('h1.uk-article-title > a ::text').get(),
                    'PRICE a day': 'Pedir presupuesto',
                    'RENTAL': 'RC SERVICE',
                    'LINK': product.css('article.uk-article').attrib['data-permalink']
                    }

