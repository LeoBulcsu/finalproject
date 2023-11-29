import scrapy 

# RC SERVICE SCRAP

class RCLensSpider(scrapy.Spider):

    name = "rclensSpider"
    start_urls = ["https://www.rcservice.es/es/alquiler-opticas-cine-peliculas"]

    def parse(self, response):
        # Parse lens categories

        rclens_categories = response.css('div.uk-clearfix > p a::attr(href)').extract()
        
        for i in range(len(rclens_categories)):

            category_url = rclens_categories[i]
            
            yield scrapy.Request(category_url, callback=self.parse_brands)

    def parse_brands(self, response):
        # Parse brands within categories
        
        lens_brands = response.css('div.uk-clearfix > p a::attr(href)').extract()
        
        for i in range(len(lens_brands)):
            
            category_url = lens_brands[i]
            
            yield scrapy.Request(category_url, callback=self.parse_products)


    def parse_products(self, response):
        # Parse product information within brands

        products = response.css('article.uk-article')

        for product in products:
            # Extract product details and yield them or process as needed
            
            yield {
                    'CATEGORY': 'LENSES',
                    'BRAND': product.css('base').attrib['href'].split('/')[-1],
                    'TYPE': product.css('base').attrib['href'].split('/')[-2], 
                    'NAME': product.css('h1.uk-article-title::text').get(),
                    'PRICE a day': 'Pedir presupuesto',
                    'RENTAL': 'RC SERVICE',
                    'LINK': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                    }