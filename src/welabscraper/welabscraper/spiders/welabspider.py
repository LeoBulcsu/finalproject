import scrapy


class WelabspiderSpider(scrapy.Spider):
    name = "welabspider"
    allowed_domains = ["welabplus.com"]
    start_urls = ["https://welabplus.com/product-category/camaras/arri/",
                  "https://welabplus.com/product-category/camaras/canon/",
                  "https://welabplus.com/product-category/camaras/red/",
                  "https://welabplus.com/product-category/camaras/sony/",
                  "https://welabplus.com/product-category/camaras/blackmagic/",
                  "https://welabplus.com/product-category/camaras/panasonic/",
                  "https://welabplus.com/product-category/camaras/phantom/",
                  "https://welabplus.com/product-category/camaras/gopro/",
                  "https://welabplus.com/product-category/camaras/sigma/",
                  "https://welabplus.com/product-category/camaras/kodak/",
                  "https://welabplus.com/product-category/camaras/otras/"]

    def parse(self, response):

        for cameras in response.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link'):

            try:

                yield {
                    'CATEGORY': 'CAMERAS',
                    'BRAND': cameras.css('h2.woocommerce-loop-product__title::text').get().split(' ')[0], 
                    'NAME': cameras.css('h2.woocommerce-loop-product__title::text').get(),
                    'PRICE a day': cameras.css('bdi::text').get().replace(',00\xa0', '').replace('.',''),
                    'RENTAL': 'WELAB',
                    'LINK': cameras.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                    }
            
            except:

                yield {
                    'CATEGORY': 'CAMERAS',
                    'BRAND': cameras.css('h2.woocommerce-loop-product__title::text').get().split(' ')[0], 
                    'NAME': cameras.css('h2.woocommerce-loop-product__title::text').get(),
                    'PRICE a day': 'Pedir presupuesto',
                    'RENTAL': 'WELAB',
                    'LINK': cameras.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                    }



class LensSpider(scrapy.Spider):
    name = "lensSpider"
    start_urls = ["https://welabplus.com/product-category/opticas/"]

    def parse(self, response):
        # Parse lens categories

        lens_categories_first = response.css('li.product-category.product.first')
        lens_categories = response.css('li.product-category.product')
        lens_categories_last = response.css('li.product-category.product.last')
        
        for category_1 in lens_categories_first:
            category_url = category_1.css('a').attrib['href']
            
            yield scrapy.Request(category_url, callback=self.parse_brands)
        
        for category_2 in lens_categories:
            category_url = category_2.css('a').attrib['href']
            
            yield scrapy.Request(category_url, callback=self.parse_brands)

        for category_3 in lens_categories_last:
            category_url = category_3.css('a').attrib['href']
            
            yield scrapy.Request(category_url, callback=self.parse_brands)

    def parse_brands(self, response):
        # Parse brands within categories
        
        lens_brands_first = response.css('li.product-category.product.first')
        lens_brands = response.css('li.product-category.product')
        lens_brands_last = response.css('li.product-category.product.last')
        
        for brand_1 in lens_brands_first:
            category_url = brand_1.css('a').attrib['href']
            
            yield scrapy.Request(category_url, callback=self.parse_brands)
        
        for brand_2 in lens_brands:
            category_url = brand_2.css('a').attrib['href']
            
            yield scrapy.Request(category_url, callback=self.parse_brands)

        for brand_3 in lens_brands_last:
            category_url = brand_3.css('a').attrib['href']
            
            yield scrapy.Request(category_url, callback=self.parse_brands)

    def parse_products(self, response):
        # Parse product information within brands
        products = response.css('a.woocommerce-LoopProduct-link woocommerce-loop-product__link')
        for product in products:
            # Extract product details and yield them or process as needed
            
            try:

                yield {
                        'CATEGORY': 'CAMERAS',
                        'BRAND': product.css('h2.woocommerce-loop-product__title::text').get().split(' ')[0], 
                        'NAME': product.css('h2.woocommerce-loop-product__title::text').get(),
                        'PRICE a day': product.css('bdi::text').get().replace(',00\xa0', '').replace('.',''),
                        'RENTAL': 'WELAB',
                        'LINK': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                        }
            
            except:

                yield {
                    'CATEGORY': 'CAMERAS',
                    'BRAND': product.css('h2.woocommerce-loop-product__title::text').get().split(' ')[0], 
                    'NAME': product.css('h2.woocommerce-loop-product__title::text').get(),
                    'PRICE a day': 'Pedir presupuesto',
                    'RENTAL': 'WELAB',
                    'LINK': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                    }

