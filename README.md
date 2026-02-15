# Face Attendance System

A desktop-based **Face Attendance System** that automatically records attendance using real-time face recognition. The application detects faces from a webcam, identifies registered users, and logs attendance with date and time.

---

## Features

* Real-time face detection and recognition
* Student registration (dataset collection)
* Automatic attendance logging (CSV format)
* Duplicate attendance prevention within the same session
* Simple desktop graphical interface (PyQt5)

---

## Project Structure

```
face_attendance/
│
├── controller/        # Camera, dataset, and attendance controllers
├── model/             # Face recognition logic
├── view/              # GUI components
│
├── haarcascade_frontalface_default.xml
├── main.py
├── requirements.txt
└── README.md
```

---

## Requirements

* Python 3.9+
* Webcam

Install required libraries:

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python main.py
```

---

## How It Works

1. Register a new student by collecting face samples.
2. The system generates facial encodings and stores them.
3. During attendance mode, the webcam detects faces in real time.
4. Recognized students are automatically recorded in the attendance file.

---

## Output

Attendance records are saved in CSV format containing:

* Student Name
* Date
* Time

---

## Future Improvements

* Cloud-based attendance storage
* Multi-classroom camera support
* Deep learning–based detection models
* Mobile integration

---

## Author

Aung Pyae Khant, 
StudentID : 2405270013,
Software Program Capstone Project,
( Stamford International University )


