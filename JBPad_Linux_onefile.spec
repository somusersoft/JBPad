# -*- mode: python ; coding: utf-8 -*-

import os
import shutil

from PyInstaller.building.build_main import Analysis, PYZ, EXE


block_cipher = None

project_dir = os.path.abspath(".")
resources_dir = os.path.join(project_dir, "resources")


a = Analysis(
    ['JBPad.py'],
    pathex=[project_dir],
    binaries=[],

    datas=[
        (resources_dir, 'resources'),
    ],

    hiddenimports=[
        'PyQt5.sip',
    ],

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],

    excludes=[
        'PyQt5.QtSvg',
        'PyQt5.QtQml',
        'PyQt5.QtQuick',
        'PyQt5.QtWebSockets',
        'PyQt5.QtSql',
        'PyQt5.QtPrintSupport',
        'PyQt5.QtOpenGL',
        'PyQt5.QtTest',
        'PyQt5.QtDesigner',
        'PyQt5.QtHelp',
        'PyQt5.QtWebEngine',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebChannel',

        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'tkinter',
    ],

    noarchive=True,
    optimize=2,
)


pyz = PYZ(
    a.pure,
    cipher=block_cipher
)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='JBPad',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
)