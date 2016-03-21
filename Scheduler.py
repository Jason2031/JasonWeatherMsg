from WeatherCrawler import JasonWeatherCrawler
from EmailSender import JasonEmailSender
from apscheduler.schedulers.background import BackgroundScheduler
import time


def send():
    print 'send starts'
    weathercrawler = JasonWeatherCrawler()
    weathercrawler.crawlParseAndSave()
    emailsender = JasonEmailSender()
    emailsender.sendOut()
    print 'Sent!'


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(send, 'cron', day_of_week='mon-sun', hour=7, minute=30, end_date='2015-12-31')
    scheduler.add_job(send, 'cron', day_of_week='mon-sun', hour=12, minute=30, end_date='2015-12-31')
    scheduler.add_job(send, 'cron', day_of_week='mon-sun', hour=20, minute=0, end_date='2015-12-31')
    scheduler.start()
    print 'Scheduler started!'
    try:
        while 1:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
