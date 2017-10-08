from transitions import Machine


class AutomotiveBotStateMachine(object):
    states = ["intent_handling","plan_route","plan_group_route","ask_user_address"]

    def __init__(self):
        self.machine = Machine(model=self, states=AutomotiveBotStateMachine.states, initial='intent_handling')
        self.machine.add_transition(trigger='plan_route', source='intent_handling', dest='plan_route')
        self.machine.add_transition(trigger='route_finished', source='plan_route', dest='intent_handling')
        self.machine.add_transition(trigger='plan_group_route', source='intent_handling', dest='plan_group_route')
        self.machine.add_transition(trigger='ask_user', source='plan_group_route', dest='ask_user_address')
        self.machine.add_transition(trigger='got_address', source='ask_user_address', dest='plan_group_route')
        self.machine.add_transition(trigger='group_route_planned', source='plan_group_route', dest='intent_handling')

