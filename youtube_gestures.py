import cv2
import mediapipe as mp
import pyautogui
import time

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# Cooldown variables
last_action_time = 0
cooldown = 2  # seconds

# Gesture detection function
def get_gesture(landmarks):
    thumb_tip = landmarks[4].y
    index_tip = landmarks[8].y
    middle_tip = landmarks[12].y
    ring_tip = landmarks[16].y
    pinky_tip = landmarks[20].y

    # Play (✊ fist)
    if (index_tip > landmarks[6].y and
        middle_tip > landmarks[10].y and
        ring_tip > landmarks[14].y and
        pinky_tip > landmarks[18].y):
        return "PLAY"

    # Pause (✌️ two fingers up)
    if index_tip < landmarks[6].y and middle_tip < landmarks[10].y and ring_tip > landmarks[14].y:
        return "PAUSE"

    # Next video (👉 point with index)
    if index_tip < landmarks[6].y and middle_tip > landmarks[10].y:
        return "NEXT"

    # Previous video (🖐️ all fingers up)
    if (index_tip < landmarks[6].y and
        middle_tip < landmarks[10].y and
        ring_tip < landmarks[14].y and
        pinky_tip < landmarks[18].y):
        return "PREVIOUS"

    return None

# Webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip for mirror effect
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            gesture = get_gesture(hand_landmarks.landmark)

            if gesture and time.time() - last_action_time > cooldown:
                if gesture == "PLAY":
                    pyautogui.press("space")
                    print("▶️ Play Video")
                elif gesture == "PAUSE":
                    pyautogui.press("space")
                    print("⏸️ Pause Video")
                elif gesture == "NEXT":
                    pyautogui.hotkey("shift", "n")
                    print("⏭️ Next Video")
                elif gesture == "PREVIOUS":
                    pyautogui.hotkey("shift", "p")
                    print("⏮️ Previous Video")

                last_action_time = time.time()

    cv2.imshow("YouTube Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
