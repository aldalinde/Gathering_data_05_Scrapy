# -*- coding: utf-8 -*-
import scrapy
import numpy as np
from vacancyparser.items import VacancyparserItem


class SpiderSjSpider(scrapy.Spider):
    name = 'spider_sj'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response):

        next_page = response.css('a.f-test-link-dalshe::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancy = response.css('div._3zucV div.f-test-vacancy-item a[href*="/vakansii/"]::attr(href)').extract()

        for link in vacancy:
             yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response):
        name = response.css('h1::text').extract_first()
        link = response.url

        salary = response.css('span[class*="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"] ::text').extract()

        if len(salary)==1:
            currency = np.nan
            min_salary = np.nan
            max_salary = np.nan
        elif len(salary)==5:
            currency = salary[4]
            min_salary = salary[2]
            max_salary = np.nan
        elif len(salary)==7:
            currency = salary[6]
            min_salary = salary[0]
            max_salary = salary[4]
        elif len(salary)==3:
            currency = salary[2]
            min_salary = salary[0]
            max_salary = salary[0]
        else:
            currency = np.nan
            min_salary = np.nan
            max_salary = np.nan

        salary = ''.join(salary)
        print(salary)
        yield VacancyparserItem(name=name, link=link, salary=salary, currency=currency, min_salary=min_salary,
                                max_salary=max_salary)

