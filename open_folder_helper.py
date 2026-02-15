import sys
from pathlib import Path
import subprocess

def open_attendance_folder():
    folder = Path.home() / "Documents" / "FaceAttendance"
    folder.mkdir(parents=True, exist_ok=True)

    if sys.platform == "darwin":          # macOS
        subprocess.run(["open", folder])
    elif sys.platform == "win32":         # Windows
        subprocess.run(["explorer", folder])
    else:                                 # Linux
        subprocess.run(["xdg-open", folder])
