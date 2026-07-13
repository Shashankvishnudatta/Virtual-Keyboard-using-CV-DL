import cv2

class WebcamModule:
    """Handles all webcam interactions and frame capturing."""
    
    def __init__(self, camera_id=0, width=1280, height=720):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id)
        
        # Request specific resolution from the hardware
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self.cap.isOpened():
            raise ValueError(f"Error: Unable to open camera with ID {self.camera_id}")

    def read_frame(self):
        """Reads a frame and flips it for a mirror effect."""
        success, frame = self.cap.read()
        if not success:
            return False, None
            
        # Flip horizontally (1) so when you move your right hand, 
        # it moves on the right side of the screen.
        frame = cv2.flip(frame, 1)
        return True, frame

    def release(self):
        """Releases the camera hardware."""
        self.cap.release()