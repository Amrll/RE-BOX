import pygame as pg

from data.components.player.states.idle import Idle


class TakeDamage:
    def __init__(self, damage):
        self.duration = 200
        self.start_time = pg.time.get_ticks()
        self.damage = damage

    def update(self, player):
        now = pg.time.get_ticks()
        if now - self.start_time > self.duration:
            player.state_machine.change_state(Idle())

    def enter(self, player):
        player.health -= self.damage
        player.is_hurt = True
        player.animation_manager.play_animation("Idle_player", player.surface, (player.rect.x, player.rect.y))

    def exit(self, player):
        player.is_hurt = False