#!/usr/bin/python3
#-*- coding:utf-8 -*-

'test code'

__author__ = 'arithmeticsx@gmail.com'



import crawler_html

if __name__=="__main__":
   # crawler_html.start_scrapy('https://jimmysong.io/istio-handbook/', 'https://jimmysong.io/istio-handbook/', xpath_pattern='//li[@class="chapter "]/a[@href]/@href', body=False)
   crawler_html.start_scrapy('www.github.com', body=False)
