import scrapy
from scrapy.loader import ItemLoader
from irasutoya.items import IrasutoyaItem

class IrasutoCategorySpider(scrapy.Spider):
    name = 'irasuto_category'
    allowed_domains = ['www.irasutoya.com']
    #カテゴリーごとのURLを指定
    start_urls = [
        'https://www.irasutoya.com/search/label/%E6%98%A0%E7%94%BB',
        'https://www.irasutoya.com/search/label/%E9%9F%B3%E6%A5%BD'
        ]


    def parse(self, response):
        page_urls = response.xpath('//div[@class="boxmeta clearfix"]/h2/a')
        IrasutoyaItem.directory_name = response.xpath('//div[@class="labelbox"]/h2/text()').get()

        for page_url in page_urls :
            if page_url.xpath('./text()').get() == 'プライバシーポリシー' :
                break

            yield response.follow(url=page_url.xpath('./@href').get(), callback=self.parse_img)

            next_page = response.xpath('//span[@id="blog-pager-older-link"]/a')
            if next_page:
                yield response.follow(url=next_page[0], callback=self.parse)


    def parse_img(self, response):
        img_block = response.xpath('//div[@class="entry"]/div[@class="separator"]/a')

        for i, img in enumerate(img_block):
            loader = ItemLoader(item=IrasutoyaItem(), response=response)
            IrasutoyaItem.page_title = response.xpath('//div[@class="title"]/h2/text()').get()

            if img.xpath('./img/@alt').get() == "■":
                image_title = (IrasutoyaItem.page_title + '(' + str(i+1) + ')').replace('\n', '')
            else:
                image_title = img.xpath('./img/@alt').get()

            loader.add_value('image_titles', image_title),
            loader.add_value('image_urls', [response.urljoin(img.xpath('./@href').get())]),
            loader.add_value('directory_name', IrasutoyaItem.directory_name),
            loader.add_value('page_title', IrasutoyaItem.page_title)

            yield loader.load_item()
