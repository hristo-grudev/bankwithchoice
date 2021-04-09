import scrapy

from scrapy.loader import ItemLoader

from ..items import BankwithchoiceItem
from itemloaders.processors import TakeFirst
base = 'https://bankwithchoice.com/blog/page/{}/'


class BankwithchoiceSpider(scrapy.Spider):
	name = 'bankwithchoice'
	page = 1
	start_urls = [base.format(page)]

	def parse(self, response):
		post_links = response.xpath('//header[@class="entry-header"]/h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		if post_links:
			self.page += 1
			yield response.follow(base.format(self.page), self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="posted-on"]/time[@class="entry-date published"]/text()').get()

		item = ItemLoader(item=BankwithchoiceItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
