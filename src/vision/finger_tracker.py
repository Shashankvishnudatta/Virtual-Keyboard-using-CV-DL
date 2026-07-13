from src.vision.landmark_utils import get_pixel_coordinates

class FingerTracker:
    """Extracts points of interest and applies Exponential Moving Average (EMA) smoothing."""
    
    def __init__(self, smoothing_factor=0.6):
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8
        
        # Smoothing factor: 1.0 = No smoothing, 0.1 = Very heavy/slow smoothing
        self.smoothing = smoothing_factor
        
        # Memory to store the previous frame's coordinates for each hand
        self.prev_positions = {}

    def extract_cursor_points(self, hand_landmarks, img_width, img_height, hand_id=0):
        """
        Extracts (x,y) coordinates and applies a low-pass smoothing filter.
        """
        # Get raw coordinates
        thumb_raw = get_pixel_coordinates(hand_landmarks.landmark[self.THUMB_TIP], img_width, img_height)
        index_raw = get_pixel_coordinates(hand_landmarks.landmark[self.INDEX_TIP], img_width, img_height)

        # If we have never seen this hand before, just use the raw coordinates
        if hand_id not in self.prev_positions:
            self.prev_positions[hand_id] = {"thumb": thumb_raw, "index": index_raw}
            return self.prev_positions[hand_id]

        # Retrieve previous frame's positions
        prev_thumb = self.prev_positions[hand_id]["thumb"]
        prev_index = self.prev_positions[hand_id]["index"]

        # ADVANCED LOGIC: Exponential Moving Average Calculation
        # New Position = (Raw * Smoothing) + (Previous * (1 - Smoothing))
        smooth_thumb_x = int((thumb_raw[0] * self.smoothing) + (prev_thumb[0] * (1 - self.smoothing)))
        smooth_thumb_y = int((thumb_raw[1] * self.smoothing) + (prev_thumb[1] * (1 - self.smoothing)))
        
        smooth_index_x = int((index_raw[0] * self.smoothing) + (prev_index[0] * (1 - self.smoothing)))
        smooth_index_y = int((index_raw[1] * self.smoothing) + (prev_index[1] * (1 - self.smoothing)))

        # Pack the smoothed coordinates
        smoothed_points = {
            "thumb": (smooth_thumb_x, smooth_thumb_y),
            "index": (smooth_index_x, smooth_index_y)
        }
        
        # Save for the next frame
        self.prev_positions[hand_id] = smoothed_points

        return smoothed_points