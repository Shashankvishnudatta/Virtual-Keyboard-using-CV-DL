class VirtualKey:
    """Represents a single key on the virtual keyboard."""
    
    def __init__(self, text, x, y, width=80, height=80):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # We will use this later for hover and click animations
        self.is_hovered = False
        self.is_pressed = False

    def get_rect(self):
        """Returns the bounding box of the key for hit testing."""
        return (self.x, self.y, self.width, self.height) 
