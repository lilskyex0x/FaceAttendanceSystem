from PyQt5.QtCore import QThread, pyqtSignal
from model.face_model import FaceModel
import os

class EncodeWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, dataset_dir):
        super().__init__()
        self.dataset_dir = dataset_dir

    def run(self):
        model = FaceModel()
        for person in os.listdir(self.dataset_dir):
            folder = os.path.join(self.dataset_dir, person)
            if not os.path.isdir(folder):
                continue
            for img in os.listdir(folder):
                model.add_encoding(os.path.join(folder, img), person)
        model.save()
        self.finished.emit()
