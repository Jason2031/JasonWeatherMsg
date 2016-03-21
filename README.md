# JasonWeatherMsg
定期爬取中国天气网数据并通过邮件发送至邮箱

依赖项
* lxml
* request
* urllib
* urllib2
* smtplib
* email
* apscheduler

----------------------

使用时要将城市代码存入data.xml里，访问http://www.weather.com.cn/并输入城市名，url中的数字串即为城市代码，如北京市页面url为http://www.weather.com.cn/weather/101010100.shtml，则北京市的城市代码为"101010100"。

需要发送的邮箱放在<mailToList>标记里，发送方的数据则是<mailHost>、<mailUser>、<mailPsw>、<mailPostfix>、<nickName>，分别代表邮箱服务器地址、邮箱用户名、密码、邮箱后缀（不包括"@"）、昵称。

以上数据在data.xml里均有示意。
