import cv2 as cv
import mediapipe as mp
import math
from mediapipe.tasks.python import vision, BaseOptions
from visualization import draw_manual, print_RSP_result

FINGERS = [(8, 6), (12, 10), (16, 14), (20, 18)]

def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def count_extended(landmarks):
    wrist = landmarks[0]
    count = 0
    for tip, pip in FINGERS:
        if dist(landmarks[tip], wrist) > dist(landmarks[pip], wrist):
            count += 1
    return count


def finger_count(count):
    if count == 0:
        return 0 #Rock
    if count == 4:
        return 1 # Paper
    if count == 2:
        return 2 # Scissors
    return None


def main():
    options = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
        num_hands=1
    )
    detector = vision.HandLandmarker.create_from_options(options)

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.flip(frame, 1) # 좌우 반전

        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        result = detector.detect(mp_image)

        rps = None
        if result.hand_landmarks:
            rps = finger_count(count_extended(result.hand_landmarks[0]))

        frame = draw_manual(frame, result)
        frame = print_RSP_result(frame, rps)

        cv.imshow('RPS', frame)

        if cv.waitKey(1) == ord('q'): # q탈출
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()