# hand_controller.py
import cv2
import mediapipe as mp
import pyautogui
import math

class HandMouseController:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands(max_num_hands=1)
        self.draw = mp.solutions.drawing_utils
        self.screen_width, self.screen_height = pyautogui.size()
        self.zoom_mode = None

    def fingers_up(self, lm_list):
        fingers = []
        # Thumb
        fingers.append(lm_list[4][0] > lm_list[3][0])
        # Other fingers
        for id in [8, 12, 16, 20]:
            fingers.append(lm_list[id][1] < lm_list[id - 2][1])
        return fingers

    def start_control(self):
        while True:
            ret, frame = self.cam.read()
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    lm_list = []
                    for id, lm in enumerate(hand_landmarks.landmark):
                        lm_list.append((int(lm.x * w), int(lm.y * h)))

                    # Index Finger controls the mouse
                    index_x, index_y = lm_list[8]
                    screen_x = int(index_x * self.screen_width / w)
                    screen_y = int(index_y * self.screen_height / h)
                    pyautogui.moveTo(screen_x, screen_y)

                    # Pinch Gesture - Click
                    thumb_tip = lm_list[4]
                    if math.hypot(index_x - thumb_tip[0], index_y - thumb_tip[1]) < 30:
                        pyautogui.click()

                    # Scroll Up (Index + Middle Up)
                    fingers = self.fingers_up(lm_list)
                    if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
                        pyautogui.scroll(50)

                    # Scroll Down (Index Up, Middle Down)
                    if fingers[1] and not fingers[2]:
                        pyautogui.scroll(-50)

                    # Zoom In - Thumb + Middle Finger Pinch
                    middle_x, middle_y = lm_list[12]
                    if math.hypot(thumb_tip[0] - middle_x, thumb_tip[1] - middle_y) < 30:
                        pyautogui.hotkey('ctrl', '+')

                    # Zoom Out - Thumb + Ring Finger Pinch
                    ring_x, ring_y = lm_list[16]
                    if math.hypot(thumb_tip[0] - ring_x, thumb_tip[1] - ring_y) < 30:
                        pyautogui.hotkey('ctrl', '-')

                    self.draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

            cv2.imshow("🖐️ Hand Gesture Controller", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cam.release()
        cv2.destroyAllWindows()
        self.hands.close()