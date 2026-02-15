import csv
from datetime import datetime
from pathlib import Path

class AttendanceController:
    def __init__(self, table):
        self.table = table
        self.marked = set()

        # ✅ macOS-safe writable location
        self.data_dir = (
            Path.home()
            / "Documents" / "FaceAttendance"
        )
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.csv_path = self.data_dir / "attendance.csv"

    def mark(self, name):
        if name in self.marked:
            return

        self.marked.add(name)
        now = datetime.now()

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, self._cell(name))
        self.table.setItem(row, 1, self._cell(now.date().isoformat()))
        self.table.setItem(row, 2, self._cell(now.time().strftime("%H:%M:%S")))

        # ✅ WRITE TO USER-WRITABLE DIRECTORY
        with open(self.csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                name,
                now.date().isoformat(),
                now.time().strftime("%H:%M:%S")
            ])
            f.flush()

    def _cell(self, text):
        from PyQt5.QtWidgets import QTableWidgetItem
        return QTableWidgetItem(text)
