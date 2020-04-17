These are the notes for my prototype state design pattern.

1. Abstract.
The State Design Pattern is a way to limit control flow without the use of branching. In an object known as an Automaton, there exists a finite number of states (hence the name, Finite State Machine). When the Automaton is triggered when it is in a specific state, a specific set of instructions are executed, in the form of a function. Additionally, the state may be changed from inside another state.

Let us use an example: a lock. A lock typically has two states, locked, and unlocked. Additionally, you may take actions that result in the change in state. These "actions" are a special kind of state, known as transition states. These states are normal states, but they only serve one purpose, to transition from one state to another. Think of them like "elevators" that connect floors, except in this case, the floors are states.

Anyway, in order to set up the states for a lock, well, we need a lock, so let's make one.
```py
from automata import Automaton
lock = Automaton()
```

We made our lock by instantiating Automaton. We do not need to pass any arguments to Automaton. 
Now that we have our lock, we can now add the states. States always have a function associated with them, and we can actually build a state around our function with a decorator.

Consider this code snippet, for our Locked state:
```py
@lock.register(allowed_states=["unlock"], default=True)
```
As you can see, this decorator must include the allowed states to switch to while in this state (``allowed_states``), and whether or not this is the default state, or the state that the Automaton will be in by default.

Pretty simple, so far. Now things may get confusing. Now, we will make our function to decorate.
```py
@lock.register(allowed_states=["unlock"], default=True)
def locked(parent):
    print("The current state is LOCKED.")
```
Now, you probably understand everything except for the ``parent`` argument. What is that? Well, you know how with instance methods, you need to pass ``self`` in order to access the instance? Well, this is the same thing. The ``parent`` argument is used to access the Automaton itself, that way we can change the state of the automaton from another state, and much more.``

This is what our code looks like now:
```py
from automata import Automaton

lock = Automaton()

@lock.register(allowed_states=["unlock"], default=True)
def locked(parent):
    print("The current state is LOCKED.")
```
If you run that code, you won't get any errors, but also, nothing happens. That's because while we created our lock, and a state for it, we haven't actually executed the lock. In order to do that, we just treat ``lock`` as a function, and call it.
```py
lock()
```
Add this line to the end of your file, and run it. If you have no errors, it should print out this:
```js
Out [1]: the current state is LOCKED.
```
Okay, so now how do we change the state? Well, in order to change the state, well, we need to make sure the state exists. We will be registering another state, ``unlock``. 'unlock' is a transition state, it is a state that only serves one purpose, to transition from one state to another.

```py
@lock.register(allowed_states=["unlocked", "locked"])
def unlock(parent):
    print("You are unlocking. Please enter the PIN. (it is 1234)")
    pin = input("PIN: >")
    if pin == "1234":
        print("Correct PIN. Unlocking...")
        parent.change_state("unlocked")
    else:
        print("Incorrect PIN. The state is still LOCKED.")
        parent.change_state("locked")
```
Now when we run this, nothing changes. That is because we need to trigger `lock` again. Instead of having `lock()` at the end of your code, replace it with this:
```py
if __name__ == "__main__":
    lock()
    lock.change_state("unlock") # change the state
    lock() # execute again.
    lock() # execute one more time.
```
Now execute your code. The following screen will show:
```
The current state is LOCKED.
You are unlocking. Please enter the PIN. (it is 1234)
PIN: >
```
If you put anything but 1234, this will show:
```
Incorrect PIN. The state is still LOCKED.
The current state is LOCKED.
```
But if you put in 1234, the following error will show:
```diff
Correct PIN. Unlocking...
Traceback (most recent call last):
  File "main.py", line 24, in <module>
    lock()
  File "(ABSOLUTE FILE PATH)/automata.py", line 16, in __call__
    self.states[self.state]()
KeyError: 'unlocked'
```
We get a KeyError, for 'unlocked'. If you recall, we changed the state to 'unlocked', but we never made an 'unlocked' state, so we need to add that, and additionally, we need to be able to lock again, so we will make a transition state, 'lock'.
```py
@lock.register(allowed_states=["_lock"])
def unlocked(parent):
    print("The state is UNLOCKED.")

@lock.register(allowed_states=["locked"])
def _lock(parent):
    print("Changing the state to LOCKED...")
    parent.change_state("locked")
```
Putting it all together, this is all the code:
```py
from automata import Automaton
 
lock = Automaton()
 
@lock.register(allowed_states=["unlock"], default=True)
def locked(parent):
    print("The current state is LOCKED.")


@lock.register(allowed_states=["unlocked", "locked"])
def unlock(parent):
    print("You are unlocking. Please enter the PIN. (it is 1234)")
    pin = input("PIN: >")
    if pin == "1234":
        print("Correct PIN. Unlocking...")
        parent.change_state("unlocked")
    else:
        print("Incorrect PIN. The state is still LOCKED.")
        parent.change_state("locked")


@lock.register(allowed_states=["_lock"])
def unlocked(parent):
    print("The state is UNLOCKED.")
 

@lock.register(allowed_states=["locked"])
def _lock(parent):
    print("Changing the state to LOCKED...")
    parent.change_state("locked")


if __name__ == "__main__":
    lock()
    lock.change_state("unlock") # change the state
    lock() # execute again.
    lock() #execute one more time...
    print("")
    print("press enter to continue...")
    input()
    lock.change_state("_lock")
    lock()
    lock()
```