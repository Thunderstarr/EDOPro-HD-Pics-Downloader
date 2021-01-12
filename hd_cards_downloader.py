# Created by Alexsander Rosante

from urllib import request, error
import time


def get_deck_list(deck_name):
    """Returns a list of all cards code from a ydk file"""
    try:
        deck = open('deck/' + deck_name + '.ydk').readlines()
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


def download(deck: list,
             database_url='https://storage.googleapis.com/ygoprodeck.com/pics/',
             folder='pics/',
             final_extension='.jpg'):
    """Recieves a list and downloads the cards pics"""
    deck_size, counter = len(deck), 0
    for card in deck:
        try:
            request.urlretrieve(database_url + card + ".jpg",
                                folder + card + final_extension)
        except error.HTTPError:
            pass
        counter += 1
        print("Downloading... (" + str(counter) + "/" + str(deck_size) + ") [" +
              str(round(counter / deck_size * 100)) + "%]", end='\r')
        time.sleep(0.04)
    print('')


def main(exit_tick: int = 5):
    # Intro prints
    print('Created by Alexsander Rosante')
    print('Download only from github.com/AlexsanderRST/edopro-hd-cards-downloader')
    print('This program downloads cards pics from db.ygoprodeck.com/\n')
    print('Enter /help to see the commands')

    # Input
    done = False
    while not done:
        deck_name = input("Insert deck name (without .ydk) or command: ")
        if deck_name == '/help':
            print('\nCommands:')
            print(" /allcards to download all cards pics")
            print(" /allfields to download all fields artworks")
            print(' /exit to exit\n')
        elif deck_name == '/exit':
            done = True
        else:
            if deck_name in ('/allfields', '/allcards'):
                if deck_name == '/allfields':
                    deck_name, url = 'allfields', 'https://tinyurl.com/y26zea99'
                else:
                    deck_name, url = 'allcards', 'https://tinyurl.com/y5om2agl'
                request.urlretrieve(url, 'deck/' + deck_name + '.ydk')
            time.sleep(0.5)
            print('')
            deck = get_deck_list(deck_name)
            if deck:
                if deck_name == 'allfields':
                    download(deck,
                             'https://storage.googleapis.com/ygoprodeck.com/pics_artgame/',
                             'pics/field/',
                             '.png')
                else:
                    download(deck)
            done = True

    # Exit
    print('')
    while exit_tick != 0:
        print('Finished. Exiting in ' + str(exit_tick) + ' seconds...', end='\r')
        exit_tick -= 1
        time.sleep(1)


main()
