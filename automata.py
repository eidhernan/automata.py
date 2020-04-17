class Automaton:
    def __init__(self):
        self.states = {}
        self.state = "DEFAULT"

    def add_state(self, state):
        self.states[state.name] = state

    def set_default(self, state):
        self.states["DEFAULT"] = self.states[state]
    
    def change_state(self, state):
        self.state = state

    def __call__(self):
        self.states[self.state]()

    def register(parent, allowed_states, default=False):
        def decorator(func):
            parent.add_state(State(parent, func.__name__, allowed_states, func))
            if default:
                parent.set_default(func.__name__)
            def wrapper():
                func(parent)
            return wrapper
        return decorator

class State:
    def __init__(self, parent, name, allowed, func):
        self.parent = parent
        self.name = name
        self.allowed = allowed
        self.func = func
    def __call__(self):
        self.func(self.parent)


