"""Created by Alexsander Rosante 2021"""
import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup


def ydk_to_list(deck_name):
    """Converts .ydk file into a list"""
    dk, aux = [], []
    code_blacklist = '#main', '!side', '#extra'
    try:
        dk = open('deck/' + deck_name + '.ydk').readlines()
    except FileNotFoundError:
        return False
    for card in dk:
        code = card[:-1]
        if code not in code_blacklist:
            aux.append(code)
    dk = aux[1:]
    return dk


def list_to_ydk(deck_name, card_list):
    """Converts list into a .ydk file"""
    with open(f'deck/{deck_name}.ydk', 'w') as fp:
        fp.write('#created by AlexsanderRosante\n')
        fp.write('#main\n')
        for card_id in card_list:
            fp.write(f'{card_id}\n')
        fp.write('!side\n')
        fp.write('#extra\n')


def get_website_page_cards(flags, offset=0):
    """Return a list of id in a page from the website"""
    url = f'https://db.ygoprodeck.com/search/?{flags}&offset={offset}&view=List'
    browser = webdriver.Firefox(service=Service(executable_path='geckodriver.exe'))
    browser.get(url)
    time.sleep(6)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    card_list = []
    for card in soup.find("div", {"id": "card-list"}).find_all('a'):
        card_img = card.find("div", {"id": "card-container"}).find("div", {"id": "card-img"})
        try:
            card_id = dict(card_img.find("img").attrs)['data-src'].split('/')[-1].split('.')[0]
            card_list.append(card_id)
        except KeyError:
            pass
    browser.close()
    return card_list


def get_new_cards(pages=1):
    new_cards = []
    for i in range(pages):
        new_cards.extend(get_website_page_cards(flags='&sort=new&sortorder=desc&num=100', offset=i * 100))
    return new_cards


def get_new_fields(pages=1):
    new_fields, flags = [], '?&type=Spell Card&race=Field&sort=new&sortorder=desc&num=100'
    for i in range(pages):
        new_fields.extend(get_website_page_cards(flags=flags, offset=i * 100))
    return new_fields


def update_all_cards():
    all_cards = ydk_to_list('allcards')
    new_cards = []
    for card_id in get_new_cards(5):
        if card_id not in all_cards:
            all_cards.append(card_id)
            new_cards.append(card_id)
    list_to_ydk('newcards', new_cards)
    list_to_ydk('allcards', all_cards)


def update_all_fields():
    all_fields = ydk_to_list('allfields')
    for card_id in get_new_fields(2):
        if card_id not in all_fields:
            all_fields.append(card_id)
    list_to_ydk('allfields', all_fields)


if __name__ == '__main__':
    pass
