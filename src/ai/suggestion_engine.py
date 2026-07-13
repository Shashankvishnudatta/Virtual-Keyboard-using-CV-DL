import threading
import time
import ollama

class PredictiveEngine:
    """Advanced AI Engine delivering 3-option iOS-style predictions."""
    
    def __init__(self, model_name="qwen2.5:0.5b"):
        self.current_text = ""
        self.suggestions = ["", "", ""] # Array of 3 options
        self.is_running = True
        self.model = model_name
        self.lock = threading.Lock()
        
        # Common English prefixes to instantly fix the "BO" -> "BOY" issue
        self.fast_dict = {
            "TH": ["THE", "THIS", "THAT"],
            "WH": ["WHAT", "WHERE", "WHEN"],
            "BO": ["BOY", "BOX", "BOAT"],
            "PRO": ["PROJECT", "PROGRAM", "PROVE"]
        }
        
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def update_text(self, text):
        with self.lock:
            self.current_text = text.strip()

    def get_suggestions(self):
        with self.lock:
            return self.suggestions

    def stop(self):
        self.is_running = False
        self.worker_thread.join()

    def _worker_loop(self):
        last_analyzed = ""
        
        while self.is_running:
            with self.lock:
                text = self.current_text.upper()
                
            if not text or text == last_analyzed:
                time.sleep(0.1)
                continue
                
            last_analyzed = text
            words = text.split()
            last_word = words[-1] if words else ""
            
            new_suggestions = ["", "", ""]
            
            # SCENARIO 1: User is mid-word. Use the fast dictionary to prevent hallucinations.
            if not text.endswith(" ") and last_word in self.fast_dict:
                new_suggestions = self.fast_dict[last_word]
                
            # SCENARIO 2: User finished a word (typed space). Use the LLM to predict the NEXT word.
            elif text.endswith(" ") or len(words) > 1:
                try:
                    context = " ".join(words[-4:])
                    prompt = (
                        f"Complete the sentence: '{context}'. "
                        f"Provide 3 different single-word options that could logically come next. "
                        f"Format exactly like this: word1, word2, word3"
                    )
                    
                    response = ollama.generate(
                        model=self.model, prompt=prompt, 
                        options={'temperature': 0.7, 'num_predict': 15}
                    )
                    
                    raw_words = response['response'].replace('.', '').replace('\n', '').split(',')
                    cleaned_words = [w.strip().upper() for w in raw_words if w.strip().isalpha()]
                    
                    # Pad the array if the AI returned fewer than 3 words
                    while len(cleaned_words) < 3:
                        cleaned_words.append("")
                        
                    new_suggestions = cleaned_words[:3]
                except Exception:
                    time.sleep(1)
                    
            with self.lock:
                if self.current_text.upper() == text:
                    self.suggestions = new_suggestions