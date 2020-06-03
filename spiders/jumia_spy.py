# -*- coding: utf-8 -*-
import scrapy


class JumiaSpySpider(scrapy.Spider):
    name = 'jumia_spy'
    page_number = 2
    start_urls = ['https://www.jumia.com.ng/android-phones/']

    def parse(self, response):
        product_url = response.css('.link::attr(href)').extract()
        brand = response.css('.brand ::text').extract()
        image_url = response.xpath('//img[contains(@class, "lazy image")]//@data-src').extract()
        title = response.xpath('//img[contains(@class, "lazy image")]//@alt').extract()
        price = response.xpath('//span[contains(@class, "price")]//span[contains(@dir,"ltr")]//text()').extract()

        zipped_data = zip(product_url,image_url,brand,title,price)

        for item in zipped_data:
            scraped_data = {
                'product_url': item[0],
                'image_url': item[1],
                'brand': item[2],
                'title': item[3],
                'price': item[4]
            }

            yield scraped_data

        next_page = 'https://www.jumia.com.ng/android-phones/?page=' + str(JumiaSpySpider.page_number)
        if JumiaSpySpider.page_number <= 50:
            JumiaSpySpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
