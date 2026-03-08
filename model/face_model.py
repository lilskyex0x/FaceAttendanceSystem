import os
import sys
import pickle
import cv2
import face_recognition
from pathlib import Path


# --------------------------------------------------
# MAC-SAFE APPLICATION DATA DIRECTORY
# ~/Library/Application Support/FaceAttendance
# --------------------------------------------------
def get_app_data_dir():
    base = Path.home() / "Library" / "Application Support" / "FaceAttendance"
    base.mkdir(parents=True, exist_ok=True)
    return base


BASE_DIR = get_app_data_dir()
DATASET_DIR = BASE_DIR / "dataset"
ENCODING_FILE = BASE_DIR / "encodings.pickle"

DATASET_DIR.mkdir(parents=True, exist_ok=True)


class FaceModel:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []

        if ENCODING_FILE.exists():
            with open(ENCODING_FILE, "rb") as f:
                data = pickle.load(f)
                self.known_encodings = data.get("encodings", [])
                self.known_names = data.get("names", [])

    def has_registered_students(self):
        return bool(self.known_encodings)

    # --------------------------------------------------
    # FACE DETECTION
    # --------------------------------------------------
    def _detect_faces(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return face_recognition.face_locations(rgb)

    # --------------------------------------------------
    # RECOGNITION
    # --------------------------------------------------
    def recognize(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        results = []

        for encoding in encodings:
            matches = face_recognition.compare_faces(
                self.known_encodings, encoding, tolerance=0.45
            )

            name = None
            if True in matches:
                name = self.known_names[matches.index(True)]

            results.append(name)

        return results, locations

    # --------------------------------------------------
    # SAVE NEW STUDENT
    # --------------------------------------------------
    def save_new_student(self, frames, name):
        student_dir = DATASET_DIR / name
        student_dir.mkdir(parents=True, exist_ok=True)

        MAX_SAMPLES = 30
        saved = 0

        for frame in frames:
            if saved >= MAX_SAMPLES:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)

            if not boxes:
                continue

            encs = face_recognition.face_encodings(rgb, boxes)
            if not encs:
                continue

            top, right, bottom, left = boxes[0]
            face_img = frame[top:bottom, left:right]

            if face_img.size == 0:
                continue

            img_path = student_dir / f"{saved:03d}.jpg"
            cv2.imwrite(str(img_path), face_img)

            self.known_encodings.append(encs[0])
            self.known_names.append(name)

            saved += 1

        if saved == 0:
            print("[WARN] No faces saved")
            return

        with open(ENCODING_FILE, "wb") as f:
            pickle.dump(
                {"encodings": self.known_encodings, "names": self.known_names},
                f
            )

        print(f"[INFO] Saved {saved} samples for {name}")
