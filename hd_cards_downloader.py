# Created by Alexsander Rosante

from urllib import request, error
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
    for card in deck:
        code = card[:-1]
        aux.append(code)
    deck = aux[1:]
    return deck


def download(deck, deck_size):
    """Recieves a list and downloads the cards pics"""
    counter = 0
    for card in deck:
        try:
            request.urlretrieve("https://storage.googleapis.com/ygoprodeck.com/pics/" + card + ".jpg",
                                "pics/" + card + ".jpg")
        except error.HTTPError:
            pass
        counter += 1
        print("Downloading... (" + str(counter) + "/" + str(deck_size) + ") [" +
              str(round(counter / deck_size * 100)) + "%]", end='\r')
        time.sleep(0.04)
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
