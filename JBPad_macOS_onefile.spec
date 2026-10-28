# -*- mode: python ; coding: utf-8 -*-

import os
import shutil


PROJECT_DIR = os.getcwd()

MAIN_SCRIPT = os.path.join(
    PROJECT_DIR,
    "JBPad.py"
)

RESOURCES_DIR = os.path.join(
    PROJECT_DIR,
    "resources"
)

DATA_DIR = os.path.join(
    PROJECT_DIR,
    "Data"
)


# ------------------------------------------------------------
# Hidden imports
# ------------------------------------------------------------

hiddenimports = [
    "PyQt5.sip",
]


# ------------------------------------------------------------
# Исключаем ненужные модули
# ------------------------------------------------------------

excludes = [
    # Ненужные модули Qt
    "PyQt5.QtSvg",
    "PyQt5.QtQml",
    "PyQt5.QtQuick",
    "PyQt5.QtWebEngine",

    # Не используемые в JBPad библиотеки
    "matplotlib",
    "numpy",
    "scipy",
    "pandas",
    "tkinter",
]


# ------------------------------------------------------------
# Ресурсы ВСТРАИВАЮТСЯ внутрь onefile
# ------------------------------------------------------------

datas = [
    (
        RESOURCES_DIR,
        "resources",
    ),
]


# ------------------------------------------------------------
# Analysis
# ------------------------------------------------------------

a = Analysis(
    [MAIN_SCRIPT],
    pathex=[PROJECT_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=True,
    optimize=2,
)


# ------------------------------------------------------------
# Python archive
# ------------------------------------------------------------

pyz = PYZ(
    a.pure
)


# ------------------------------------------------------------
# Onefile executable
#
# В отличие от onedir:
# binaries и datas включаются непосредственно в EXE.
# ------------------------------------------------------------

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="JBPad",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
)


# ------------------------------------------------------------
# macOS .app
# ------------------------------------------------------------

app = BUNDLE(
    exe,
    name="JBPad.app",
    icon=os.path.join(PROJECT_DIR, "resources", "icons", "JBPad_windowicon.icns"),
    bundle_identifier="org.somuser.JBPad",
    version="1.0",
    info_plist={
        "CFBundleName": "JBPad",
        "CFBundleDisplayName": "JBPad",
        "CFBundleShortVersionString": "1.0",
        "CFBundleVersion": "1.0",
        "NSPrincipalClass": "NSApplication",
        "NSAppleScriptEnabled": False,
    },
)
