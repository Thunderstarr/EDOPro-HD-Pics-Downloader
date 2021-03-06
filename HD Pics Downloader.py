"""
Created by Alexsander Rosante 2021
Github: https://github.com/AlexsanderRST
"""

from math import sin
from urllib import request, error
from pygame.locals import *
from webbrowser import open as open_url

import pygame
import threading

version = '2.3.0'

pygame.init()
pygame.font.init()

# font
default_font = 'Arial'

# Colors
colorBackground = '#29282e'
colorButton = '#0252b1'
colorButtonHovered = '#1b63b8'
colorButtonText = '#ffffff'
colorButtonTextHovered = '#ffffff'
colorText = '#282829'
colorDownloadbar = '#1b63b8'
colorInputboxActive = '#00ffff'

# Events
BKSP_DOWN = USEREVENT + 1


class App:
    def __init__(self):
        # display
        self.display = pygame.display.set_mode((display_w, display_h), NOFRAME)
        self.bg_color = colorBackground
        pygame.display.set_icon(get_icon_surf())
        # events
        self.inputevents = [inputbox_filled]
        self.events = pygame.event.get()
        # sprites
        self.group = pygame.sprite.LayeredUpdates()
        # collisions check
        self.button_collision = pygame.sprite.Group()
        self.inputbox_collision = pygame.sprite.Group()
        # clock
        self.clock = pygame.time.Clock()
        # other
        self.bksp_timer = pygame.time.get_ticks()
        self.bksp_down = False

        self.loop = True

    def check_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                self.leave_game()
            elif event.type == MOUSEBUTTONDOWN:
                inputbox.active = inputbox.rect.collidepoint(event.pos)
            elif event.type == KEYDOWN:
                if inputbox.active:
                    if event.key == K_ESCAPE:
                        inputbox.text = ''
                    elif event.key == K_BACKSPACE:
                        inputbox.text = inputbox.text[:-1]
                        pygame.time.set_timer(BKSP_DOWN, 300, 1)
                        self.bksp_down = True
                    else:
                        inputbox.text += event.unicode
            elif event.type == KEYUP:
                if inputbox.active and event.key == K_BACKSPACE:
                    self.bksp_down = False
            elif event.type == BKSP_DOWN and self.bksp_down and inputbox.active:
                inputbox.text = ''
        for event in self.inputevents:
            event()

    def get_center(self):
        return self.display.get_width() / 2, self.display.get_height() / 2

    def clear_collision_boxes(self):
        self.button_collision.empty()
        self.inputbox_collision.empty()

    def cursor_by_context(self):
        cursor = SYSTEM_CURSOR_ARROW
        if len(self.button_collision) > 0:
            cursor = SYSTEM_CURSOR_HAND
        elif len(self.inputbox_collision) > 0:
            cursor = SYSTEM_CURSOR_IBEAM
        pygame.mouse.set_cursor(cursor)

    def leave_game(self):
        self.loop = False

    def quit(self):
        self.loop = False

    def run(self):
        while self.loop:
            # self.clock.tick(30)
            self.display.fill(self.bg_color)
            self.cursor_by_context()
            self.check_events()
            self.group.update()
            self.group.draw(self.display)
            pygame.draw.rect(self.display, '#414141', [0, 0, display_w, display_h], 1)
            pygame.display.flip()
        pygame.quit()


