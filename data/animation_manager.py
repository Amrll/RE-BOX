"""
This file handles the animations of the character and the enemies,
in an inefficient way ofc but it works so yhea
"""

import pygame as pg

class AnimationManager:
    def __init__(self):
        """Initialize the animation manager and load all animations."""
        self.animations = {}
        self.load_animations()

    def load_animations(self):
        """Load all animation frames and store them in the manager."""
        # Load idle_gloves animation frames
        idle_gloves_frames = [pg.image.load(f"assets/graphics/player/gloves_1/idle_frame_{i}.png") for i in range(5)]
        self.add_animation("Idle_player", idle_gloves_frames, frame_duration=100)

        punch_left_frame = [pg.image.load(f"assets/graphics/player/gloves_1/punch_left_frame_{i}.png") for i in range(1)]
        self.add_animation("Attack_left_player", punch_left_frame, frame_duration=100)

        heart_frames = [pg.image.load(f"assets/graphics/misc/heart/heart_frame_{i}.png") for i in range(6)]
        self.add_animation("Heart", heart_frames, frame_duration=100)

        """Background Animation"""
        crowd_frames = [pg.image.load(f"assets/graphics/misc/crowd_{i}.png") for i in range(2)]
        self.add_animation("crowd", crowd_frames, frame_duration=400)

        """ENEMIES ANIMATIONS"""

        # EMOJI ANIMATION
        emoji_idle = [pg.image.load(f"assets/graphics/enemies/emoji/idle_{i}.png") for i in range(2)]
        self.add_animation("emoji_idle", emoji_idle, frame_duration=1000)

        # emoji_attack = [pg.image.load(f"assets/graphics/enemies/emoji/idle_{i}.png") for i in range(1)]
        # self.add_animation("emoji_attack", emoji_attack, frame_duration=1000)

        emoji_hurt = [pg.image.load(f"assets/graphics/enemies/emoji/hurt_{i}.png") for i in range(1)]
        self.add_animation("emoji_hurt", emoji_hurt, frame_duration=1000)

        emoji_block = [pg.image.load(f"assets/graphics/enemies/emoji/block_{i}.png") for i in range(3)]
        self.add_animation("emoji_block", emoji_block, frame_duration=1000)

        # emoji_warning = [pg.image.load(f"assets/graphics/enemies/emoji/warning_{i}.jpg") for i in range(1)]
        # self.add_animation("emoji_warning", emoji_warning, frame_duration=1000)

        # Skull

        skull_idle = [pg.image.load(f"assets/graphics/enemies/skull/idle_{i}.png") for i in range(2)]
        self.add_animation("skully_idle", skull_idle, frame_duration=1000)

        skull_hurt = [pg.image.load(f"assets/graphics/enemies/skull/hurt_{i}.png") for i in range(1)]
        self.add_animation("skully_hurt", skull_hurt, frame_duration=1000)

        skull_block = [pg.image.load(f"assets/graphics/enemies/skull/block_{i}.png") for i in range(3)]
        self.add_animation("skully_block", skull_block, frame_duration=1000)



    def add_animation(self, name, frames, frame_duration):
        """Add an animation with its frames and frame duration."""
        self.animations[name] = {
            "frames": frames,
            "frame_duration": frame_duration,
            "current_frame": 0,
            "last_update": pg.time.get_ticks()
        }

    def play_animation(self, name, surface, position):
        """Play the animation with the given name on the provided surface."""
        if name in self.animations:
            animation = self.animations[name]
            now = pg.time.get_ticks()

            # Update frame based on time
            if now - animation["last_update"] > animation["frame_duration"]:
                animation["current_frame"] = (animation["current_frame"] + 1) % len(animation["frames"])
                animation["last_update"] = now

            # Get the current frame and draw it on the surface
            current_frame_image = animation["frames"][animation["current_frame"]]
            surface.blit(current_frame_image, position)
        else:
            print(f"Animation '{name}' not found.")
