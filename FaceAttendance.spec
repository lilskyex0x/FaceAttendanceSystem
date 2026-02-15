# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [
    ('haarcascade_frontalface_default.xml', '.'),
    ('encodings.pickle', '.'),
]
binaries = []
hiddenimports = ['face_attendence', 'face_attendence.controller', 'face_attendence.model', 'face_attendence.view']

tmp_ret = collect_all('face_recognition')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

tmp_ret = collect_all('face_recognition_models')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

tmp_ret = collect_all('dlib')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='FaceAttendance',
    debug=False,
    strip=False,
    upx=True,
    console=False
)


app = BUNDLE(
    exe,
    name='FaceAttendance.app',
    icon=None,
    bundle_identifier='com.lilsnow.faceattendance',
    info_plist={
        'NSCameraUsageDescription':
            'FaceAttendance needs camera access to recognize faces for attendance.'
    }
)

