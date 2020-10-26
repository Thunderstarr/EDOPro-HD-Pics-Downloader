# Created by Alexsander Rosante

import urllib.request
import time


def get_deck_list(deck_name):
    """Returns a list of all cards code from a ydk file"""
    try:
        deck = open(deck_name).readlines()
    except FileNotFoundError:
        print('Deck not found')
        return False
    deck.remove("#main\n")
    deck.remove("#extra\n")
    deck.remove("!side\n")
    aux = []
    for carta in deck:
        code = carta[:-1]
        aux.append(code)
    deck = aux[1:]
    return deck


def download(deck, deck_size):
    """Recieves a list and downloads the cards pics"""
    counter = 0
    for carta in deck:
        urllib.request.urlretrieve("https://storage.googleapis.com/ygoprodeck.com/pics/" + carta + ".jpg",
                                   "pics/" + carta + ".jpg")
        counter += 1
        print("Downloading... (" + str(counter) + "/" + str(deck_size) + ") [" +
              str(round(counter/deck_size * 100)) + "%]", end="\r")
    print('')


def main():
    print('Created by Alexsander Rosante')
    print('This program downloads cards pics from https://db.ygoprodeck.com/\n')
    deck_name = "deck/" + input("Insert deck name (without .ydk): ") + ".ydk"
    print('')
    deck = get_deck_list(deck_name)
    if deck:
        download(deck, len(deck))
    tick = 5
    print('')
    while tick != 0:
        print("Finished. Exiting in " + str(tick) + " seconds...", end="\r")
        tick -= 1
        time.sleep(1)


main()
