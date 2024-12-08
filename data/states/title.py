"""
State for the Title scene.
"""
import threading
import time

import pygame as pg
from .. import prepare, state_machine, tools, hand_detection
from ..controls import DEFAULT_CONTROLS
from ..tools import Timer

SCROLL_SPEED = 2
DELAY_UNTIL_SCROLL = 10000  # Miliseconds.


class Title(state_machine._State):
    """This State is updated while our game shows the title screen."""

    def __init__(self):
        super().__init__()
        self.hand_detected = False  # Store detection result
        self.detecting = True  # Control detection thread
        self.gesture_lock = threading.Lock()
        self.detection_thread = threading.Thread(target=self.run_hand_detection, daemon=True)
        self.last_gesture_time = None  # Time of last detected gesture
        self.gesture_debounce_time = 1
        self.detection_thread.start()
        self.current_gesture = None

        state_machine._State.__init__(self)

        self.ground = prepare.GFX["misc"]["title_screen"]
        self.elements = self.make_elements()
        self.arena_settled = False  # To know when the arena has fully dropped in
        self.title_settled = False  # To know when the title has fully dropped in
        self.anykey_visible = False  # Track visibility of AnyKey
        self.trademark_visible = False  # Track visibility of TradeMark
        self.arena_speed = 20  # Speed for the arena dropping in
        self.title_speed = 50  # Speed for the title dropping in
        self.arena = None
        self.title_image = None
        self.any_key = None
        self.trade_mark = None
        self.anykey_delay = 800  # 2-second delay for AnyKey and TradeMark
        self.delay_timer = None  # Timer for delaying AnyKey and TradeMark appearance

    def startup(self, now, persistant):
        self.persist = persistant
        self.start_time = now
        self.scrolling = False
        self.delay_timer = tools.Timer(self.anykey_delay, False)  # Delay timer starts later
        self.elements = self.make_elements()

    def make_elements(self):
        group = pg.sprite.LayeredUpdates()

        # Create sprite instances
        any_key = AnyKey()  # Store reference for AnyKey
        title_image = TitleImage()  # Store reference to TitleImage
        trade_mark = TradeMark()  # Store reference for TradeMark
        arena = Arena()  # Store reference to Arena

        # Store references for arena, title, any_key, and trade_mark
        self.arena = arena
        self.title_image = title_image
        self.any_key = any_key
        self.trade_mark = trade_mark

        # Add sprites to the group, but initially hide AnyKey and TradeMark
        group.add(arena, layer=1)
        group.add(title_image, layer=2)

        return group

    def update(self, keys, now):
        """Updates the title screen animations."""
        self.now = now

        # First, handle the arena dropping in
        if not self.arena_settled:
            self.arena.drop_in(now, self.arena_speed)
            if self.arena.rect.bottom <= prepare.SCREEN_RECT.bottom:  # Once arena reaches the bottom
                self.arena_settled = True

        # Then, handle the title dropping in only after the arena settles
        if self.arena_settled and not self.title_settled:
            self.title_image.drop_in(now, self.title_speed)
            # Check if the title image has reached the center
            if self.title_image.rect.centery >= prepare.SCREEN_RECT.centery:
                self.title_image.rect.centery = prepare.SCREEN_RECT.centery  # Snap to center
                self.title_settled = True
                self.delay_timer.start(now)

                # Check the timer for showing AnyKey and TradeMark
        if self.title_settled and not self.anykey_visible and self.delay_timer.check_tick(now):
            self.elements.add(self.any_key, layer=2)  # Add to sprite group
            self.elements.add(self.trade_mark, layer=2)
            self.anykey_visible = True  # Mark that they're now visible

        # Update elements like blinking "Punch to start"
        self.elements.update(now)

    def run_hand_detection(self):
        while self.detecting:
            detected_gesture = hand_detection.get_detected_gesture()

            # Only update current_gesture if enough time has passed since the last update
            if detected_gesture:
                current_time = time.time()
                if self.last_gesture_time is None or current_time - self.last_gesture_time >= self.gesture_debounce_time:
                    with self.gesture_lock:
                        self.current_gesture = detected_gesture
                        self.last_gesture_time = current_time

                        if detected_gesture in ("punch_left", "punch_right"):
                            self.done = True
                            self.next = "SELECT"

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == DEFAULT_CONTROLS["punch_left"] or event.key == DEFAULT_CONTROLS["punch_right"]:
                self.done = True
                self.next = "SELECT"


    def draw(self, surface, interpolate):
        surface.blit(self.ground, (0, 0))
        self.elements.draw(surface)


class Arena(tools._BaseSprite):
    def __init__(self, *groups):
        # Load the background image
        self.image = prepare.GFX["backgrounds"]["ring1"]

        # Scale the image to fit the entire screen
        self.image = pg.transform.scale(self.image, prepare.SCREEN_RECT.size)

        # Initialize the sprite with the new size
        tools._BaseSprite.__init__(self, (0, 0), prepare.SCREEN_RECT.size, *groups)

        # Set the rect to start below the screen
        self.rect = self.image.get_rect(midtop=(prepare.SCREEN_RECT.centerx, prepare.SCREEN_RECT.height))

    def drop_in(self, now, speed):
        """Animate the arena dropping in from below."""
        if self.rect.top > 0:
            self.rect.move_ip(0, -speed)


class TitleImage(tools._BaseSprite):
    def __init__(self, *groups):
        # Load the title image
        self.image = prepare.GFX["misc"]["titlewords"]

        # Initialize the sprite with the image size
        tools._BaseSprite.__init__(self, (0, 0), self.image.get_size(), *groups)

        # Set the rect to start above the screen
        # Adjust rect so that it's centered horizontally and starts above the screen
        self.rect = self.image.get_rect(midbottom=(prepare.SCREEN_RECT.centerx, 0))

    def drop_in(self, now, speed):
        """Animate the title dropping in from above."""
        # Adjust so the title is fully centered both horizontally and vertically
        if self.rect.centery < prepare.SCREEN_RECT.centery:
            self.rect.move_ip(0, speed)
        else:
            self.rect.centery = prepare.SCREEN_RECT.centery  # Snap to center when done



class AnyKey(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.raw_image = render_font("Fixedsys500c", 40,
                                     "[Punch to start]", (251, 251, 251))
        self.null_image = pg.Surface((1, 1)).convert_alpha()
        self.null_image.fill((0, 0, 0, 0))
        self.image = self.raw_image
        center = (prepare.SCREEN_RECT.centerx, 700)
        self.rect = self.image.get_rect(center=center)
        self.blink = False
        self.timer = tools.Timer(400, True)  # Start the blinking timer

    def update(self, now, *args):
        if not self.timer.running:
            self.timer.start(now)  # Start the timer when the update is called for the first time
        if self.timer.check_tick(now):  # Ensure blinking keeps working
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
