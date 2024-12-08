"""
This module contains the fundamental Control class.
Also contained here are resource loading functions.
"""
import os
import pygame as pg
from . import state_machine
from .controls import ControlManager


TIME_PER_UPDATE = 16.0  # Milliseconds


class Control:
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.fps_visible = True
        self.now = 0.0
        self.keys = pg.key.get_pressed()
        self.state_machine = state_machine.StateMachine()
        self.control_manager = ControlManager()  # Initialize ControlManager

    def update(self):
        """Updates the currently active state."""
        self.now = pg.time.get_ticks()
        self.state_machine.update(self.keys, self.now)

    def draw(self, interpolate):
        if not self.state_machine.state.done:
            self.state_machine.draw(self.screen, interpolate)
            pg.display.update()
            self.show_fps()

    def event_loop(self):
        """Process all events and pass them down to the state_machine."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.control_manager.handle_key_event(event)  # Handle key events through ControlManager
                self.toggle_show_fps(event.key)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.state_machine.get_event(event)

    def toggle_show_fps(self, key):
        """Press f5 to turn on/off displaying the framerate in the caption."""
        if key == pg.K_F5:
            self.fps_visible = not self.fps_visible
            if not self.fps_visible:
                pg.display.set_caption(self.caption)

    def show_fps(self):
        """Display the current FPS in the window handle if fps_visible is True."""
        if self.fps_visible:
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pg.display.set_caption(with_fps)

    def main(self):
        """Main loop for the entire program. Uses a constant timestep."""
        lag = 0.0
        while not self.done:
            lag += self.clock.tick(self.fps)
            self.event_loop()
            while lag >= TIME_PER_UPDATE:
                self.update()
                lag -= TIME_PER_UPDATE
            self.draw(lag / TIME_PER_UPDATE)


class Timer:
    def __init__(self, interval, start_on_init=False):
        self.interval = interval  # Time duration in milliseconds
        self.start_time = None    # Tracks when the timer starts
        self.running = False      # Tracks if the timer is running
        if start_on_init:
            self.start(pg.time.get_ticks())

    def start(self, now=None):
        """Start the timer."""
        if now is None:
            now = pg.time.get_ticks()
        self.start_time = now
        self.running = True

    def check_tick(self, now=None):
        """Check if the timer has finished."""
        if now is None:
            now = pg.time.get_ticks()
        if self.running and (now - self.start_time >= self.interval):
            self.running = False  # Timer stops after interval
            return True
        return False

    def stop(self):
        """Manually stop the timer."""
        self.running = False
        self.start_time = None



class _BaseSprite(pg.sprite.Sprite):
    """
    A very basic base class that contains some commonly used functionality.
    """

    def __init__(self, pos, size, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.rect = pg.Rect(pos, size)
        self.exact_position = list(self.rect.topleft)
        self.old_position = self.exact_position[:]

    @property
    def frame_speed(self):
        """
        Returns the total displacement undergone in a frame. Used for the
        interpolation of the sprite's location in the draw phase.
        """
        return (self.exact_position[0] - self.old_position[0],
                self.exact_position[1] - self.old_position[1])

    def reset_position(self, value, attribute="topleft"):
        """
        Set the sprite's location variables to a new point.  The attribute
        argument can be specified to assign to a chosen attribute of the
        sprite's rect.
        """
        setattr(self.rect, attribute, value)
        self.exact_position = list(self.rect.topleft)
        self.old_position = self.exact_position[:]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def on_map_change(self):
        pass


# Resource loading functions.
def load_all_gfx(directory, colorkey=(255, 0, 255), accept=(".png", ".jpg", ".bmp")):
    """
    Load all graphics from a directory and its subdirectories.
    Handles nested directories, returning a nested dictionary structure.
    If alpha transparency is found in the image, it is converted using
    convert_alpha(). Otherwise, colorkey is applied.
    """
    graphics = {}
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isdir(full_path):
            # Recursively load graphics from subdirectories
            graphics[item] = load_all_gfx(full_path, colorkey, accept)
        else:
            # Process individual image files
            name, ext = os.path.splitext(item)
            if ext.lower() in accept:
                img = pg.image.load(full_path)
                if img.get_alpha():
                    img = img.convert_alpha()
                else:
                    img = img.convert()
                    img.set_colorkey(colorkey)
                graphics[name] = img
    return graphics


def load_all_music(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """
    Create a dictionary of paths to music files in given directory
    if their extensions are in accept.
    """
    songs = {}
    for song in os.listdir(directory):
        name, ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_fonts(directory, accept=(".ttf",)):
    """
    Create a dictionary of paths to font files in given directory
    if their extensions are in accept.
    """
    return load_all_music(directory, accept)


def load_all_sfx(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """
    Load all sfx of extensions found in accept.  Unfortunately it is
    common to need to set sfx volume on a one-by-one basis.  This must be done
    manually if necessary.
    """
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects

# Utility classes like Anim and Timer would go here, but let's focus on the structure for now.
