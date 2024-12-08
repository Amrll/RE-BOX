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
