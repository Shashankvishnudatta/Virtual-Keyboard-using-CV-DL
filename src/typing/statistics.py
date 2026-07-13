import time
from functools import wraps

class Telemetry:
    """Advanced logging and performance metrics for the HCI platform."""
    
    def __init__(self):
        self.metrics = {"keystrokes": 0, "session_start": time.time()}
        self.prev_time = time.time()
        self.fps = 0.0
        self.frame_count = 0

    def log_keystroke(self):
        self.metrics["keystrokes"] += 1

    def update_fps(self):
        """Calculates rolling frame rate dynamically per loop iteration."""
        current_time = time.time()
        time_diff = current_time - self.prev_time
        self.frame_count += 1
        
        # Update FPS calculation every second or per frame smoothly
        if time_diff > 0.05:  
            self.fps = 1.0 / (time_diff if time_diff > 0 else 1e-6)
            self.prev_time = current_time

    def get_fps(self):
        """Returns integer representation of the current frame rate."""
        return int(self.fps)

    @staticmethod
    def profile(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            # Optional debug latency tracing
            return result
        return wrapper