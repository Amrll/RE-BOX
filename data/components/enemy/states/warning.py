import pygame as pg


class WarningAttack:
    def __init__(self, attack_position, duration=1500):
        self.attack_position = attack_position  # The attack position (left, middle, or right)
        self.duration = duration  # Duration of the warning phase (1 second)
        self.start_time = pg.time.get_ticks()

    def update(self, enemy):
        now = pg.time.get_ticks()
        if now - self.start_time > self.duration:
            # After the warning duration, trigger the attack
            enemy.state_machine.start_attack(self.attack_position)

    def enter(self, enemy):
        pass

    def exit(self, enemy):
        # Cleanup when exiting the warning state (not necessary for warning state, but for completeness)
        pass
