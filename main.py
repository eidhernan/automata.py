from automata import Automaton
 
"""DOCUMENTATION IN NOTES.MD"""


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