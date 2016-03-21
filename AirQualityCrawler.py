# coding=utf-8
import requests
import os
import time
from lxml import etree
import urllib
import urllib2
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class JasonAirQualityCrawler:
    def __init__(self):
        try:
            fileData = open('./data.xml', 'r')
            xmlData = fileData.read()
            selector = etree.XML(xmlData)
        except Exception, e:
            print str(e)
        finally:
            fileData.close()
        self.baseURL = selector.xpath('//airURL')[0].text
        cities = selector.xpath('//places')[0]
        self.cityID = {}
        for city in cities:
            self.cityID[city.tag] = city.text

    def crawlParseAndSave(self):
        for item, value in self.cityID.items():
            url = self.baseURL % value

            html = requests.get(url).content
            try:
                fileHandler = open('./air_raw/%s_raw.txt' % item, 'w')
                fileHandler.write(html)
            except Exception, e:
                print str(e)
            finally:
                fileHandler.close()
            selector = etree.HTML(html)


if __name__ == '__main__':
    crawler = JasonAirQualityCrawler()
    crawler.crawlParseAndSave()
    print 'Done!'
