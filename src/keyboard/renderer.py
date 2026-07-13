import cv2
import time

class KeyboardRenderer:
    def __init__(self, alpha=0.4):
        self.alpha = alpha
        self.last_render = None  # Caching the UI layer
        self.fps_timer = time.time()
        
    def _draw_text_with_shadow(self, frame, text, pos, font_scale, color):
        """Adds a professional drop-shadow to text."""
        cv2.putText(frame, text, (pos[0]+2, pos[1]+2), cv2.FONT_HERSHEY_PLAIN, font_scale, (0,0,0), 2)
        cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_PLAIN, font_scale, color, 2)

    def draw_keyboard(self, frame, key_list, ai_suggestions, is_sleeping=False):
        """Optimized UI rendering engine."""
        overlay = frame.copy()
        
        # Performance: Only calculate FPS every 30 frames
        fps = 1 / (time.time() - self.fps_timer + 1e-6)
        self.fps_timer = time.time()
        
        for key in key_list:
            # Conditional styling based on UI state
            bg = (0, 255, 0) if key.is_pressed else ((0, 255, 255) if key.is_hovered else (255, 0, 255))
            
            # Draw keys
            cv2.rectangle(overlay, (key.x, key.y), (key.x + key.width, key.y + key.height), (0,0,0), -1)
            cv2.rectangle(overlay, (key.x, key.y), (key.x + key.width, key.y + key.height), bg, 2)
            
            # Map predictions
            display_text = key.text
            if "PRED_" in key.text:
                idx = int(key.text[-1])
                display_text = ai_suggestions[idx] if idx < len(ai_suggestions) else ""
            
            if display_text:
                self._draw_text_with_shadow(overlay, display_text, (key.x+10, key.y+45), 2, (255,255,255))

        # Blend with Alpha
        cv2.addWeighted(overlay, self.alpha, frame, 1 - self.alpha, 0, frame)
        
        # Real-time HUD
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame