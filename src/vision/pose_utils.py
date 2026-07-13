class PoseClassifier:
    """Analyzes hand geometry to classify complex semantic poses."""
    
    def __init__(self):
        # MediaPipe landmark indices
        self.WRIST = 0
        self.FINGERTIPS = [8, 12, 16, 20] # Index, Middle, Ring, Pinky
        self.FINGER_PIPS = [6, 10, 14, 18] # The middle knuckles
        
    def classify_pose(self, hand_landmarks):
        """
        Determines if fingers are extended or folded.
        Returns: 'FIST', 'OPEN', or 'DEFAULT'
        """
        extended_fingers = 0
        
        # A finger is "extended" if its tip is further from the wrist than its knuckle
        for tip_idx, pip_idx in zip(self.FINGERTIPS, self.FINGER_PIPS):
            tip_y = hand_landmarks.landmark[tip_idx].y
            pip_y = hand_landmarks.landmark[pip_idx].y
            
            # In image coordinates, lower Y means higher up on the screen
            if tip_y < pip_y: 
                extended_fingers += 1
                
        # If all 4 main fingers are folded down, it's a closed fist
        if extended_fingers == 0:
            return "FIST"
        # If all 4 are up, it's an open palm
        elif extended_fingers == 4:
            return "OPEN"
            
        return "DEFAULT" 
