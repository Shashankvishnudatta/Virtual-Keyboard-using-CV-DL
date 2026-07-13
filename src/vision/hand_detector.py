import cv2
import mediapipe as mp

class HandDetector:
    """Encapsulates MediaPipe Hand tracking logic for clean architecture."""
    
    def __init__(self, max_hands=2, detection_con=0.7, tracking_con=0.7):
        # Standard MediaPipe initialization
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False, 
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=tracking_con
        )
        
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles

    def process_frame(self, frame, draw=True):
        """
        Takes a BGR frame, converts it for MediaPipe, finds hands, 
        and optionally draws the landmarks on the original frame.
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Optimization
        rgb_frame.flags.writeable = False 
        results = self.hands.process(rgb_frame)
        rgb_frame.flags.writeable = True
        
        detected_hands = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_styles.get_default_hand_landmarks_style(),
                        self.mp_styles.get_default_hand_connections_style()
                    )
                detected_hands.append(hand_landmarks)
                
        return frame, detected_hands