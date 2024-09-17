"""
State for the Title scene.
"""

import pygame as pg
from .. import prepare, state_machine, tools
from ..controls import DEFAULT_CONTROLS

SCROLL_SPEED = 2
DELAY_UNTIL_SCROLL = 10000  # Miliseconds.


class Title(state_machine._State):
    """This State is updated while our game shows the title screen."""
    def __init__(self):
        state_machine._State.__init__(self)
        self.ground = prepare.GFX["misc"]["title_screen"]
        self.elements = self.make_elements()
        self.timer = None
        self.scrolling = False

    def startup(self, now, persistant):
        self.persist = persistant
        self.start_time = now
        self.timer = tools.Timer(DELAY_UNTIL_SCROLL, 1)
        self.timer.check_tick(now)
        self.scrolling = False
        self.elements = self.make_elements()

    def make_elements(self):
        group = pg.sprite.LayeredUpdates()

        # Create sprite instances
        any_key = AnyKey()
        title_image = TitleImage()
        trade_mark = TradeMark()

        # Add sprites to the group with specific layers
        group.add(any_key, layer=1)
        group.add(title_image, layer=1)
        group.add(trade_mark, layer=1)

        return group

    def update(self, keys, now):
        """Updates the title screen."""
        self.now = now
        self.elements.update(now)

    def draw(self, surface, interpolate):
        surface.blit(self.ground, (0, 0))
        # Then, draw other elements (title words, press any key, etc.)
        self.elements.draw(surface)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == DEFAULT_CONTROLS["punch_left"] or event.key == DEFAULT_CONTROLS["punch_right"]:
                self.next = "SELECT"
                self.done = True


class TitleImage(tools._BaseSprite):
    def __init__(self, *groups):
        # Load the title image
        self.image = prepare.GFX["misc"]["titlewords"]

        # Initialize the sprite
        tools._BaseSprite.__init__(self, (0, 0), self.image.get_size(), *groups)

        # Center the title image on the screen
        self.rect = self.image.get_rect(center=prepare.SCREEN_RECT.center)
        self.exact_position = list(self.rect.topleft)

    def update(self, now):
        # Update the sprite position
        self.rect.topleft = self.exact_position

        # Kill the sprite if it moves off-screen
        if not self.rect.colliderect(prepare.SCREEN_RECT):
            self.kill()


class AnyKey(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        pg.sprite.Sprite.__init__(self, *groups)
        self.raw_image = render_font("Fixedsys500c", 40,
                                     "[Punch to start]", (251, 251, 251))
        self.null_image = pg.Surface((1, 1)).convert_alpha()
        self.null_image.fill((0, 0, 0, 0))
        self.image = self.raw_image
        center = (prepare.SCREEN_RECT.centerx, 680)
        self.rect = self.image.get_rect(center=center)
        self.blink = False
        self.timer = tools.Timer(400)

    def update(self, now, *args):
        if self.timer.check_tick(now):
            self.blink = not self.blink
        self.image = self.raw_image if self.blink else self.null_image


class TradeMark(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.raw_image = render_font("Fixedsys500c", 30,
                                     "© Masterals 2024. All Rights Reserved", (255, 255, 0))
        self.image = self.raw_image
        center = (prepare.SCREEN_RECT.centerx, 900)
        self.rect = self.image.get_rect(center=center)

def render_font(font, size, msg, color=(255, 255, 255)):
    """
    Takes the name of a loaded font, the size, and the color and returns
    a rendered surface of the msg given.
    """
    selected_font = pg.font.Font(prepare.FONTS[font], size)
    return selected_font.render(msg, 1, color)
