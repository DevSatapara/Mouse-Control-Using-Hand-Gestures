import cv2
import mediapipe
import pyautogui

camera = cv2.VideoCapture(0)
capture_hands = mediapipe.solutions.hands.Hands()
drawing_option = mediapipe.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()
x1 = y1 = x2 = y2 = 0
while True:
    _,image = camera.read()
    image = cv2.flip(image,1)
    image_height, image_width,_ = image.shape
    rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    output_hands = capture_hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks
    if all_hands:
        for hands in all_hands:
            drawing_option.draw_landmarks(image,hands)
            one_hand_landmarks = hands.landmark
            for id,lm in enumerate(one_hand_landmarks):
                x = int(lm.x*image_width)
                y = int(lm.y*image_height)
                # print(x,y)
                if id == 8:# id for tip of first finger
                    mouse_x = int(screen_w / image_width * x)
                    mouse_y = int(screen_h / image_height * y)
                    cv2.circle(image,(x,y),10,(0,255,0))
                    pyautogui.moveTo(mouse_x,mouse_y)
                    x1 = x
                    y1 = y
                if id == 4: # id for thumb finger
                    x2 = x
                    y2 = y
                    cv2.circle(image,(x,y),10,(0,255,0))
        dist = y2-y1
        if (dist<23):
            pyautogui.click()
    cv2.imshow("Hand Movements Video Capture",image)
    key = cv2.waitKey(100)
    if key == 27: #value of escape key
        break

camera.release()
cv2.destroyAllWindows()