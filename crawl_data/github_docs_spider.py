import csv
import scrapy
from scrapy.crawler import CrawlerProcess


class GithubDocsSpider(scrapy.Spider):
    name = "github_docs"

    def start_requests(self):
        url = "https://docs.github.com/en/github"
        yield scrapy.Request(url=url, callback=self.parse1)
    
    def parse1(self, response):
        c_link = response.css("a.article-link::attr(href)").getall()
        for url in c_link:
            yield response.follow(url=url, callback=self.parse2)

    def parse2(self, response):
        c_link = response.css("a.article-link::attr(href)").getall()
        for url in c_link:
            yield response.follow(url=url, callback=self.parse3)
            
    def parse3(self, response):
        # url = response.css('li.is-current-page > a::attr(href)').getall()
        url = response.request.url
        headline = response.css('h1.border-bottom-0::text').getall()
        content = response.css('div#article-contents').getall()

        with open('./data/data_crawl.csv','a') as f:
            for u in url:
                f.write(u + ",")
            for h in headline:
                f.write(h + ",")
            for c in content:
                f.write(str([c]))
            f.write('\n')

process = CrawlerProcess()
process.crawl(GithubDocsSpider)
process.start()