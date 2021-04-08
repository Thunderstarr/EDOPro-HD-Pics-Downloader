"""
Created by Alexsander Rosante
"""

import pygame
from pygame.locals import *
from urllib import request, error
import webbrowser
import os

version = '2.0'

font_directory = 'font/'  # No uses
icon_directory = 'img/icon/'  # No uses

# Resources
request.urlretrieve('https://i.ibb.co/ryjynsw/mini-icon.png', 'hdcd_icon.png')
pygame.time.wait(1)


class App:

    def __init__(self):
        pygame.init()
        # display
        self.display = pygame.display.set_mode((480, 260))
        self.bg_color = (178, 97, 58)
        pygame.display.set_caption('EDOPRO HD Cards Downloader ' + version)
        pygame.display.set_icon(pygame.image.load('hdcd_icon.png'))
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

    def run(self):
        while self.loop:
            self.display.fill(self.bg_color)
            self.cursor_by_context()
            self.event_check()
            self.group.update()
            self.group.draw(self.display)
            pygame.display.flip()
            self.clock.tick(60)
        os.remove('hdcd_icon.png')
        pygame.quit()

    def event_check(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                self.leave()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.leave()
        for event in self.inputevents:
            event()

    def leave(self):
        self.loop = False

    def cursor_by_context(self):
        if len(self.button_collision) > 0:
            cursor = SYSTEM_CURSOR_HAND
        elif len(self.inputbox_collision) > 0:
            cursor = SYSTEM_CURSOR_IBEAM
        else:
            cursor = SYSTEM_CURSOR_ARROW
        pygame.mouse.set_cursor(cursor)

    def get_display_center(self):
        return self.display.get_width() / 2, self.display.get_height() / 2

    def clear_collision_boxes(self):
        self.button_collision.empty()
        self.inputbox_collision.empty()


class LoadingBar(pygame.sprite.Sprite):

    def __init__(self,
                 width=560,
                 height=80,
                 color=(0, 255, 0),
                 bg_color=(65, 65, 65),
                 border_size=0,
                 grow_vel=0,
                 end_command=lambda: False,
                 text_method='',
                 text_prefix='',
                 text_suffix='',
                 text_size=32,
                 max_items=1,
                 text_pos=''):

        pygame.sprite.Sprite.__init__(self)

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
        return '{}/{}'.format(round(self.width/self.max_width*self.max_items), self.max_items)

    def text_centered(self):
        text = '{} {} {}'.format(self.text_prefix, self.text(), self.text_suffix)
        text_surf = self.font.render(text, True, Color('white'))
        text_rect = text_surf.get_rect(center=(self.max_width / 2, self.image.get_height() / 2))
        self.image.blit(text_surf, text_rect)


class Button(pygame.sprite.Sprite):

    def __init__(self,
                 game,
                 width=0,
                 height=0,
                 depth=10,
                 color=(178, 34, 34),
                 color_above=(193, 78, 78),
                 color_pressed=(142, 27, 27),
                 color_below=(65, 65, 65),
                 text='',
                 text_size=0,
                 text_color=(255, 255, 255),
                 text_font='',
                 text_sysfont='',
                 text_at_left=False,
                 text_at_right=False,
                 aatext=True,
                 icon='',
                 icon_size=0,
                 icon_fit=False,
                 icon_centered=True,
                 icon_at_left=True,
                 command=lambda: None,
                 interactive=True):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.command = command

        if width <= 0:
            width = 240
        if height <= 0:
            height = 60
        border_dist = 5

        # transparent bg
        self.image = pygame.Surface((width, height + depth), SRCALPHA)
        self.rect = self.image.get_rect()

        # idle surf
        front = pygame.Surface((width, height))
        front.fill(color)
        front_rect = front.get_rect(top=depth)
        above = pygame.Surface((width, depth))
        above.fill(color_above)
        above_rect = above.get_rect()
        self.idle_surf = self.image.copy()
        self.idle_surf.blit(front, front_rect)
        self.idle_surf.blit(above, above_rect)

        # pushed surf
        front.fill(color_pressed)
        front_rect.top = 0
        below = pygame.Surface((width, depth))
        below.fill(color_below)
        below_rect = below.get_rect(top=height)
        self.pressed_surf = self.image.copy()
        self.pressed_surf.blit(front, front_rect)
        self.pressed_surf.blit(below, below_rect)

        # text and icon
        text_surf = pygame.Surface((1, 1))
        if text:
            # create text surf
            if not text_size:
                text_size = round(8 / 15 * height)
            # font load
            font = pygame.font.SysFont('Arial', text_size)
            if text_font:
                try:
                    font = pygame.font.Font('{0}{1}.ttf'.format(font_directory, text_font), text_size)
                except FileNotFoundError:
                    pass
            elif text_sysfont:
                font = pygame.font.SysFont(text_sysfont, text_size)

            text_surf = font.render(text, aatext, text_color)

        if icon:
            # create icon surf
            try:
                icon_surf = pygame.image.load('{0}{1}.png'.format(icon_directory, icon))
            except FileNotFoundError:
                icon_surf = pygame.Surface((10, 10), SRCALPHA)
            # resize icon surf to fit at button and create it's rect
            if not icon_size:
                icon_fit = True
            if icon_fit:
                if width > height:
                    icon_size = round(height - 2 * border_dist)
                else:
                    icon_size = round(width - 2 * border_dist)
            icon_surf = pygame.transform.smoothscale(icon_surf.copy(),
                                                     [icon_size for _ in range(2)])
            # icon_rect
            icon_rect = icon_surf.get_rect()

            if text:
                # resize text surf, if needed, to fit at button with icon surf
                text_size = width - icon_size - 3 * border_dist
                if text_surf.get_width() > text_size:
                    text_surf = pygame.transform.scale(text_surf.copy(),
                                                       (text_size, text_surf.get_height()))
                # text_rect
                text_rect = text_surf.get_rect()
                # icon and text position set
                for j in ((self.idle_surf, depth), (self.pressed_surf, 0)):
                    front_rect.top = j[1]
                    if icon_at_left:
                        icon_rect.left = border_dist
                        text_rect.centerx = width - text_size / 2 - border_dist
                    else:
                        icon_rect.right = width - border_dist
                        text_rect.centerx = text_size / 2 + border_dist
                    icon_rect.centery = front_rect.centery
                    text_rect.centery = front_rect.centery
                    j[0].blit(icon_surf, icon_rect)
                    j[0].blit(text_surf, text_rect)
            else:
                # icon surf position set
                for j in ((self.idle_surf, depth), (self.pressed_surf, 0)):
                    front_rect.top = j[1]
                    if icon_centered:
                        icon_rect.centerx = front_rect.centerx
                    elif icon_at_left:
                        icon_rect.left = border_dist
                    else:
                        icon_rect.right = width - border_dist
                    icon_rect.centery = front_rect.centery
                    j[0].blit(icon_surf, icon_rect)

        elif text:
            # resize text surf, if needed
            text_size = width - 2 * border_dist
            if text_surf.get_width() > text_size:
                text_surf = pygame.transform.scale(text_surf.copy(),
                                                   (text_size, text_surf.get_height()))
            # text rect
            text_rect = text_surf.get_rect()
            # text surf position set
            for j in ((self.idle_surf, depth), (self.pressed_surf, 0)):
                front_rect.top = j[1]
                if text_at_left:
                    text_rect.left = border_dist
                elif text_at_right:
                    text_rect.right = front_rect.right - border_dist
                else:
                    text_rect.centerx = front_rect.centerx
                text_rect.centery = front_rect.centery
                j[0].blit(text_surf, text_rect)

        # interaction
        self.interaction = lambda: None
        if interactive:
            self.interaction = self.interactive
            self.game.button_collision = pygame.sprite.Group()

        self.image = self.idle_surf.copy()

    def update(self):
        self.interaction()

    def interactive(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.game.button_collision.add(self)
            for event in self.game.events:
                if event.type == MOUSEBUTTONDOWN:
                    self.image = self.pressed_surf.copy()
                elif event.type == MOUSEBUTTONUP:
                    self.command()
                    self.image = self.idle_surf.copy()
        else:
            self.image = self.idle_surf.copy()
            self.game.button_collision.remove(self)


class InputBox(pygame.sprite.Sprite):

    def __init__(self,
                 game,
                 width=240,
                 height=60,
                 inputext_color=(0, 0, 0),
                 inputbox_color=(255, 255, 255),
                 border_size=3,
                 border_color=(128, 128, 128),
                 previewtext='',
                 password_mode=False):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        # configs
        self.height = height
        self.border_color = border_color
        self.password_mode = password_mode
        self.game.inputbox_collision = pygame.sprite.Group()

        # bg
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()

        # box
        self.box = pygame.Surface((width - 2 * border_size,
                                   height - 2 * border_size))
        self.box.fill(inputbox_color)
        self.box_rect = self.box.get_rect(left=border_size,
                                          centery=height / 2)

        # input text
        self.font = pygame.font.SysFont('Consolas', 32)
        self.text = ''
        self.blitable_text = str(self.text)

        # caret
        self.caret = self.Carret(self.font.get_height(), inputext_color, inputbox_color)

        # preview text
        self.previewtext = self.font.render(previewtext, True, inputext_color)
        self.previewtext.set_alpha(128)

    def update(self):
        self.image.fill(self.border_color)
        self.input_check()
        box = self.box.copy()

        # text
        text = self.font.render(self.blitable_text, True, (0, 0, 0))
        if text.get_width() < box.get_width():
            text_rect = text.get_rect(midleft=(5, box.get_height() / 2))
        else:
            text_rect = text.get_rect(midright=(box.get_width() - 5, box.get_height() / 2))
        if self.text:
            box.blit(text, text_rect)
        else:
            box.blit(self.previewtext, text_rect)

        # caret
        self.caret.rect.midleft = text_rect.midright
        self.caret.update()
        box.blit(self.caret.image, self.caret.rect)

        self.image.blit(box, self.box_rect)

    def input_check(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.game.inputbox_collision.add(self)
            for event in self.game.events:
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
            if self.password_mode:
                self.blitable_text = len(self.text) * '*'
            else:
                self.blitable_text = str(self.text)
        else:
            self.game.inputbox_collision.remove(self)

    def clean(self):
        self.text = ''
        self.blitable_text = str(self.text)

    class Carret(pygame.sprite.Sprite):
        def __init__(self, font_height, inputext_color, inputbox_color):
            pygame.sprite.Sprite.__init__(self)
            self.visible_color, self.hidden_color = inputext_color, inputbox_color
            self.image = pygame.Surface((3, font_height))
            self.rect = self.image.get_rect()
            self.frame = 0

        def update(self, blinkspeed=1):
            if self.frame < 30:
                self.image.fill(self.visible_color)
            elif self.frame < 60:
                self.image.fill(self.hidden_color)
            else:
                self.frame = 0
            self.frame += blinkspeed


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


    @inputevent
    def pressed_key_outside():
        if not download_mode:
            for event in app.events:
                if event.type == KEYDOWN:
                    pygame.mouse.set_pos((inputbox.rect.left + 5, inputbox.rect.centery))


    def call_download_ui():
        global download_mode
        download_mode = 1
        app.group.remove(*input_ui)
        app.group.add(*download_ui[:-2])
        app.clear_collision_boxes()


    def call_input_ui():
        global download_mode
        download_mode = 0
        app.group.remove(*download_ui)
        app.group.add(*input_ui[:-1])
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
            inputbox.text = ''
        deck = ydk_to_list(deck_name)
        if deck:
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
            pass


    def download(database_url, pics_folder, pics_extension):
        """Receives a deck list to download cards pics from database"""
        global counter
        download_bar.max_items = len(deck)
        if counter < len(deck):
            try:
                request.urlretrieve(database_url + deck[counter] + '.jpg',
                                    pics_folder + deck[counter] + pics_extension)
            except error.HTTPError or ConnectionResetError:
                print(Exception)
            download_bar.add_percent(1 / len(deck))
            counter += 1
        else:
            pass


    def complete_download():
        global deck, counter
        # change ui elements
        app.group.remove(*download_ui[:-2])
        app.group.add(txt_download_done, btn_continue)
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
    btns_default = {'game': app, 'width': 160, 'height': 40, 'depth': 6, 'color': (102, 55, 33),
                    'color_above': (253, 230, 138), 'color_pressed': (102, 55, 33), 'text_sysfont': 'Consolas'}
    txts_default = {'game': app, 'color': (102, 55, 33), 'text_sysfont': 'Consolas', 'interactive': False}

    # Objects
    # General UI:
    btn_git = Button(app,
                     width=40,
                     height=40,
                     depth=4,
                     text='Git',
                     command=lambda: webbrowser.open('http://tinyurl.com/yufb2ucj'))
    # rects
    '''txt_devname.rect.bottomright = btn_git.rect.bottomleft'''
    btn_git.rect.bottomright = app.display.get_width() - 5, app.display.get_height() - 5
    # ui list
    '''general_ui = [txt_devname, btn_git]'''
    general_ui = [btn_git]

    # Input UI:
    inputbox = InputBox(app, 400, 50, previewtext='Deck name')
    btn_allcards = Button(text='All Cards', command=lambda: download_setup('allcards'), **btns_default)
    btn_allfields = Button(text='All Fields', command=lambda: download_setup('allfields'), **btns_default)
    btn_download = Button(text='Download', command=download_setup, **btns_default)
    btn_newcards = Button(text='New Cards', command=lambda: download_setup('newcards'), **btns_default)
    txt_ydk = Button(
        game=app,
        width=70,
        height=inputbox.image.get_height(),
        depth=0,
        text='.ydk',
        text_sysfont='Consolas',
        color=app.bg_color,
        interactive=False
    )
    # rects
    inputbox.rect.midleft = 5, app.get_display_center()[1]
    btn_download.rect.centerx = app.get_display_center()[0]
    btn_download.rect.top = inputbox.rect.bottom + 8
    txt_ydk.rect.midleft = inputbox.rect.midright
    last_right = 0
    for i in (btn_newcards, btn_allcards, btn_allfields):
        i.rect.left = last_right
        last_right = i.rect.right + 3
    # ui list
    input_ui = [inputbox, txt_ydk, btn_allcards, btn_allfields, btn_newcards, btn_download]

    # Download UI:
    download_bar = LoadingBar(460, 60, (29, 158, 116), border_size=3, text_method='item',
                              end_command=complete_download)
    btn_continue = Button(text='Continue', command=call_input_ui, **btns_default)
    txt_download_done = Button(app, width=480, depth=0, text='Download Completed!', text_sysfont='Consolas',
                               color=app.bg_color, interactive=False)
    # rects
    download_bar.rect.center = app.get_display_center()
    txt_download_done.rect.midbottom = app.display.get_width() / 2, app.display.get_height() / 2 - 10
    btn_continue.rect.midtop = txt_download_done.rect.centerx, txt_download_done.rect.bottom + 20
    # ui list
    download_ui = [download_bar, txt_download_done, btn_continue]
    # }

    app.group.add(*general_ui, *input_ui[:-1])

    app.run()
