import cv2
import yaml
import pyautogui

from src.camera.webcam import WebcamModule
from src.vision.hand_detector import HandDetector
from src.vision.finger_tracker import FingerTracker
from src.vision.pose_utils import PoseClassifier
from src.keyboard.layouts import get_qwerty_layout
from src.keyboard.renderer import KeyboardRenderer
from src.keyboard.hit_testing import HitTester
from src.gestures.recognizer import GestureRecognizer
from src.gestures.debounce import StateManager   # NEW
from src.typing.engine import TypingEngine
from src.typing.statistics import Telemetry      # NEW
from src.ai.suggestion_engine import PredictiveEngine
from src.utils.audio import AudioFeedback

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def main():
    print("Starting Advanced HCI Platform...")
    
    config = load_config()
    cam_settings = config['camera']
    vis_settings = config['vision']
    
    camera = WebcamModule(cam_settings['device_id'], cam_settings['width'], cam_settings['height'])
    detector = HandDetector(vis_settings['max_hands'], 0.5, 0.5)
    tracker = FingerTracker()
    pose_classifier = PoseClassifier()
    recognizer = GestureRecognizer(pinch_threshold=40)
    
    keyboard_keys = get_qwerty_layout()
    renderer = KeyboardRenderer(alpha=0.4)
    typing_engine = TypingEngine()
    ai_engine = PredictiveEngine(model_name="qwen2.5:0.5b")

    # NEW: State Manager + Telemetry
    fsm = StateManager()
    stats = Telemetry()

    print("System Online. Press Ctrl+C to quit.\n")

    try:
        while True:
            success, frame = camera.read_frame()
            if not success:
                break

            h, w, _ = frame.shape
            frame, hands = detector.process_frame(frame, draw=True)

            # Reset keyboard states
            for key in keyboard_keys:
                key.is_pressed = False
                key.is_hovered = False

            is_sleeping = False
            current_suggestions = ai_engine.get_suggestions()

            if hands:
                # Mode switching logic
                hand_y = hands[0].landmark[0].y * h
                mode = fsm.update_state(hand_y)

                if mode == StateManager.TRACKPAD:
                    index_px = tracker.extract_cursor_points(hands[0], w, h, 0)["index"]
                    pyautogui.moveTo(index_px[0] * 1.5, index_px[1] * 1.5)

                elif mode == StateManager.KEYBOARD:
                    for hand_id, hand_landmarks in enumerate(hands):
                        pose = pose_classifier.classify_pose(hand_landmarks)
                        if pose == "FIST":
                            is_sleeping = True
                            continue

                        points = tracker.extract_cursor_points(hand_landmarks, w, h, hand_id)
                        index_pos = points["index"]
                        thumb_pos = points["thumb"]

                        hovered_key = HitTester.check_hover(keyboard_keys, index_pos)
                        is_clicking, distance = recognizer.detect_pinch(thumb_pos, index_pos, hand_id)

                        if hovered_key and is_clicking:
                            hovered_key.is_pressed = True
                            AudioFeedback.play_click()

                            if "PRED_" in hovered_key.text:
                                pred_idx = int(hovered_key.text[-1])
                                if pred_idx < len(current_suggestions) and current_suggestions[pred_idx]:
                                    word = current_suggestions[pred_idx]
                                    pyautogui.write(word.lower() + " ")
                                    typing_engine.current_text += (word + " ")
                                    ai_engine.update_text(typing_engine.get_text())
                            else:
                                typing_engine.process_keypress(hovered_key.text)
                                ai_engine.update_text(typing_engine.get_text())

                        color = (0, 255, 0) if distance < 40 else (255, 255, 0)
                        cv2.circle(frame, index_pos, 15, color, cv2.FILLED)

            # Render UI with mode + telemetry
            frame = renderer.draw_keyboard(frame, keyboard_keys, current_suggestions, is_sleeping)
            cv2.putText(frame, f"MODE: {fsm.current_state}", (50, 600),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.putText(frame, f"FPS: {stats.get_fps()}", (50, 650),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            cv2.imshow("VisionTypeAI", frame)

            stats.update()  # Update telemetry stats

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        print("Shutting down subsystems safely...")
        ai_engine.stop()
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
