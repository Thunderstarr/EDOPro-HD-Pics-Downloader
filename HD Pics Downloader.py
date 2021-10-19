"""Created by Alexsander Rosante 2021"""
import pygame
from pygame.locals import *
from urllib import request, error
import webbrowser

version = '2.1.3'

# Resources
try:
    request.urlretrieve('https://i.ibb.co/ryjynsw/mini-icon.png', 'hdcd_icon.png')
except error.HTTPError:
    pass
pygame.time.wait(1)

# Colors
BG_COLOR = (227, 227, 233)
BTN_COLOR = '#0252b1'
BTN_TXT_COLOR = '#ccdcef'
BTN_TXT_HOVERED_COLOR = (227, 227, 233)
TXT_COLOR = (40, 40, 41)
DWNLDBAR_COLOR = (56, 98, 150)


class App:
    def __init__(self):
        pygame.init()
        # display
        self.display = pygame.display.set_mode((480, 260))
        self.bg_color = BG_COLOR
        pygame.display.set_caption('EDOPRO HD Cards Downloader ' + version)
        self.set_icon()
        # events
        self.inputevents = []
        self.events = pygame.event.get()
        # sprites
        self.group = pygame.sprite.LayeredUpdates()
        # collisions check
        self.button_collision = pygame.sprite.Group()
        self.inputbox_collision = pygame.sprite.Group()
        # clock
        self.clock = pygame.time.Clock()

        self.loop = True

    def check_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                self.leave_game()
            if event.type == KEYDOWN:
                if inputbox.active:
                    if event.key == K_ESCAPE:
                        inputbox.text = ''
                    elif event.key == K_BACKSPACE:
                        inputbox.text = inputbox.text[:-1]
                    else:
                        inputbox.text += event.unicode
            if event.type == MOUSEBUTTONDOWN:
                if inputbox.rect.collidepoint(event.pos):
                    inputbox.active = True
                else:
                    inputbox.active = False
        for event in self.inputevents:
            event()

    def get_center(self):
        return self.display.get_width() / 2, self.display.get_height() / 2

    @staticmethod
    def set_icon():
        try:
            pygame.display.set_icon(pygame.image.load('hdcd_icon.png').convert_alpha())
        except FileNotFoundError:
            return

    def clear_collision_boxes(self):
        self.button_collision.empty()
        self.inputbox_collision.empty()

    def cursor_by_context(self):
        if len(self.button_collision) > 0:
            cursor = SYSTEM_CURSOR_HAND
        elif len(self.inputbox_collision) > 0:
            cursor = SYSTEM_CURSOR_IBEAM
        else:
            cursor = SYSTEM_CURSOR_ARROW
        pygame.mouse.set_cursor(cursor)

    def leave_game(self):
        self.loop = False

    def run(self):
        while self.loop:
            self.display.fill(self.bg_color)
            self.cursor_by_context()
            self.check_events()
            self.group.update()
            self.group.draw(self.display)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


class LoadingBar(pygame.sprite.Sprite):

    def __init__(self, width=560, height=80,
                 color=(0, 255, 0), bg_color=(65, 65, 65),
                 text_method='', text_prefix='', text_suffix='', text_size=32, text_pos='',
                 border_size=0, grow_vel=0, end_command=lambda: None,  max_items=1):

        super().__init__()

        # General configs
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
            self.font = pygame.font.SysFont('Consolas', text_size)
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

        self.end_command = end_command

    def update(self):
        self.image.fill(self.bg_color)
        # bar
        if self.width < self.max_width:
            self.width += self.grow_vel
        else:
            self.width = self.max_width
            self.end_command()
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


class Button(pygame.sprite.Sprite):
    def __init__(self, text, command, width=150):
        super().__init__()
        # General config
        self.width = width
        self.image = pygame.Surface((self.width, 40))
        self.rect = self.image.get_rect()
        self.border_radius = 0
        self.command = command
        # Color
        self.color = BTN_COLOR
        # Text
        self.text = text
        self.font = pygame.font.SysFont('Consolas', 21)
        self.text_color_idle = BTN_TXT_COLOR
        self.text_color_hovered = BTN_TXT_HOVERED_COLOR
        self.text_color = self.text_color_idle

    def update(self, max_radius=12, grow_vel=2):
        self.image.fill(app.bg_color)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            for event in app.events:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.command()
                        return
            app.button_collision.add(self)
            self.text_color = self.text_color_hovered
            if self.border_radius < max_radius:
                self.border_radius += grow_vel
        else:
            app.button_collision.remove(self)
            self.text_color = self.text_color_idle
            if self.border_radius > 0:
                self.border_radius -= grow_vel
        # Box
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, 40), 0, self.border_radius)
        # Text
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=(self.width / 2, 20))
        self.image.blit(text, text_rect)


class Text(pygame.sprite.Sprite):
    def __init__(self, text):
        super().__init__()
        font = pygame.font.SysFont('Consolas', 22)
        self.image = font.render(text, True, TXT_COLOR)
        self.rect = self.image.get_rect()


