import cv2
import os

def capture_and_save():
    cam = cv2.VideoCapture(1)  # 1 = फ्रंट कैमरा (अगर न चले तो 0, 2 ट्राय करें)
    ret, frame = cam.read()

    if ret:
        media_path = os.path.join("media", "captured_image.jpg")  # Django के media/ फोल्डर में Save करें
        cv2.imwrite(media_path, frame)
        print(f"✅ Photo saved at {media_path}")

    cam.release()

capture_and_save()
