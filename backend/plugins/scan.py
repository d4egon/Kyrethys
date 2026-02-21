import cv2

def find_camera():
    for i in range(10):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"Kamera fundet på indeks: {i}")
            cap.release()
        else:
            print(f"Intet på indeks: {i}")

find_camera()