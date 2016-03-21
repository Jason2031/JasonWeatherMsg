from WeatherCrawler import JasonWeatherCrawler
from EmailSender import JasonEmailSender

if __name__ == '__main__':
    weatherCrawler = JasonWeatherCrawler()
    weatherCrawler.crawlParseAndSave()
    emailSender = JasonEmailSender()
    emailSender.sendOut()
    print 'Done!'
