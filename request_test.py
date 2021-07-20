import requests
import json
import re
import hashlib
from selenium import webdriver
import time


def do_hash(string):
    '''
    Получаум hash имени игрока
    :param string: Имя игрока
    :return: md5
    '''
    return hashlib.md5(f"{string}".encode('utf-8')).hexdigest()


def go_parse(url):
    '''
     Главная функция
    :param url: Url адрес для парсинга
    :return: Список с результатми
    '''
    r = requests.get(url)
    response = json.loads(r.text)
    football_id = []
    resault_gamers = {}
    all_league = []

    for sport in response['sports']:
        el = sport
        if (re.match(r'Футбол', el['name']) != None and sport['kind'] == 'sport'):
            football_id.append(el['id'])

    for league in response['sports']:
        if league.get('parentId'):
            if football_id.count(league['parentId']) > 0:
                all_league.append(league['id'])

    print('xx')
    for event in response['events']:
        if event.get('sportId') != None:
            parentId = event['sportId']
            if all_league.count(parentId) > 0 and event['level'] == 1:
                gamer1 = event['team1']
                gamer2 = event['team2']
                game_name = f"{gamer1} - {gamer2}"
                gamer_object = {
                    do_hash(gamer1): gamer1,
                    do_hash(gamer2): gamer2
                }
                resault_gamers[game_name] = gamer_object

    return resault_gamers

gamers = go_parse('https://line11.bkfon-resources.com/live/currentLine/ru')

first_name = next(iter(gamers))

def selenium_random_search(name_of_game):
    """
    Получение ссылки и переход на страницу по первому элементу из результата функции go_parse
    :param name_of_game: имена игроков для поиска матча
    :return:
    """
    chromedriver = '/Users/levhotylev/Desktop/chromedrv/chromedriver' # Работаю на mac, в связи с чем передаю в ручную путь до драйвера
    driver = webdriver.Chrome()
    driver.get("https://www.fonbet.ru/")
    time.sleep(5)
    search_elem = driver.find_element_by_class_name('search__link')
    search_elem.click()
    search_comp = driver.find_element_by_id('search-component')
    input_filed = search_comp.find_element_by_tag_name('input')
    input_filed.send_keys(name_of_game)
    time.sleep(0.5)
    search_resault = driver.find_element_by_id('search-container')
    time.sleep(2)
    search_resault_div = search_resault.find_elements_by_tag_name('div')
    for item in search_resault_div:
        if re.search(r'^search__dropdown--', item.get_attribute('class')):
            resault_table = item.find_elements_by_tag_name('div')
            for item_table in resault_table:
                if re.search(r'^search-result__event--', item_table.get_attribute('class')):
                    h_ref = item_table.find_element_by_tag_name('a')
                    print('Название игры - ', h_ref.text)
                    h_ref.click()
                    time.sleep(4)
                    break
            break
    driver.quit()


# selenium_random_search(first_name)
