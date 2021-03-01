from pprint import pprint
from lxml import html
import requests


header = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}


def mail_parser(link):
    news = {}
    response = requests.get(link, headers=header)
    dom = html.fromstring(response.text)
    source = dom.xpath("//a[@class='link color_gray breadcrumbs__link']//text()")[0]
    date = dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]
    title = dom.xpath("//h1[@class='hdr__inner']/text()")[0]
    news['source'] = source
    news['title'] = title
    news['link'] = link
    news['date'] = '/'.join(date[:10].split('-')[::-1])
    return news


def mail_scan():
    mail_link = 'https://news.mail.ru'
    mail_response = requests.get(mail_link, headers=header)
    mail_dom = html.fromstring(mail_response.text)
    mail_list = []

    main_news_link = mail_dom.xpath("//a[@class='photo photo_full photo_scale js-topnews__item']/@href")[0]
    mail_list.append(mail_parser(main_news_link))

    days_news_link = mail_dom.xpath("//td[@class='daynews__items']//@href")
    for item in days_news_link:
        new_link = item
        mail_list.append(mail_parser(new_link))

    other_news = mail_dom.xpath("//ul[@class='list list_type_square list_half js-module']/li[@class='list__item']/a/@href")
    for item in other_news:
        new_link = item
        mail_list.append(mail_parser(new_link))

    bottom_news = mail_dom.xpath("//span[@class='list__text']//@href")
    for item in bottom_news:
        new_link = item
        mail_list.append(mail_parser(new_link))

    cells_news = mail_dom.xpath("//span[@class='cell']//@href")
    for item in cells_news:
        new_link = item
        mail_list.append(mail_parser(new_link))

    return pprint(mail_list)


def lenta_news(lenta_link):
    lenta_response = requests.get(lenta_link, headers=header)
    lenta_dom = html.fromstring(lenta_response.text)
    main_news = lenta_dom.xpath("//section[contains(@class, 'b-top7-for-main')]//div[contains(@class, 'item')]")
    news_container = []
    for new in main_news:
        news = {}
        link_to_new = new.xpath(".//a/@href")[0]
        time_of_new = new.xpath(".//a/time[@class]/@datetime")
        title_of_new = new.xpath(".//a/text()")[0]
        news['source'] = 'Lenta news'
        news['link'] = lenta_link + link_to_new
        news['title'] = title_of_new.replace(u'\xa0', u'')
        news['time'] = time_of_new
        news_container.append(news)
    return pprint(news_container)


def yandex_news(yandex_link):
    yandex_response = requests.get(yandex_link, headers=header)
    yandex_dom = html.fromstring(yandex_response.text)
    main_news = yandex_dom.xpath("//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']/div")
    news_container = []
    for new in main_news:
        news = {}
        link_to_new = new.xpath(".//a[@class='news-card__link']/@href")[0]
        time_of_new = new.xpath(".//span[@class='mg-card-source__time']/text()")[0]
        title_of_new = new.xpath(".//h2[@class='news-card__title']/text()")[0]
        source = new.xpath(".//span[@class='mg-card-source__source']/a/text()")[0]
        news['source'] = source
        news['link'] = link_to_new
        news['title'] = title_of_new
        news['time'] = time_of_new
        news_container.append(news)
    other_news = yandex_dom.xpath("//div[@class='mg-grid__row mg-grid__row_gap_8']")
    for new in other_news:
        news = {}
        link_to_new = new.xpath(".//div[@class='news-card__text-content']//@href")[0]
        time_of_new = new.xpath(".//span[@class='mg-card-source__time']/text()")[0]
        title_of_new = new.xpath(".//h2[@class='news-card__title']/text()")[0]
        source = new.xpath(".//span[@class='mg-card-source__source']/a/text()")[0]
        news['source'] = source
        news['link'] = link_to_new
        news['title'] = title_of_new
        news['time'] = time_of_new
        news_container.append(news)
    return pprint(news_container)


mail_scan()
lenta_news('https://lenta.ru/')
yandex_news('https://yandex.ru/news/')
