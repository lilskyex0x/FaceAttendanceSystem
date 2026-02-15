import time
import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal


class CameraThread(QThread):
    frame_ready = pyqtSignal(np.ndarray)
    attendance_signal = pyqtSignal(str)
    collect_finished = pyqtSignal(str)

    def __init__(self, face_model):
        super().__init__()
        self.face_model = face_model
        self.running = True
        self.mode = "idle"  # idle | attendance | collect

        self.already_marked = set()

        self.collected_frames = []
        self.collect_start_time = None
        self.student_name = None

    def run(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("[ERROR] Camera could not be opened")
            return

        while self.running:
            try:
                ret, frame = cap.read()
                if not ret:
                    continue

                # ================== COLLECT MODE ==================
                if self.mode == "collect":
                    if self.collect_start_time is None:
                        self.collect_start_time = time.time()

                    elapsed = time.time() - self.collect_start_time
                    locations = self.face_model._detect_faces(frame)

                    for (top, right, bottom, left) in locations:
                        cv2.rectangle(
                            frame, (left, top), (right, bottom), (0, 255, 0), 2
                        )
                        cv2.putText(
                            frame, "Collecting...",
                            (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2
                        )

                    if elapsed <= 5:
                        self.collected_frames.append(frame.copy())
                    else:
                        self.face_model.save_new_student(
                            self.collected_frames,
                            self.student_name
                        )
                        self.collect_finished.emit(self.student_name)

                        self.collected_frames.clear()
                        self.collect_start_time = None
                        self.mode = "idle"

                # ================= ATTENDANCE MODE =================
                elif self.mode == "attendance":
                    names, locations = self.face_model.recognize(frame)

                    for (top, right, bottom, left), name in zip(locations, names):
                        cv2.rectangle(
                            frame, (left, top), (right, bottom), (0, 255, 0), 2
                        )

                        label = name if name else "Unknown"
                        cv2.putText(
                            frame,
                            label,
                            (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 0),
                            2
                        )

                        # 🔥 IMPORTANT FIX
                        if name and name not in self.already_marked:
                            self.already_marked.add(name)
                            self.attendance_signal.emit(name)

                self.frame_ready.emit(frame)

            except Exception as e:
                print("[CameraThread ERROR]", e)
                break

        cap.release()

    def stop(self):
        self.running = False
        self.wait()

    def start_attendance(self):
        self.already_marked.clear()   # 🔥 RESET HERE
        self.mode = "attendance"

    def stop_attendance(self):
        self.mode = "idle"
        self.already_marked.clear()   # 🔥 RESET HERE

    def start_collect(self, student_name):
        self.student_name = student_name
        self.collected_frames.clear()
        self.collect_start_time = None
        self.mode = "collect"
