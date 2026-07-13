class SystemState:
    TRACKPAD = "TRACKPAD"
    KEYBOARD = "KEYBOARD"
    SLEEP = "SLEEP"

class StateManager:
    """Finite State Machine (FSM) to handle mode switching."""
    def __init__(self):
        self.current_state = SystemState.KEYBOARD

    def update_state(self, hand_y):
        # If hand is high up (Y < 200), switch to Trackpad, else Keyboard
        if hand_y < 200:
            self.current_state = SystemState.TRACKPAD
        else:
            self.current_state = SystemState.KEYBOARD
        return self.current_state 
