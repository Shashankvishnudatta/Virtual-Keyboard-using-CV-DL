class HitTester:
    """Handles collision detection for multiple concurrent cursors."""
    
    @staticmethod
    def check_hover(keys, cursor_pos):
        """
        Checks if a specific cursor (x, y) is inside any key's bounding box.
        Only sets True (app.py will handle resetting at the start of the frame).
        """
        cx, cy = cursor_pos
        hovered_key = None
        
        for key in keys:
            if (key.x < cx < key.x + key.width) and (key.y < cy < key.y + key.height):
                key.is_hovered = True
                hovered_key = key
                break # Optimization: A cursor can only hover one key at a time
                
        return hovered_key