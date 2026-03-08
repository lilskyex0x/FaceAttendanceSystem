import cv2
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QTableWidget, QInputDialog, QMessageBox
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from open_folder_helper import open_attendance_folder
from controller.camera_thread import CameraThread
from controller.attendance_controller import AttendanceController
from model.face_model import FaceModel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Face Attendance System")
        self.resize(1000, 600)

        # --------- TABLE ----------
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Date", "Time"])
        self.table.horizontalHeader().setStretchLastSection(True)

        # --------- MODELS / CONTROLLERS ----------
        self.face_model = FaceModel()
        self.attendance = AttendanceController(self.table)

        # --------- UI ELEMENTS ----------
        self.video_label = QLabel()
        self.video_label.setFixedSize(640, 480)
        self.video_label.setStyleSheet("background-color: black;")

        self.status_label = QLabel("Idle")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.collect_btn = QPushButton("Collect New Student Data")
        self.attendance_btn = QPushButton("Take Attendance")
        self.stop_btn = QPushButton("Stop")
        self.openFolderBtn = QPushButton("Open Attendance Folder")

        # give table to attendance controller
        # self.attendance.set_table(self.table)

        # --------- LAYOUT ----------
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.video_label)
        left_layout.addWidget(self.status_label)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.table)
        right_layout.addWidget(self.collect_btn)
        right_layout.addWidget(self.attendance_btn)
        right_layout.addWidget(self.stop_btn)
        right_layout.addWidget(self.openFolderBtn)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        # --------- CAMERA THREAD ----------
        self.camera = CameraThread(self.face_model)
        self.camera.frame_ready.connect(self.update_frame)
        self.camera.attendance_signal.connect(
            self.on_attendance,
            Qt.QueuedConnection
        )
        self.camera.start()

        # --------- BUTTON ACTIONS ----------
        self.collect_btn.clicked.connect(self.collect_dataset)
        self.attendance_btn.clicked.connect(self.start_attendance)
        self.stop_btn.clicked.connect(self.stop_all)
        self.openFolderBtn.clicked.connect(open_attendance_folder)

    # ==========================================
    #               CAMERA DISPLAY
    # ==========================================
    def update_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(
            rgb.data, w, h, bytes_per_line, QImage.Format_RGB888
        )
        self.video_label.setPixmap(
            QPixmap.fromImage(qt_img).scaled(
                self.video_label.size(), Qt.KeepAspectRatio
            )
        )

    # ==========================================
    #               ATTENDANCE
    # ==========================================
    def start_attendance(self):
        if not self.face_model.has_registered_students():
            QMessageBox.warning(
                self,
                "No Registered Students",
                "No registered student data found.\n"
                "Please collect new student data before taking attendance."
            )
            self.status_label.setText(
                "No registered students. Please collect data first."
            )
            return

        self.camera.start_attendance()
        self.status_label.setText("Attendance running...")

    def on_attendance(self, name):
        self.attendance.mark(name)

    # ==========================================
    #           DATASET COLLECTION
    # ==========================================
    def collect_dataset(self):
        name, ok = QInputDialog.getText(
            self,
            "New Student",
            "Enter student name:"
        )

        if not ok or not name.strip():
            QMessageBox.warning(self, "Cancelled", "Student name is required.")
            return

        self.camera.start_collect(name.strip())
        self.status_label.setText("Collecting new student data (5s)...")

    # ==========================================
    #               STOP
    # ==========================================
    def stop_all(self):
        self.camera.stop_attendance()
        self.status_label.setText("Stopped")

    # ==========================================
    #               CLEAN EXIT
    # ==========================================
    def closeEvent(self, event):
        self.camera.stop()
        event.accept()
