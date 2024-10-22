from data.components.player.states.idle import Idle


class AttackLeft:
    def __init__(self):
        pass

    def update(self, player):
        player.is_attacking = True
        player.state_machine.change_state(Idle())
