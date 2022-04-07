import scrapy
from scrapy.loader import ItemLoader
from irasutoya.items import IrasutoyaItem
from scrapy_selenium import SeleniumRequest
from time import sleep
from selenium.webdriver.common.keys import Keys

class IrasutoSearchSpider(scrapy.Spider):
    name = 'irasuto_search'

    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://www.irasutoya.com',
            wait_time = 3,
            callback = self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        search_bar = driver.find_element_by_xpath('//input[@placeholder="イラストを検索"]')

        search_word = 'プログラミング' #検索ワード

        search_bar.send_keys(search_word)
        search_bar.send_keys(Keys.ENTER)
        sleep(2)
        IrasutoyaItem.directory_name = search_word

        yield SeleniumRequest(
            url=driver.current_url,
            wait_time = 3,
            callback = self.parse_list
            )


    def parse_list(self, response):
        page_urls = response.xpath('//div[@class="boxmeta clearfix"]/h2/a')

        for page_url in page_urls :
            if page_url.xpath('./text()').get() == 'プライバシーポリシー' :
                break

            yield response.follow(url=page_url.xpath('./@href').get(), callback=self.parse_img)

            next_page = response.xpath('//span[@id="blog-pager-older-link"]/a')
            if next_page:
                yield response.follow(url=next_page[0], callback=self.parse_list)


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