# UI ###################################################################################################################
class Button(pygame.sprite.Sprite):
    def __init__(
            self,
            text,
            on_click=lambda: None,
            width=150,
            color=colorButton,
            color_hovered=colorButtonHovered,
            color_text=colorButtonText,
            color_text_hovered=colorButtonTextHovered,
            border_radius=8):
        super().__init__()
        # properties
        self.width = width
        self.image = pygame.Surface((self.width, 40))
        self.rect = self.image.get_rect()
        self.border_radius = border_radius
        self.on_click = on_click
        # color
        self.color = color
        self.color_hovered = color_hovered
        self.cur_color = self.color
        # text
        self.text = text
        self.font = pygame.font.SysFont(default_font, 24)
        self.font.set_bold(False)
        self.text_color_idle = color_text
        self.text_color_hovered = color_text_hovered
        self.text_color = self.text_color_idle

    def check_input(self):
        self.cur_color = self.color
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            app.button_collision.remove(self)
            self.text_color = self.text_color_idle
        else:
            for event in app.events:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.on_click()
                    return
            app.button_collision.add(self)
            self.text_color = self.text_color_hovered
            self.cur_color = self.color_hovered

    def draw_button(self):
        self.image.fill(app.bg_color)
        # box
        pygame.draw.rect(self.image, self.cur_color, (0, 0, self.width, 40), 0, self.border_radius)
        # text
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=(self.width / 2, 20))
        self.image.blit(text, text_rect)

    def update(self):
        self.check_input()
        self.draw_button()


class InputBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((400, 50))
        self.rect = self.image.get_rect()
        self.active = False
        # Text
        self.font = pygame.font.SysFont(default_font, 28)
        self.text = ''
        # Border
        self.border_size = 3
        self.color_active = colorInputboxActive
        self.color_passive = (43, 43, 43)
        # Innerbox
        self.innerbox = pygame.Surface((self.rect.w - self.border_size * 2,
                                        self.rect.h - self.border_size * 2))
        # caret
        self.caret = self.Caret(self.font)

    def update(self):
        self.hovered_check()
        if self.active:
            self.image.fill(self.color_active)
        else:
            self.image.fill(self.color_passive)
        self.update_innerbox()
        self.image.blit(self.innerbox, 2 * [self.border_size])

    def update_innerbox(self):
        self.innerbox.fill(Color('white'))
        # Text
        if self.text:
            text = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text.get_rect(midleft=(5, self.innerbox.get_height() / 2))
            if text.get_width() > self.innerbox.get_width():
                text_rect = text.get_rect(midleft=(5, self.innerbox.get_height() / 2))
                text_rect.right = self.innerbox.get_width() - 10
        else:
            text = self.font.render('Deck name', True, '#808080')
            text_rect = text.get_rect(midleft=(5, self.innerbox.get_height() / 2))
        self.innerbox.blit(text, text_rect)
        # carret
        if self.active:
            self.caret.draw(self.text, text_rect, self.innerbox)

    def hovered_check(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.active:
                app.button_collision.remove(self)
                app.inputbox_collision.add(self)
            else:
                app.inputbox_collision.remove(self)
                app.button_collision.add(self)
        else:
            app.button_collision.remove(self)
            app.inputbox_collision.remove(self)

    class Caret:
        def __init__(self, font):
            self.font = font

        def draw(self, text, text_rect, box):
            image = self.font.render('|', True, 'black')
            image.set_alpha(self.get_wave_alpha())
            rect = image.get_rect(topleft=(0, 5))
            if text:
                rect.left = text_rect.right - 5
            box.blit(image, rect)

        @staticmethod
        def get_wave_alpha():
            if sin(pygame.time.get_ticks() * 0.01) > 0:
                return 255
            return 0


class LoadingBar(pygame.sprite.Sprite):

    def __init__(self,
                 width=560,
                 height=80,
                 color=(0, 255, 0),
                 bg_color=(65, 65, 65),
                 text_method='',
                 text_prefix='',
                 text_suffix='',
                 text_size=32,
                 text_pos='',
                 border_size=0,
                 grow_vel=0,
                 on_end=lambda: None,
                 max_items=1):

        super().__init__()

        # properties
        self.color = color
        self.bg_color = bg_color
        self.border_size = border_size
        self.grow_vel = grow_vel

        # bg
        self.image = pygame.Surface((width, height))
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect()

        # loading bar
        self.width = .01
        self.max_width = width - 2 * self.border_size
        self.height = height - 2 * self.border_size

        # text
        if text_method:
            self.font = pygame.font.SysFont(default_font, text_size)
            if text_method == 'percentage':
                self.text = self.get_percent
            elif text_method == 'item':
                self.max_items = max_items
                self.text = self.get_items_proportion
            if not text_pos or text_pos == 'center':
                self.blit_text = self.text_centered
        else:
            self.blit_text = lambda: None
        self.text_prefix = text_prefix
        self.text_suffix = text_suffix

        self.on_end = on_end

    def update(self):
        self.image.fill(self.bg_color)
        # bar
        if self.width < self.max_width:
            self.width += self.grow_vel
        else:
            self.width = self.max_width
            self.on_end()
        pygame.draw.rect(self.image, self.color, (self.border_size,
                                                  self.border_size,
                                                  self.width,
                                                  self.height))

        # texts
        self.blit_text()

    def add_percent(self, percent: float):
        self.width += self.max_width * percent

    def get_percent(self):
        return '{:.1%}'.format(self.width / self.max_width)

    def get_items_proportion(self):
        return '{}/{}'.format(round(self.width / self.max_width * self.max_items), self.max_items)

    def text_centered(self):
        text = '{} {} {}'.format(self.text_prefix, self.text(), self.text_suffix)
        text_surf = self.font.render(text, True, Color('white'))
        text_rect = text_surf.get_rect(center=(self.max_width / 2, self.image.get_height() / 2))
        self.image.blit(text_surf, text_rect)


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size=30, color=colorText):
        super().__init__()
        font = pygame.font.SysFont(default_font, size)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()


