class Idle:
    def __init__(self):
        pass

    def update(self, player):
        """Check for any input or transitions to other states."""
        # The Idle state doesn't need to perform any logic itself.
        # It just waits for input to trigger another state.
        pass

    def enter(self, player):
        """Optional: Actions to perform when entering the Idle state."""
        # For example, reset some player flags or set an idle animation.
        player.is_attacking = False
        # Optionally, play idle animation
        player.animation_manager.play_animation("Idle_player", player.surface, (player.rect.x, player.rect.y))

    def exit(self, player):
        """Optional: Actions to perform when leaving the Idle state."""
        # You could reset some flags or stop the idle animation here, if needed.
        pass
