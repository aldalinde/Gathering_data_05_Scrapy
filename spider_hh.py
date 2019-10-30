# -*- coding: utf-8 -*-
import scrapy
from vacancyparser.items import VacancyparserItem


class SpiderHhSpider(scrapy.Spider):
    name = 'spider_hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=python&showClusters=true']

    def parse(self, response):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)'
        ).extract()

        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response):
        name = response.css('div.vacancy-title h1.header::text').extract_first()
        link = response.url
        salary = response.css('div.vacancy-title p.vacancy-salary::text').extract_first()
        currency = response.css('div.vacancy-title span[itemprop*=baseSalary] meta[itemprop*=currency]::attr(content)'
                                ).extract_first()
        min_salary = response.css(
            'div.vacancy-title span[itemprop*=baseSalary] span[itemprop*=value] meta[itemprop*=minValue]::attr(content)'
        ).extract_first()
        max_salary = response.css(
            'div.vacancy-title span[itemprop*=baseSalary] span[itemprop*=value] meta[itemprop*=maxValue]::attr(content)'
        ).extract_first()

        yield VacancyparserItem(name=name, link=link, salary=salary, currency=currency, min_salary=min_salary,
                                max_salary=max_salary)