class WarningText(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont(default_font, 28)
        self.image = self.font.render('Deck not found!', True, (255, 0, 0))
        self.rect = self.image.get_rect(midbottom=inputbox.rect.midtop)
        self.rect.bottom -= 5
        self.alpha = 255

    def update(self, fadeout_vel=0.1):
        if self.alpha <= 0:
            self.kill()
        self.image.set_alpha(self.alpha)
        self.alpha -= fadeout_vel


########################################################################################################################


# Utils ################################################################################################################
def call_download_ui():
    global download_mode
    download_mode = 1
    app.group.remove(*uiInput)
    app.group.add(*uiDownload[:-2])
    app.clear_collision_boxes()


def call_input_ui():
    global download_mode
    download_mode = 0
    app.group.remove(*uiDownload)
    app.group.add(*uiInput[:-1])
    app.clear_collision_boxes()


def check_version(text_size=17):
    try:
        cur_version = request.urlopen(
            'https://raw.githubusercontent.com/AlexsanderRST/EDOPro-HD-Pics-Downloader/main/version.txt',
        ).read(10).decode()[:-1]
        if version == cur_version:
            log.append('Version checked: updated \n')
            return Text(f'{version}', size=text_size, color='green')
        log.append(f'Version checked: outdated. Update to {cur_version} \n')
        return Text(f'{version} (outdated)', size=text_size, color='red')
    except exceptions as e:
        log.append(f'Version not checked due {e}\n')
        return Text(f'offline', size=text_size, color='red')


def download():
    if threading.active_count() == 1 and not download_paused:
        download_complete()


def download_threaded(c, accr, deck_len):
    """Downloads a card pics and spawn a new thread"""
    global counter
    if c < len(deck):
        card_id = deck[c]
        try:
            request.urlretrieve(f'{db_url}{card_id}.jpg', f'{pics_dir}{card_id}{pics_ext}')
            log.append(f'{card_id} downloaded [{c + 1}/{len(deck)}]\n')
        except exceptions as e:
            log.append(f'Pass at {card_id} due {e}\n')
        download_bar.add_percent(1 / deck_len)
        counter += 1
        if c + accr < len(deck) and not download_paused:
            thread_args = (c + accr, accr, deck_len)
            thread = threading.Thread(target=download_threaded, args=thread_args)
            thread.start()


def download_setup(deck_name=''):
    global deck, db_url, pics_dir, pics_ext
    log.append('Download setup initialized...\n')

    # set deck
    if deck_name not in ('newcards', 'allcards', 'allfields'):
        deck_name = inputbox.text
    else:
        url = 'https://raw.githubusercontent.com/AlexsanderRST/edopro-hd-cards-downloader/main/'
        url += f'{deck_name}.ydk'
        try:
            request.urlretrieve(url, f'deck/{deck_name}.ydk')
            log.append(f'{deck_name}.ydk downloaded from repository \n')
        except exceptions as e:
            log.append(f'{deck_name}.ydk not downloaded: {e}\n')
            return
    deck = ydk_to_list(deck_name)

    # set download
    if not deck:
        app.group.add(WarningText())
        log.append(f'{deck_name}.ydk not found \n')

    else:
        if deck_name == 'allfields':
            db_url = 'https://storage.googleapis.com/ygoprodeck.com/pics_artgame/'
            pics_dir = 'pics/field/'
            pics_ext = '.png'
        else:
            db_url = 'https://storage.googleapis.com/ygoprodeck.com/pics/'
            pics_dir = 'pics/'
            pics_ext = '.jpg'
        app.inputevents.append(download)
        call_download_ui()
        inputbox.text = ''
        download_bar.max_items = len(deck)

        # threads setup
        for i in range(threads):
            thread_args = (counter + i, threads, len(deck))
            thread = threading.Thread(target=download_threaded, args=thread_args)
            thread.start()

        log.append(f'Download setup done. Downloading {deck_name}.ydk...\n')


def download_complete(canceled=False):
    global deck, counter
    # resets
    app.inputevents = app.inputevents[:-1]
    deck, counter = [], 0
    download_bar.width = .1
    # checks the reason of download completing
    if not canceled:
        app.group.remove(*uiDownload[:-2])
        app.group.add(textDownloadDone, buttonContinue)
        log.append('Download completed \n')
    else:
        download_unpause()
        call_input_ui()
        log.append('Download canceled \n')


def download_pause():
    global download_paused
    app.group.remove(buttonDnldPause)
    app.group.add(buttonDlndContinue)
    app.clear_collision_boxes()
    download_paused = True
    log.append('Download paused \n')


def download_unpause():
    global download_paused
    # ui changes
    app.group.remove(buttonDlndContinue)
    app.group.add(buttonDnldPause)
    app.clear_collision_boxes()
    # restart download
    for i in range(threads):
        thread_args = ((counter - threads) + i, threads, len(deck))
        thread = threading.Thread(target=download_threaded, args=thread_args)
        thread.start()
    download_paused = False
    log.append('Download unpaused \n')


def get_icon_surf(size=26):
    surf = pygame.Surface((32, 32), SRCALPHA)
    # body
    pygame.draw.rect(surf, '#a55127', [5, 0, 22, 32])
    pygame.draw.rect(surf, '#e6cabe', [6, 20, 20, 11])
    pygame.draw.rect(surf, '#000000', [6, 4, 20, 15])
    # text
    font = pygame.font.SysFont(default_font, 11)
    font.set_bold(True)
    text = font.render('HD', True, 'yellow')
    surf.blit(text, (7, 6))
    surf = pygame.transform.smoothscale(surf, [size] * 2)
    return surf


def inputbox_filled():
    if not download_mode:
        if inputbox.text:
            app.group.remove(buttonAllCards, buttonAllFields, buttonNewCards)
            app.group.add(buttonDownload)
        else:
            app.group.remove(buttonDownload)
            app.group.add(buttonAllCards, buttonAllFields, buttonNewCards)


def open_repo_url():
    open_url('https://github.com/AlexsanderRST/EDOPro-HD-Pics-Downloader')


def write_log():
    try:
        with open('HD Pics Downloader log.txt', 'w') as fp:
            fp.write(''.join(log))
    except PermissionError:
        return


def ydk_to_list(deck_name):
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


########################################################################################################################


if __name__ == '__main__':
    display_w, display_h = 480, 305
    app = App()

    # positioning
    btn_exit_h = 40
    spacing = 6

    # errors
    exceptions = (error.URLError, error.HTTPError, ConnectionResetError, FileNotFoundError, OSError)

    # download states
    counter = 0
    deck = []
    download_mode = 0
    download_paused = False
    db_url = ''
    pics_dir = ''
    pics_ext = ''

    # log
    log = []

    # threads (NOT CPU ones) - the more the faster, but heavy memory cost
    threads = 20

    # Input Box
    inputbox = InputBox()

    # Buttons
    buttonAllCards = Button('All cards', lambda: download_setup('allcards'))
    buttonAllFields = Button('All fields', lambda: download_setup('allfields'))
    buttonContinue = Button('Continue', call_input_ui)
    buttonGit = Button('Git', open_repo_url, width=75)
    buttonDownload = Button('Download', download_setup)
    buttonMinimize = Button('_', pygame.display.iconify, 37, colorBackground, '#595959', '#414141', border_radius=0)
    buttonExit = Button('X', app.quit, 37, colorBackground, '#e50000', '#414141', border_radius=0)
    buttonNewCards = Button('New cards', lambda: download_setup('newcards'))
    buttonDnldPause = Button('Pause', on_click=download_pause)
    buttonDlndContinue = Button('Continue', on_click=download_unpause)
    buttonDlndCancel = Button('Cancel', on_click=lambda: download_complete(canceled=True))

    # Texts
    textYdk = Text('.ydk', size=26, color='darkgray')
    textDownloadDone = Text('Download completed!', size=26, color='green')
    textName = Text('EDOPro HD Pics Downloader', size=20, color='#595959')
    textVersion = check_version()

    # Bar
    download_bar = LoadingBar(460, 60, (56, 98, 150), border_size=3, text_method='item')

    # others
    icon_sprite = pygame.sprite.Sprite()
    icon_sprite.image = get_icon_surf()

    # Rects
    buttonNewCards.rect.topleft = spacing, btn_exit_h + spacing
    buttonAllCards.rect.midtop = display_w / 2, btn_exit_h + spacing
    buttonAllFields.rect.topright = display_w - spacing, btn_exit_h + spacing
    buttonGit.rect.bottomright = display_w - spacing, display_h - spacing
    download_bar.rect.center = display_w / 2, display_h / 2
    inputbox.rect.midleft = spacing, display_h / 2
    textYdk.rect.midleft = inputbox.rect.right + spacing, inputbox.rect.centery
    buttonDownload.rect.midtop = inputbox.rect.centerx, inputbox.rect.bottom + spacing
    textDownloadDone.rect.midbottom = display_w / 2, display_h / 2 - spacing
    buttonContinue.rect.midtop = display_w / 2, display_h / 2 + spacing
    buttonExit.rect.topright = display_w, 0
    buttonMinimize.rect.midright = buttonExit.rect.midleft
    textVersion.rect.bottomleft = spacing, display_h - spacing
    icon_sprite.rect = icon_sprite.image.get_rect(midleft=(spacing, buttonExit.rect.centery))
    textName.rect.midleft = icon_sprite.rect.right + spacing, buttonExit.rect.centery
    buttonDnldPause.rect.topright = download_bar.rect.centerx - spacing, download_bar.rect.bottom + spacing
    buttonDlndCancel.rect.midleft = download_bar.rect.centerx + spacing, buttonDnldPause.rect.centery
    buttonDlndContinue.rect.center = buttonDnldPause.rect.center

    # Lists
    uiInput = [inputbox, textYdk, buttonAllCards, buttonAllFields, buttonNewCards, buttonGit, buttonDownload]
    uiDownload = [download_bar, buttonDnldPause, buttonDlndCancel, textDownloadDone, buttonContinue]
    uiFixed = [buttonMinimize, buttonExit, textName, textVersion, icon_sprite]
    app.group.add(*uiFixed, *uiInput[:-1])

    pygame.time.wait(100)

    app.run()

    # write log
    log.append('Program exited \n')
    write_log()
