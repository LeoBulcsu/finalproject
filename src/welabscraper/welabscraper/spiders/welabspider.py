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

        lens_categories = response.css('li.product-category.product')
        
        for category in lens_categories:

            category_url = category.css('a').attrib['href']
            
            yield scrapy.Request(category_url, callback=self.parse_brands)

    def parse_brands(self, response):
        # Parse brands within categories
        
        lens_brands = response.css('li.product-category.product')
        
        for brand in lens_brands:
            category_url = brand.css('a').attrib['href']
            
            yield scrapy.Request(category_url, callback=self.parse_products)


    def parse_products(self, response):
        # Parse product information within brands

        products = response.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link')

        for product in products:
            # Extract product details and yield them or process as needed
            
            try:

                yield {
                        'CATEGORY': 'LENSES',
                        'BRAND': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-2].split('-')[0],
                        'TYPE': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-3], 
                        'NAME': product.css('h2.woocommerce-loop-product__title::text').get(),
                        'PRICE a day': product.css('bdi::text').get().replace(',00\xa0', '').replace('.',''),
                        'RENTAL': 'WELAB',
                        'LINK': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                        }
            
            except:

                yield {
                        'CATEGORY': 'LENSES',
                        'BRAND': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-2].split('-')[0],
                        'TYPE': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-3],
                        'NAME': product.css('h2.woocommerce-loop-product__title::text').get(),
                        'PRICE a day': 'Pedir presupuesto',
                        'RENTAL': 'WELAB',
                        'LINK': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                        }





class AudioSpider(scrapy.Spider):
    name = "audioSpider"
    start_urls = ["https://welabplus.com/product-category/audio/"]

    def parse(self, response):
        # Parse lens categories

        audio_categories = response.css('li.product-category.product')
        
        for category in audio_categories:

            category_url = category.css('a').attrib['href']
            
            yield scrapy.Request(category_url, callback=self.parse_products)

    # def parse_brands(self, response):
    #     # Parse brands within categories
        
    #     lens_brands = response.css('li.product-category.product')
        
    #     for brand in lens_brands:
    #         category_url = brand.css('a').attrib['href']
            
    #         yield scrapy.Request(category_url, callback=self.parse_products)


    def parse_products(self, response):
        # Parse product information within brands

        products = response.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link')

        for product in products:
            # Extract product details and yield them or process as needed
            
            try:

                yield {
                        'CATEGORY': 'AUDIO',
                        'BRAND': product.css('h2.woocommerce-loop-product__title::text').get().split(' ')[0],
                        'TYPE': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-3], 
                        'NAME': product.css('h2.woocommerce-loop-product__title::text').get(),
                        'PRICE a day': product.css('bdi::text').get().replace(',00\xa0', '').replace('.',''),
                        'RENTAL': 'WELAB',
                        'LINK': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                        }
            
            except:

                yield {
                        'CATEGORY': 'LENSES',
                        'BRAND': product.css('h2.woocommerce-loop-product__title::text').get().split(' ')[0],
                        'TYPE': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-3],
                        'NAME': product.css('h2.woocommerce-loop-product__title::text').get(),
                        'PRICE a day': 'Pedir presupuesto',
                        'RENTAL': 'WELAB',
                        'LINK': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                        }





class LightSpider(scrapy.Spider):
    name = "lightSpider_1"
    start_urls = ["https://welabplus.com/product-category/iluminacion/"]

    def parse(self, response):
        # Parse lens categories

        light_categories = response.css('li.product-category.product')
        
        for category in light_categories:

            category_url = category.css('a').attrib['href']
                
            yield scrapy.Request(category_url, callback=self.parse_brands)



    def parse_brands(self, response):
        # Parse brands within categories
        
        lens_brands = response.css('li.product-category.product')
        
        for brand in lens_brands:
            category_url = brand.css('a').attrib['href']
            
            yield scrapy.Request(category_url, callback=self.parse_products)


    def parse_products(self, response):
        # Parse product information within brands

        products = response.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link')

        for product in products:
            # Extract product details and yield them or process as needed
            
            try:

                yield {
                        'CATEGORY': 'LIGHTING',
                        'SubCatgory': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-2].split('-')[0],
                        'TYPE': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-3], 
                        'NAME': product.css('h2.woocommerce-loop-product__title::text').get(),
                        'PRICE a day': product.css('bdi::text').get().replace(',00\xa0', '').replace('.',''),
                        'RENTAL': 'WELAB',
                        'LINK': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                        }
            
            except:

                yield {
                        'CATEGORY': 'LENSES',
                        'SubCatgory': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-2].split('-')[0],
                        'TYPE': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-3],
                        'NAME': product.css('h2.woocommerce-loop-product__title::text').get(),
                        'PRICE a day': 'Pedir presupuesto',
                        'RENTAL': 'WELAB',
                        'LINK': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                        }
                



    name = "lightSpider_2"
    start_urls = ["https://welabplus.com/product-category/iluminacion/"]

    def parse(self, response):
        # Parse lens categories

        light_categories = response.css('li.product-category.product')
        
        for category in light_categories:

            category_url = category.css('a').attrib['href']
                
            yield scrapy.Request(category_url, callback=self.parse_products)



    # def parse_brands(self, response):
    #     # Parse brands within categories
        
    #     lens_brands = response.css('li.product-category.product')
        
    #     for brand in lens_brands:
    #         category_url = brand.css('a').attrib['href']
            
    #         yield scrapy.Request(category_url, callback=self.parse_products)


    def parse_products(self, response):
        # Parse product information within brands

        products = response.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link')

        for product in products:
            # Extract product details and yield them or process as needed
            
            try:

                yield {
                        'CATEGORY': 'LIGHTING',
                        'SubCatgory': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-2].split('-')[0],
                        'TYPE': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-3], 
                        'NAME': product.css('h2.woocommerce-loop-product__title::text').get(),
                        'PRICE a day': product.css('bdi::text').get().replace(',00\xa0', '').replace('.',''),
                        'RENTAL': 'WELAB',
                        'LINK': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                        }
            
            except:

                yield {
                        'CATEGORY': 'LENSES',
                        'SubCatgory': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-2].split('-')[0],
                        'TYPE': product.xpath("/html/head/link[6]").attrib['href'].split('/')[-3],
                        'NAME': product.css('h2.woocommerce-loop-product__title::text').get(),
                        'PRICE a day': 'Pedir presupuesto',
                        'RENTAL': 'WELAB',
                        'LINK': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
                        }