import cv2, os, time

# NOTE: Legacy helper, currently unused by the main application.
# Kept for reference; FaceModel now handles dataset collection internally.

DATASET_DIR = "dataset"

class DatasetController:

    def collect(self, label, preview_callback):
        os.makedirs(DATASET_DIR, exist_ok=True)
        person_dir = os.path.join(DATASET_DIR, label)
        os.makedirs(person_dir, exist_ok=True)

        cap = cv2.VideoCapture(0)
        start = time.time()
        count = 0

        while time.time() - start < 5:
            ret, frame = cap.read()
            if not ret:
                break
            preview_callback(frame)
            cv2.imwrite(os.path.join(person_dir, f"{count}.jpg"), frame)
            count += 1
            time.sleep(0.15)

        cap.release()
