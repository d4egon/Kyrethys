import cv2
import os
import datetime

class MarvixVision:
    def __init__(self):
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.snapshot_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'snapshots')
        if not os.path.exists(self.snapshot_path):
            os.makedirs(self.snapshot_path)

    def capture_snapshot(self):
        success, frame = self.camera.read()
        if success:
            # FLIP: -1 flipper både horisontalt og vertikalt (180 grader)
            frame = cv2.flip(frame, -1)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snap_{timestamp}.jpg"
            full_path = os.path.join(self.snapshot_path, filename)
            cv2.imwrite(full_path, frame)
            return filename 
        return None

    def generate_frames(self): # Omdøbt fra get_frames for at matche din backend route
        while True:
            success, frame = self.camera.read()
            if not success: break
            
            # FLIP: Sikrer at dit Live Feed i frontenden også vender rigtigt
            frame = cv2.flip(frame, -1)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def __del__(self):
        if hasattr(self, 'camera') and self.camera.isOpened():
            self.camera.release()