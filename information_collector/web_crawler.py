# -*- coding: utf-8 -*-

import datetime
import glob
import shutil
from contextlib import contextmanager
from operator import itemgetter
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

URL = 'https://www.moex.com'


# функция выбирает диапазон с ПЕРВОГО числа по выбранную дату и возвращает не упорядоченные строки с таблицы
def click_currency_rate(website, currency, data):
    # кликаем на нужные валюты
    website.find_element_by_xpath('//option[@value="{}"]'.format(currency)).click()

    # выставляем начало срока
    # кликаем на первое число
    website.find_element_by_xpath('//*[@id="d1day"]/option[@value="1"]').click()
    # кликаем на месяц
    website.find_element_by_xpath('//*[@id="d1month"]/option[@value="{}"]'.format(data.month)).click()
    # кликаем на год
    website.find_element_by_xpath('//*[@id="d1year"]/option[@value="{}"]'.format(data.year)).click()

    # аналогично для конца срока
    # кликаем на первое число
    website.find_element_by_xpath('//*[@id="d2day"]/option[@value="{}"]'.format(data.day)).click()
    # кликаем на месяц
    website.find_element_by_xpath('//*[@id="d2month"]/option[@value="{}"]'.format(data.month)).click()
    # кликаем на год
    website.find_element_by_xpath('//*[@id="d2year"]/option[@value="{}"]'.format(data.year)).click()

    # кликакем показать
    website.find_element_by_name("bSubmit").click()

    # получаем список элементов класса tr1(белая полоса в таблице)
    tr1 = website.find_elements_by_class_name("tr1")
    # получаем список элементов класса tr0(серая полоса в таблице)
    tr0 = website.find_elements_by_class_name("tr0")

    return [itemgetter(0, 3)(el.text.split()) for el in tr1 + tr0]


def get_currency_pair(*pairs, date=datetime.date.today(), driver_path=None):
    options = Options()
    options.headless = True

    with webdriver.Firefox(options=options, executable_path=driver_path) as driver:
        driver.get(URL)
        # кликаем на меню
        driver.find_element_by_xpath(
            "//*[@class='header-menu__item js-menu-dropdown']/a[@href='javascript:void(0)']").click()
        # кликаем на срочный рынок
        driver.find_element_by_link_text("Срочный рынок").click()
        # соглашаемся с условиями использовани
        driver.find_element_by_link_text("Согласен").click()
        # кликаем на индикативные курсы
        driver.find_element_by_link_text("Индикативные курсы").click()

        return {pair: click_currency_rate(driver, pair, date) for pair in pairs}


WEBDRIVER_URL = {
    'win': 'https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-win64.zip',
    'linux': 'https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz',
}


@contextmanager
def download_webdriver(platform='win'):
    with TemporaryDirectory() as driver_dir:
        url = WEBDRIVER_URL[platform]
        with TemporaryDirectory() as tmp_dir:
            archive = Path(tmp_dir).joinpath(Path(url).name)
            archive.write_bytes(urlopen(url).read())
            shutil.unpack_archive(str(archive), driver_dir)
        yield glob.glob(driver_dir + '/geckodriver*')[0]
