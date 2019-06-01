from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import os
import pickle
if len(sys.argv)<3:
    print('Error: Insufficient data')
    exit
os.mkdir(str(sys.argv[2]))
class FlipkartItem(scrapy.Item):
    
    # define the fields for your item here like:
    # name = scrapy.Field()
    laptop_name = scrapy.Field()
    laptop_price = scrapy.Field()
    laptop_rating = scrapy.Field()
    
class MySpider(scrapy.Spider):
    count=sys.argv[1]
    flag=1
    counter=0
    path=sys.argv[2]
    items=FlipkartItem()
    name = 'flipkart'
    page_number = 2
    start_urls = ['https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1']
    laptops=[]
    def parse(self, response):
        items=FlipkartItem()
        laptop_name=response.css('._3wU53n').css('::text').extract()
        laptop_rating=response.css('.hGSR34').css('::text').extract()
        laptop_price=response.css('._2rQ-NK').css('::text').extract()
        MySpider.counter+=len(laptop_name)
        if int(MySpider.counter)>int(MySpider.count):
            MySpider.flag=0
            for i in range(int(MySpider.count),int(MySpider.counter)):
                del laptop_name[-1]
                del laptop_price[-1]
                del laptop_rating[-1]
        items['laptop_name'] = laptop_name
        items['laptop_price'] = laptop_price
        items['laptop_rating'] = laptop_rating
        
        MySpider.laptops.append(items)
                
        next_page='https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=' +str(MySpider.page_number)
        if MySpider.page_number<=29 and MySpider.flag==1:
            MySpider.page_number+=1
            yield response.follow(next_page,callback = self.parse)
        f=open(str(MySpider.path)+'/'+'laptop.p','wb')
        pickle.dump(self.laptops,f)
        f.close()

process=CrawlerProcess()
process.crawl(MySpider)
process.start()
f=open(str(MySpider.path)+'/'+'laptop.p','rb')
laptop_dict=pickle.load(f)
print(MySpider.laptops)
