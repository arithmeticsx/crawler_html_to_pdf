#!/usr/bin/python3
#-*- coding:utf-8 -*-

'project init'

__author__ = 'arithmeticsx@gmail.com'


import logging


logging.basicConfig(level=logging.INFO,
                    filename='output.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

LOG = logging.getLogger(__name__)





