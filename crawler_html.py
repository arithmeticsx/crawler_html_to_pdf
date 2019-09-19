#!/usr/bin/python3
#-*- coding:utf-8 -*-

'coding for crawler'

__author__ = 'arithmeticsx@gmail.com'


import requests, bs4
from lxml import etree
import os, time, pdfkit, PyPDF2
from __init__ import LOG


base_url = ''
css_selector = ''
xpath_selector = ''

def parse_contents(contents_pattern, html):
    pass

def request_html(url, body):
    if not str(url).startswith('http'):
        url = 'http://' + url
    res = requests.get(url)
    res.raise_for_status()
    text = res.text
    contents_rlt = ''
    file_name = str(hash(time.time())).strip()

    if str(css_selector).strip() == '' and str(xpath_selector).strip() == '':
        contents_rlt = []
        contents_rlt.append(url)
    elif str(css_selector).strip() != '':
        contents_rlt = css_parse(css_selector, text)
    elif str(xpath_selector).strip() != '':
        contents_rlt = xpath_parse(xpath_selector, text)

    # 对contents_rlt列表中的每个url进行访问获取html，取body的内容转成pdf
    os.chdir(os.path.join(os.getcwd(), 'output_files'))
    if contents_rlt != None and contents_rlt != '':
        for num in range(len(contents_rlt)): 
            if num == 0:
                # 创建文件夹
                if not os.path.exists(os.path.join(os.getcwd(), file_name)):
                    os.makedirs(os.path.join(os.getcwd(), file_name))
                    os.chdir(os.path.join(os.getcwd(), file_name))
                
            page_url = base_url + contents_rlt[num]
            # 抓取页面并保存pdf
            try:
                if body:
                    scrapy_pagebody(page_url, num)
                else:
                    scrapy_page(page_url, num)
            except Exception:
                LOG.error('scrapy %s--%s page faild!!'.format(page_url, num))
    # 抓取结束后将合并pdf成一个pdf文档，并删除中间文件
    merge_pdf(len(contents_rlt))

def merge_pdf(num):
    pdf_files = []
    for i in range(num):
        file_name = str(i).strip()+'.pdf'
        pdf_files.append(file_name)

    pdf_writer = PyPDF2.PdfFileWriter()

    for file_name in pdf_files:
        try:
            pdf_obj = open(file_name, 'rb')
            pdf_reader = PyPDF2.PdfFileReader(pdf_obj)
            for page_num in range(pdf_reader.numPages):
                page_obj = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page_obj)
        except Exception:
            LOG.error('can not handle the %s file'.format(file_name))

    pdf_output = open('output.pdf', 'wb')
    pdf_writer.write(pdf_output)
    pdf_output.close()
    for one_file in os.listdir('.'):
        if str(one_file).strip() != 'output.pdf':
            os.remove(one_file)

def css_parse(pattern, html_text):
    soup = bs4.BeautifulSoup(html_text)
    result = soup.select(str(pattern).strip())
    return result

def xpath_parse(pattern, html_text):
    html = etree.HTML(html_text)
    result = html.xpath(str(pattern).strip())
    return result

def scrapy_pagebody(url, num):
    page_html = requests.get(url)
    #TODO:细节页面html的body部分，并调用系统外部命令，将html转换成pdf，并保存该页
    page_etree = etree.HTML(page_html.text)
    page_body = page_etree.xpath('//body')
    body_text = etree.tostring(page_body[0])

    html_teplate = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
        {content}
        </body>
        </html>
    """

    options = {
        'page-size' : 'Letter',
        'margin-top' : '0.75in',
        'margin-right' : '0.75in',
        'margin-bottiom' : '0.75in',
        'margin-left' : '0.75in',
        'encoding' : 'UTF-8',
        'no-outline' : None
    }

    pdfkit.from_string(html_teplate.format(content=str(body_text)), str(num).strip()+'.pdf')

def scrapy_page(url, num):
    try:
        pdfkit.from_url(url, str(num).strip()+'.pdf')
    except Exception:
        html = requests.get(url)
        pdfkit.from_string(str(html.text), str(num).strip()+'.pdf')

def start_scrapy(url, web_base='', css_pattern='', xpath_pattern='', body=True):
    global base_url, css_selector, xpath_selector
    base_url = str(web_base).strip()
    if body:
        if str(css_pattern).strip() != '':
            css_selector = str(css_pattern).strip()
        elif str(xpath_pattern).strip() != '':
            xpath_selector = str(xpath_pattern).strip()
        if str(url).strip() == '' or (css_selector == '' and xpath_selector==''):
            raise Exception('url and pattern can not be empty!!!!')
    request_html(url, body=body)