class WarningText(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Consolas', 23)
        self.image = self.font.render('! Deck not found !', True, (255, 0, 0))
        self.rect = self.image.get_rect(midbottom=inputbox.rect.midtop)
        self.rect.bottom -= 5
        self.alpha = 255

    def update(self, fadeout_vel=2):
        if self.alpha <= 0:
            self.kill()
        self.image.set_alpha(self.alpha)
        self.alpha -= fadeout_vel


class InputBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((400, 50))
        self.rect = self.image.get_rect()
        self.active = False
        # Text
        self.font = pygame.font.SysFont('Consolas', 30)
        self.text = ''
        # Border
        self.border_size = 3
        self.color_active = (255, 215, 0)
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
            text_rect = text.get_rect(topleft=(5, 5))
            if text.get_width() > self.innerbox.get_width():
                text_rect = text.get_rect(top=5)
                text_rect.right = self.innerbox.get_width() - 10
        else:
            text = self.font.render('Deck name', True, (128, 128, 128))
            text_rect = text.get_rect(topleft=(10, 5))
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
            self.frame = 0

        def draw(self, text, text_rect, box):
            image = self.font.render('|', True, self.color())
            rect = image.get_rect(topleft=(0, 5))
            if text:
                rect.left = text_rect.right - 5
            box.blit(image, rect)

        def color(self, blink_speed=1):
            color = Color('black')
            if 30 < self.frame <= 60:
                color = Color('white')
            elif self.frame > 60:
                self.frame = 0
            self.frame += blink_speed
            return color


if __name__ == '__main__':

    app = App()

    # Functions
    def inputevent(func):
        app.inputevents.append(func)
        return func


    @inputevent
    def inputbox_filled():
        if not download_mode:
            if inputbox.text:
                app.group.remove(btn_allcards, btn_allfields, btn_newcards)
                app.group.add(btn_download)
            else:
                app.group.remove(btn_download)
                app.group.add(btn_allcards, btn_allfields, btn_newcards)


    def call_download_ui():
        global download_mode
        download_mode = 1
        app.group.remove(*input_ui)
        app.group.remove(*general_ui)
        app.group.add(*download_ui[:-2])
        app.clear_collision_boxes()


    def call_input_ui():
        global download_mode
        download_mode = 0
        app.group.remove(*download_ui)
        app.group.add(*input_ui[:-1])
        app.group.add(*general_ui)
        app.clear_collision_boxes()


    def download_setup(mode=''):
        global deck
        if mode in ('newcards', 'allcards', 'allfields'):
            if mode == 'newcards':
                ydk_url = 'http://tinyurl.com/k598ry'
            elif mode == 'allcards':
                ydk_url = 'https://tinyurl.com/y5om2agl'
            else:
                ydk_url = 'https://tinyurl.com/y26zea99'
            request.urlretrieve(ydk_url, 'deck/' + mode + '.ydk')
            deck_name = mode
        else:
            deck_name = inputbox.text
        deck = ydk_to_list(deck_name)
        if deck:
            inputbox.text = ''
            if mode == 'allfields':
                dwnld_info = {'database_url': 'https://storage.googleapis.com/ygoprodeck.com/pics_artgame/',
                              'pics_folder': 'pics/field/',
                              'pics_extension': '.png'}
            else:
                dwnld_info = {'database_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/',
                              'pics_folder': 'pics/',
                              'pics_extension': '.jpg'}
            app.inputevents.append(lambda: download(**dwnld_info))
            call_download_ui()
        else:  # Deck not found
            app.group.add(WarningText())


    def download(database_url, pics_folder, pics_extension):
        """Receives a deck list to download cards pics from database"""
        global counter
        download_bar.max_items = len(deck)
        if counter < len(deck):
            try:
                request.urlretrieve(database_url + deck[counter] + '.jpg',
                                    pics_folder + deck[counter] + pics_extension)
            except error.HTTPError or ConnectionResetError:
                pass
            download_bar.add_percent(1 / len(deck))
            counter += 1


    def complete_download():
        global deck, counter
        # change ui elements
        app.group.remove(*download_ui[:-2])
        app.group.add(txt_dwnld_done, btn_continue)
        # resets
        app.inputevents = app.inputevents[:-1]
        deck, counter = [], 0
        download_bar.width = .1


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


    # Parameters
    deck, counter = [], 0
    download_mode = 0

    # Input Box
    inputbox = InputBox()

    # Buttons
    btn_git = Button('Git', lambda: webbrowser.open('http://tinyurl.com/yufb2ucj'), width=75)
    btn_allcards = Button('All Cards', lambda: download_setup('allcards'))
    btn_allfields = Button('All Fields', lambda: download_setup('allfields'))
    btn_download = Button('Download', download_setup)
    btn_newcards = Button('New Cards', lambda: download_setup('newcards'))
    btn_continue = Button('Continue', call_input_ui)

    # Texts
    txt_ydk = Text('.ydk')
    txt_dwnld_done = Text('Download Completed!')

    # Bar
    download_bar = LoadingBar(460, 60, (56, 98, 150), border_size=3, text_method='item',
                              end_command=complete_download)

    # Rects
    btn_git.rect.bottomright = 475, 255
    inputbox.rect.midleft = 5, 130
    btn_download.rect.midtop = 205, 163
    txt_ydk.rect.midleft = 408, 130
    btn_allcards.rect.midtop = 240, 5
    btn_newcards.rect.topright = 161, 5
    btn_allfields.rect.topleft = 319, 5
    download_bar.rect.center = 240, 130
    txt_dwnld_done.rect.midbottom = 240, 120
    btn_continue.rect.midtop = 240, 140

    # Lists
    input_ui = [inputbox, txt_ydk, btn_allcards, btn_allfields, btn_newcards, btn_download]
    download_ui = [download_bar, txt_dwnld_done, btn_continue]
    general_ui = [btn_git]
    app.group.add(*general_ui, *input_ui[:-1])

    app.run()
