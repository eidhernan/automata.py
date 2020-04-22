"""
Automata: a lightweight module that allows for easy creation of finite state machines.
"""

class Automaton:
    """
    An Automaton is a finite state machine object. It has a finite number of states, it has a dynamic size, so states can be added on the fly.
    
    Parameters: None
    
    """
    def __init__(self):
        self.states = {} # The states of the Automaton are represented by a single dictionary, in a fasion of {"state name":<state object>}.
        # The reason behind this is to allow easy lookup of states by name >>> self.states[state]
        self.state = "DEFAULT" # The current state is represented by a string. This way, when it is time to access the state, you simply do self.states[self.state] to get the current state.
     

    def add_state(self, state):
        """
        Adds a new state to the Automaton object. This is done by updating Automaton.states.

        Parameters:
            state : a State instance, to be used by the Automaton.
        
        Returns: Nothing.
        """
        
        self.states[state.name] = state # Update self.states. See documentation for self.states for more info.

    def set_default(self, state:str):
        """
        Sets the default state to an existing state, as a string.

        Parameters:
            state: an existing state, as a string.

        Returns: Nothing
        """

        self.states["DEFAULT"] = self.states[state]
        # This creates a new state, "DEFAULT", with the same exact functionality as the specified state.
    
    def change_state(self, state):
        """
        Changes the current state the Automaton is in, by updating Automaton.state.

        Parameters:
            state : The state to change to, as a string.
        """

        self.state = state # Changes the state to the specified state name, as a string. See self.states for reasoning behind this.

    def __call__(self):
        """
        The 'trigger' for the Automaton object. It executes the current state.
        """

        self.states[self.state]() # You see, the call() method for a State object calls the function assigned to the state, passing in the Automaton instance it belongs to, as a positional argument. 

    def register(self, allowed_states, default=False):
        """
        A wizard to automatically create a state for an Automaton object, by decorating a function. The function can access the Automaton object through a single positional argument for the function.

        register() itself is a decorator factory.
        """

        def decorator(func):
            state = State(self, func.__name__, allowed_states, func) # Creates a state.

            self.add_state(state) # Creates a state based on the name of the function.
            if default:
                self.set_default(func.__name__)
            def wrapper():
                func(self) # Calls the function, passing the Automaton object as a parameter to it to allow the function to access the Automaton itself (such as changing state internally)
            return wrapper
        return decorator

class State:
    """
    A state for an Automaton. These states always have a function bound to them, to give states functionality.
    """

    def __init__(self, parent, name, allowed, func):
        self.parent = parent # The automaton itself.
        self.name = name # The name of the state
        self.allowed = allowed # The allowed states that may be changed to while in the current state
        self.func = func # A function to call when the Automaton is "triggered", while in this current state.
    def __call__(self):
        """
        Executes the state.
        """
        self.func(self.parent)
