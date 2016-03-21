# coding=utf-8
import requests
import os
import time
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class JasonWeatherCrawler:
    def __init__(self):
        try:
            fileData = open(sys.path[0] + '/data.xml', 'r')
            xmlData = fileData.read()
            selector = etree.XML(xmlData)
        except Exception, e:
            print str(e)
        finally:
            fileData.close()
        self.baseURL = selector.xpath('//weatherURL')[0].text
        cities = selector.xpath('//places')[0]
        self.cityID = {}
        for city in cities:
            self.cityID[city.tag] = city.text

    def crawlParseAndSave(self):
        for item, value in self.cityID.items():
            url = self.baseURL % value

            html = requests.get(url).content
            try:
                fileHandler = open(sys.path[0] + '/weather_raw/%s_raw.txt' % item, 'w')
                fileHandler.write(html)
            except Exception, e:
                print str(e)
            finally:
                fileHandler.close()
            selector = etree.HTML(html)

            place = selector.xpath('//title')[0].text.split('】')[0].split('【')[1]

            needed = selector.xpath('//div[@class="left fl"]/div[@class="today clearfix"]')[0]
            todayTitle = needed.xpath('./input[@id="hidden_title"]/@value')[0]
            components = todayTitle.split('  ')
            try:
                updateTime = needed.xpath('./input[@id="fc_24h_internal_update_time"]/@value')[0]
            except:
                updateTime = needed.xpath('./input[@id="fc_24h_external_update_time"]/@value')[0]
                timeArray = time.strptime(updateTime, '%Y%m%d%H%M%S')
                updateTime = time.strftime('%Y-%m-%d %H:%M', timeArray)
            forcast = needed.xpath('./div[@class="t"]/ul')[0]

            forcast1Title = forcast[0].xpath('./h1')[0].text
            forcast1Weather = forcast[0].xpath('./p[@class="wea"]/@title')[0].split(' ')[0]
            forcast1Temperature = forcast[0].xpath('./p[@class="tem"]/span')[0].text + '℃'
            forcast1WindDir = forcast[0].xpath('./p[@class="win"]/span')[0]
            forcast1Wind = forcast1WindDir.text + ' ' + forcast1WindDir.xpath('./@title')[0]
            forcast1Sun = forcast[0].xpath('./p')[3].xpath('./span')[0].text

            forcast2Title = forcast[1].xpath('./h1')[0].text
            forcast2Weather = forcast[1].xpath('./p[@class="wea"]')[0].text.split(' ')[0]
            forcast2Temperature = forcast[1].xpath('./p[@class="tem"]/span')[0].text + '℃'
            forcast2WindDir = forcast[1].xpath('./p[@class="win"]/span')[0]
            forcast2Wind = forcast2WindDir.text + ' ' + forcast2WindDir.xpath('./@title')[0]
            forcast2Sun = forcast[1].xpath('./p')[3].xpath('./span')[0].text

            try:
                life = selector.xpath('//div[@class="livezs"]')[0]
                lifeUpdateTime = life.xpath('./input[@id="zs_7d_update_time"]/@value')
                data = life.xpath('./ul')[0]

                ultravioletRay = data[0].xpath('./em')[0].text + ' ' + data[0].xpath('./p')[0].text
                flu = data[1].xpath('./em')[0].text + ' ' + data[1].xpath('./p')[0].text
                clothes = data[2].xpath('./em')[0].text + ' ' + data[2].xpath('./p')[0].text
                car = data[3].xpath('./em')[0].text + ' ' + data[3].xpath('./p')[0].text
                traffic = data[4].xpath('./em')[0].text + ' ' + data[4].xpath('./p')[0].text
                air = data[5].xpath('./em')[0].text + ' ' + data[5].xpath('./p')[0].text
            except:
                ultravioletRay = '无紫外线指数'
                flu = '无感冒指数'
                clothes = '无穿衣指数'
                car = '无洗车指数'
                traffic = '无交通指数'
                air = '无空气污染扩散指数'

            fileHandler = open(sys.path[0] + '/weather_parsed/%s.txt' % item, 'w')
            fileHandler.write(str(place) + os.linesep)
            fileHandler.write('时间：' + components[0] + os.linesep)
            fileHandler.write('天气：' + components[1] + os.linesep)
            fileHandler.write('气温：' + components[2] + os.linesep)
            fileHandler.write('更新时间：' + updateTime + os.linesep)
            fileHandler.write(os.linesep)
            fileHandler.write(forcast1Title + os.linesep)
            fileHandler.write(forcast1Weather + os.linesep)
            fileHandler.write(forcast1Temperature + os.linesep)
            fileHandler.write(forcast1Wind + os.linesep)
            fileHandler.write(forcast1Sun + os.linesep)
            fileHandler.write(os.linesep)
            fileHandler.write(forcast2Title + os.linesep)
            fileHandler.write(forcast2Weather + os.linesep)
            fileHandler.write(forcast2Temperature + os.linesep)
            fileHandler.write(forcast2Wind + os.linesep)
            fileHandler.write(forcast2Sun + os.linesep)
            fileHandler.write(os.linesep)
            fileHandler.write(ultravioletRay + os.linesep)
            fileHandler.write(flu + os.linesep)
            fileHandler.write(clothes + os.linesep)
            fileHandler.write(car + os.linesep)
            fileHandler.write(traffic + os.linesep)
            fileHandler.write(air + os.linesep)
            fileHandler.close()


if __name__ == '__main__':
    crawler = JasonWeatherCrawler()
    crawler.crawlParseAndSave()
