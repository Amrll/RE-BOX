from data.components.enemy.states.idle import Idle


class AttackRight:
    def __init__(self):
        pass

    def update(self, player):
        player.is_attacking = True
        player.state_machine.change_state(Idle())