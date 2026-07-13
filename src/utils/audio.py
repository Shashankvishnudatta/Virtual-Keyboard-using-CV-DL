import numpy as np
import sounddevice as sd

class AudioFeedback:
    """Provides synthetic digital auditory haptics directly to the main speakers."""
    
    # Pre-compute the sound wave in memory so there is absolutely ZERO latency
    SAMPLE_RATE = 44100
    DURATION = 0.04  # 40 milliseconds for a fast, crisp click
    
    # 1. Create a time array
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), False)
    
    # 2. Create a sharp exponential decay envelope (starts loud, fades instantly)
    envelope = np.exp(-t * 200)
    
    # 3. Create a high-frequency mechanical "tick" (combining two frequencies for texture)
    wave = (np.sin(2 * np.pi * 1200 * t) + np.sin(2 * np.pi * 2800 * t)) * 0.5
    
    # 4. Apply the envelope and set the volume to 30%
    CLICK_SOUND = wave * envelope * 0.3 

    @classmethod
    def play_click(cls):
        """Plays the pre-computed sound wave. sounddevice.play is naturally non-blocking!"""
        try:
            # Flushes any currently playing sound and instantly plays the new one
            sd.stop() 
            sd.play(cls.CLICK_SOUND, cls.SAMPLE_RATE)
        except Exception as e:
            # Fails silently so it doesn't crash your camera if audio drivers are busy
            pass