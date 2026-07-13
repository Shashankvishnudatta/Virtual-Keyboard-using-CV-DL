import pyautogui

class TypingEngine:
    """Manages internal text state AND injects keystrokes directly into the Windows OS."""
    
    def __init__(self):
        self.current_text = ""
        self.active_suggestion = ""
        
        # Disable pyautogui's default safety pause so our virtual keyboard is lightning fast
        pyautogui.PAUSE = 0 

    def process_keypress(self, key_label):
        """Processes regular characters and executes system commands globally."""
        
        if key_label == "DEL":
            self.current_text = self.current_text[:-1]
            # Tell Windows to press the physical Backspace key
            pyautogui.press('backspace')
            
        elif key_label == "SPACE":
            self.current_text += " "
            pyautogui.press('space')
            
        elif key_label == "CLR":
            # Rapid-fire backspace to clear the physical OS text field
            for _ in range(len(self.current_text)):
                pyautogui.press('backspace')
            self.current_text = ""
            
        elif key_label == "TAB":
            # Autocomplete! Inject the AI suggestion into the OS
            suggestion = self.active_suggestion.lower()
            self.current_text += self.active_suggestion
            pyautogui.write(suggestion) # Types the whole word instantly
            self.active_suggestion = ""
            
        else:
            # Standard letter typing
            self.current_text += key_label
            # Tell Windows to type the lowercase version of the letter
            pyautogui.write(key_label.lower())
            
    def get_text(self):
        """Returns the clean text for the AI engine (no fake cursor)."""
        return self.current_text