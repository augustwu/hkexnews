#coding=utf-8

import scrapy
from datetime import datetime
from hkexnews.items import HkexnewsItem 
from scrapy.selector import HtmlXPathSelector


class HkSpider(scrapy.Spider):

  name ="hkspider"

  start_urls = ["http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/mutualmarketsdw/main_c.htm"]


#  def start_requests(self):
#    urls = ["http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh",
#      "http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz"]
#  
# #   for url in urls:
# #       yield scrapy.Request(url=url, callback=self.parse)
# #   return [scrapy.Request(i.strip(), callback=self.parse) for i in urls]
#    yield self.make_requests_from_url("http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/mutualmarketsdw/main_c.htm")
#

  def parse(self, response):
    urls = response.xpath('//p[@class="MsoListParagraph"]//a/text()').extract()
    print urls
    for url in urls:
      print url
      yield Request(url, callback=self.parse_url)



  def parse_url(self,response):
    date_str = response.css("div#pnlResult div::text").extract_first()
    date_str = date_str.split(":")[1].strip() 
    datetime_object = datetime.strptime(date_str, '%d/%m/%Y')
    print datetime_object  

    item_data = response.xpath('//*[@id="pnlResult"]/table//tr')
    for item in item_data[2:3]:
      code = item.xpath('td[1]/text()').extract_first().strip()
      name = item.xpath('td[2]/text()').extract_first().strip()
      mount = item.xpath('td[3]/text()').extract_first().strip()
      percent = item.xpath('td[4]/text()').extract_first().strip()

      instance  = HkexnewsItem()
      instance['name'] = name
      instance['code'] = code
      instance['mount'] = mount
      instance['percent'] = percent
      

      if code.startswith('7'):
        instance['market'] = 'sz'
      else:
        instance['market'] = 'sh'
      yield instance 


      
