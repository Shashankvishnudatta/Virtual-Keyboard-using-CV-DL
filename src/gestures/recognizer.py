import math

class GestureRecognizer:
    """Analyzes hand landmarks with advanced State-Machine Edge Triggering."""
    
    def __init__(self, pinch_threshold=40):
        self.pinch_threshold = pinch_threshold
        # Memory dictionary to track if a hand was pinched in the PREVIOUS frame
        self.hand_states = {}

    def detect_pinch(self, thumb_pos, index_pos, hand_id):
        """
        Registers a click ONLY on the exact frame the fingers transition from Open to Pinched.
        """
        distance = math.hypot(index_pos[0] - thumb_pos[0], index_pos[1] - thumb_pos[1])
        
        # Current physical state
        is_currently_pinched = distance < self.pinch_threshold
        
        # Previous physical state (defaults to False / Open)
        was_pinched = self.hand_states.get(hand_id, False)
        
        click_triggered = False
        
        # ADVANCED LOGIC: The "Falling Edge" Trigger
        # If the hand wasn't pinched a millisecond ago, but is pinched now -> CLICK!
        if is_currently_pinched and not was_pinched:
            click_triggered = True
            
        # Save the current state so the next frame knows what happened
        self.hand_states[hand_id] = is_currently_pinched
                
        return click_triggered, distance