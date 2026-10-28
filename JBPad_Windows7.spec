# -*- mode: python ; coding: utf-8 -*-

import os
import shutil

from PyInstaller.building.datastruct import Target

block_cipher = None

# --- пути ---
project_dir = os.path.abspath(".")
resources_dir = os.path.join(project_dir, "resources")
data_dir = os.path.join(project_dir, "Data")


a = Analysis(
    ['JBPad.py'],
    pathex=[project_dir],
    binaries=[],

    datas=[
        (resources_dir, 'resources'),
    ],

    hiddenimports=[
        'PyQt5.sip',  # нужен для стабильной сборки PyQt
    ],

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],

    # Убираем лишнее
    excludes=[
        # Qt модули
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

        # Тяжёлые Python-библиотеки
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'tkinter',
    ],

    noarchive=True,   # быстрее холодный старт
    optimize=2,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='JBPad',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    contents_directory='_Windows7+_x32',
    icon='resources/icons/JBPad_windowicon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='JBPad',
)


class CopyDataFolder(Target):
    """Копирует каталог Data целиком рядом с exe (не в _internal)."""

    def __init__(self, coll_target, app_name='JBPad'):
        super().__init__()
        self.coll = coll_target
        self.app_name = app_name
        self.dependencies = [coll_target]
        self.__postinit__()

    _GUTS = (
        ('app_name', None),
    )

    def _check_guts(self, data, last_build):
        return True

    def assemble(self):
        dist_dir = os.path.join(DISTPATH, self.app_name)
        src = data_dir
        dst = os.path.join(dist_dir, 'Data')
        if not os.path.isdir(src):
            print(f"CopyDataFolder: skip (no source): {src}")
            return []
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"CopyDataFolder: copied {src} -> {dst}")
        return []


copy_data = CopyDataFolder(coll)
