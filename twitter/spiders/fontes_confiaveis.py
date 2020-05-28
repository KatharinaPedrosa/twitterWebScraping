# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
import hashlib

class FontesConfiaveisSpider(scrapy.Spider):
    name = 'fontes_confiaveis'
    allowed_domains = ['twitter.com']
    start_urls = ['https://twitter.com/minsaude',
                  'https://twitter.com/fiocruz']

    def parse(self, response):
        for tweet in response.css('.tweet'):
            data = tweet.css('.tweet-timestamp::attr("title")').get()
            fonte = tweet.css('.username').css('b::text').get()
            s = ''
            texto = s.join(tweet.css('.TweetTextSize::text').getall())
            hashTexto = hashlib.md5(texto.encode('utf8')).hexdigest()

            dados = {'fonte': fonte, 'data': data, 'texto':texto, 'hash': hashTexto}
            client = MongoClient('mongodb://localhost:27017')
            data_base = client['scrap']
            collection = data_base['tweets']

            query = {'hash':hashTexto}
            resultado = collection.find(query)
            if resultado.count() == 0:
                collection.insert(dados)





