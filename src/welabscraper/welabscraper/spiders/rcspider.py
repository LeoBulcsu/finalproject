import scrapy 

# RC SERVICE SCRAP

class RCLensSpider_1(scrapy.Spider):

    name = "rclensSpider_1"
    start_urls = ["https://www.rcservice.es/es/alquiler-opticas-cine-peliculas"]

    def parse(self, response):
        
        #Parse lens categories

        rclens_categories = response.css('div.uk-clearfix > p a::attr(href)').extract()
        
        for category_url in rclens_categories:
            yield scrapy.Request(category_url, callback=self.parse_brands)

    def parse_brands(self, response):
        # Parse brands within categories

        lens_brands = response.css('div.uk-clearfix > p a::attr(href)').extract()
        
        for brand_url in lens_brands:
            yield scrapy.Request(brand_url, callback=self.parse_products)

    def parse_products(self, response):
        # Parse product information within brands

        products = response.css('article.uk-article')

        for product in products:
            # Extract product details and yield them or process as needed

            yield {
                    'CATEGORY': 'LENSES',
                    'BRAND': response.css('base').attrib['href'].split('/')[-1],
                    'TYPE': response.css('base').attrib['href'].split('/')[-2], 
                    'NAME': product.css('h1.uk-article-title > a ::text').get(),
                    'PRICE a day': 'Pedir presupuesto',
                    'RENTAL': 'RC SERVICE',
                    'LINK': product.css('article.uk-article').attrib['data-permalink']
                    }





class RCLensSpider_2(scrapy.Spider):

    name = "rclensSpider_2"
    start_urls = ["https://www.rcservice.es/es/alquiler-opticas-cine-peliculas"]

    def parse(self, response):
        
        #Parse lens categories

        rclens_categories = response.css('div.uk-clearfix > p a::attr(href)').extract()
        
        for category_url in rclens_categories:
            yield scrapy.Request(category_url, callback=self.parse_products)

    # def parse_brands(self, response):
    #     # Parse brands within categories

    #     lens_brands = response.css('div.uk-clearfix > p a::attr(href)').extract()
        
    #     for brand_url in lens_brands:
    #         yield scrapy.Request(brand_url, callback=self.parse_products)

    def parse_products(self, response):
        # Parse product information within brands

        products = response.css('article.uk-article')

        for product in products:
            # Extract product details and yield them or process as needed

            yield {
                    'CATEGORY': 'LENSES',
                    'BRAND': product.css('h1.uk-article-title > a ::text').get().split(' ')[1],
                    'TYPE': response.css('base').attrib['href'].split('/')[-1], 
                    'NAME': product.css('h1.uk-article-title > a ::text').get(),
                    'PRICE a day': 'Pedir presupuesto',
                    'RENTAL': 'RC SERVICE',
                    'LINK': product.css('article.uk-article').attrib['data-permalink']
                    }
