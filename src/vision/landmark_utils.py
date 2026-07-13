import math

def get_pixel_coordinates(landmark, img_width, img_height):
    """
    Converts normalized MediaPipe coordinates (0.0 to 1.0) 
    into absolute pixel coordinates on the screen.
    """
    x_px = min(math.floor(landmark.x * img_width), img_width - 1)
    y_px = min(math.floor(landmark.y * img_height), img_height - 1)
    return x_px, y_px

def calculate_distance(point1, point2):
    """
    Calculates the Euclidean distance between two pixel coordinates.
    Useful for determining if fingers are touching (e.g., a pinch gesture).
    """
    x1, y1 = point1
    x2, y2 = point2
    return math.hypot(x2 - x1, y2 - y1) 
