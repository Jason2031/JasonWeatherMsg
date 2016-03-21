# coding=utf-8
import smtplib
import os
from lxml import etree
from email.mime.text import MIMEText
import sys


class JasonEmailSender:
    def __init__(self):
        try:
            fileData = open(sys.path[0] + '/data.xml', 'r')
            xmlData = fileData.read()
            selector = etree.XML(xmlData)
        except Exception, e:
            print str(e)
        finally:
            fileData.close()
        self.host = selector.xpath('//mailHost')[0].text
        self.user = selector.xpath('//mailUser')[0].text + '@' + selector.xpath('//mailPostfix')[0].text
        self.psw = selector.xpath('//mailPsw')[0].text
        self.nickName = selector.xpath('//nickName')[0].text
        mailTo = selector.xpath('//mailToList')[0]
        self.mailToList = {}
        self.toSendMsg = {}
        for m in mailTo:
            email = m.xpath('./@to')[0]
            places = m.xpath('./city')
            mailTxt = ''
            for place in places:
                if not place.text in self.toSendMsg.keys():
                    try:
                        fileData = open(sys.path[0] + '/weather_parsed/%s.txt' % place.text, 'r')
                        self.toSendMsg[place.text] = fileData.read()
                    except Exception, e:
                        print str(e)
                    finally:
                        fileData.close()
                mailTxt += self.toSendMsg[place.text] + os.linesep + '-----------------' + os.linesep
            self.mailToList[email] = mailTxt

    def sendMail(self, to, content):
        me = '<' + self.user + '>'
        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = '来自Jason的天气预报'
        msg['From'] = me
        msg['To'] = to
        try:
            server = smtplib.SMTP()
            server.connect(self.host)
            server.login(self.user, self.psw)
            server.sendmail(me, to, msg.as_string())
            server.close()
        except Exception, e:
            print str(e)

    def sendOut(self):
        for item, value in self.mailToList.items():
            self.sendMail(item, value)
            print 'E-mail sent to '+str(item)


if __name__ == '__main__':
    emailSender = JasonEmailSender()
    emailSender.sendOut()
