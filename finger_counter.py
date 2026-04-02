import pygame
import cv2
import mediapipe as mp

# ================= MEDIAPIPE =================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
finger_tips = [4, 8, 12, 16, 20]

def count_fingers(frame):
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if not result.multi_hand_landmarks:
        return -1

    hand = result.multi_hand_landmarks[0]
    lm = hand.landmark
    count = 0

    handedness = result.multi_handedness[0].classification[0].label

    # Ngón cái (xử lý cả tay trái & phải)
    if handedness == "Right":
        if lm[4].x < lm[3].x:
            count += 1
    else:
        if lm[4].x > lm[3].x:
            count += 1

    # 4 ngón còn lại
    for tip in finger_tips[1:]:
        if lm[tip].y < lm[tip - 2].y:
            count += 1

    return count

# ================= PYGAME =================
pygame.init()
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption('Finger Counter')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

status = True

while status:
    clock.tick(60)
    screen.fill((255, 255, 255))

    # ======= CAMERA =======
    ret, frame = cap.read()
    fingers = count_fingers(frame) if ret else -1

    # ======= GAME =======
    text = font.render("So ngon tay: " + str(fingers), True, (0, 0 ,0))
    text_rect = text.get_rect(center=(300, 150))
    screen.blit(text, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False

    pygame.display.flip()

cap.release()
hands.close()
pygame.quit()
