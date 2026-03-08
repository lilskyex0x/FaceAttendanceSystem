# Face Attendance System

Desktop-based **Face Attendance System** built with **PyQt5**, **OpenCV**, and **face_recognition**.  
The app uses a webcam to detect and recognize faces in real time, then logs attendance to a CSV file with name, date, and time.

---

## Features

- **Real-time recognition**: webcam preview with live face detection and name overlays.
- **Student enrollment**: collect a short video sample and generate face encodings for each student.
- **Automatic attendance logging**:
  - Attendance saved as CSV (`Name, Date, Time`).
  - Duplicate attendance for the same person is prevented within a session.
- **Desktop UI**:
  - PyQt5 interface with video preview, attendance table, and control buttons.
  - Custom color theme defined via Qt style sheets.

---

## Tech Stack

- **Language**: Python 3.9+
- **GUI**: PyQt5
- **Computer Vision**: OpenCV (`opencv-python`)
- **Face Recognition**: `face_recognition` (dlib-based)
- **Packaging (macOS)**: PyInstaller (`FaceAttendance.spec` + `Info.plist`)

---

## Project Structure

```text
face_attendance/
│
├── controller/               # Application controllers
│   ├── camera_thread.py      # Webcam capture + recognition loop (QThread)
│   ├── attendance_controller.py  # Attendance table + CSV writer
│   ├── dataset_controller.py     # Legacy dataset collector (unused)
│   └── encode_worker.py          # Legacy encoder worker (unused)
│
├── model/
│   └── face_model.py         # Face detection, encodings, and recognition logic
│
├── view/
│   ├── main_window.py        # Main PyQt5 window and layout
│   └── styles.py             # Global UI theme (Qt style sheet)
│
├── main.py                   # Application entry point
├── open_folder_helper.py     # Helper to open attendance folder in OS file manager
├── FaceAttendance.spec       # PyInstaller spec for macOS app bundle
├── Info.plist                # macOS bundle metadata (camera usage description)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/lilskyex0x/FaceAttendanceSystem.git
cd FaceAttendanceSystem
```

### 2. (Recommended) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
# On Windows (PowerShell):
# .venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note**: Installing `face_recognition` may require C/C++ build tools and `dlib`.  
> On macOS, ensure you have Xcode command line tools installed.

---

## Running the Application

From the project root:

```bash
python main.py
```

The main window will open with:

- A **live camera preview** on the left.
- An **attendance table** and control buttons on the right.

On first launch, your OS may ask for **camera permission**—you must allow it.

---

## Usage

### 1. Enroll a new student

1. Click **“Collect New Student Data”**.
2. Enter the student’s name.
3. The camera will collect face samples for about **5 seconds**.
4. Cropped face images and face encodings are saved for that student.

> If no face is detected during collection, no samples will be saved.

### 2. Take attendance

1. Make sure at least one student has been enrolled.
2. Click **“Take Attendance”**.
3. When a known face is recognized:
   - A bounding box and name are shown on the video preview.
   - The student is added **once per session** to the attendance table and CSV.
4. Click **“Stop”** to stop attendance mode.

### 3. View attendance records

- Click **“Open Attendance Folder”** in the UI to open the folder where attendance is stored.
- Attendance is saved as a CSV file with columns:
  - `Name`
  - `Date` (`YYYY-MM-DD`)
  - `Time` (`HH:MM:SS`)

---

## Data Storage

- **Face data (images + encodings)**:
  - Stored under a per-user application directory in your home folder.
- **Attendance CSV**:
  - Stored under your documents folder in a dedicated `FaceAttendance` directory.

These files are stored **unencrypted** on the local machine and should be treated as sensitive data.

---

## Development Notes

- The repository uses a **Git branching model**:
  - `develop` – active development branch (default).
  - `main` – stable branch for releases.
- Legacy helper modules (`dataset_controller.py`, `encode_worker.py`) are kept for reference but not used by the current UI flow.

---

## Future Improvements

- Cloud-based attendance synchronization (e.g., Firebase, Supabase, or custom API).
- Multi-classroom / multi-camera support.
- Deep learning–based detection/recognition pipeline.
- User management (roles, admin panel, and deletion of face data).
- Cross-platform installers (Windows, Linux).

---

## Author

**Aung Pyae Khant**  
Student ID: 2405270013  
Software Program Capstone Project  
Stamford International University

