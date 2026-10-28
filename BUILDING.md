# Building JBPad

This document describes how to build JBPad from source and prepare the platform components used in the official distributions, including the combined **All_OS** package.

## Contents

- [Overview](#overview)
- [Build environments](#build-environments)
- [Before building](#before-building)
- [Build commands](#build-commands)
- [Understanding the build outputs](#understanding-the-build-outputs)
- [Preparing platform components](#preparing-platform-components)
- [Assembling All_OS](#assembling-all_os)
- [Important notes](#important-notes)

## Overview

JBPad uses one shared Python source file, `JBPad.py`, for Windows, Linux, and macOS. The repository provides six PyInstaller specification files (`.spec`): two for Windows, two for Linux, and two for macOS.

- **`onedir`** builds collect the executable and its dependencies into a directory or application bundle.
- **`onefile`** builds package the executable and its dependencies into a single executable. On macOS, the result is still an `.app` application bundle.

The Linux and macOS `onefile` builds are used as components of **All_OS**. They are not, by themselves, complete All_OS distributions.

## Build environments

Build on the target operating system using a compatible Python and PyInstaller environment. These specifications are not a cross-compilation system.

The following versions are the environments in which the project builds were tested:

| Target | Tested environment |
|---|---|
| Windows 7+ x86 | Windows 7, Python 3.8.10 x86, PyQt5 5.15.2 / Qt 5.15.2, PyInstaller 6.22.3 |
| Windows 10+ x64 | Windows 10 22H2, Python 3.11.9 x64, PyQt5 5.15.11 / Qt 5.15.2, PyInstaller 6.18.0 |
| Linux | Linux Mint 22.2 x86_64, Python 3.12.3, PyQt5 5.15.11 / Qt 5.15.19, PyInstaller 6.22.0 |
| macOS | macOS Ventura 13.2 x86_64, Python 3.11.15, PyQt5 5.15.11 / Qt 5.15.19, PyInstaller 6.22.0 |

The project was also tested at runtime on Windows 7, 10, and 11; Linux Mint 22.2 (X11) and Fedora Workstation 44 (X11 and Wayland); and macOS Ventura 13.2 and Sequoia 15.1. Runtime testing on these systems does not mean every listed system was used to build every distribution.

Python 3.8.10 was used for the Windows 7 x86 build because it was the last Python release supporting Windows 7. The Windows 7 build environment is separate from the newer Windows build environment.

In the project's observed builds, Python 3.11.9–3.12.3 and PyInstaller 6.18.0–6.22.3 worked without noticeable differences for Windows 10+, Linux, and macOS. This is an observation from the tested environments, not a guarantee that all combinations of these versions are interchangeable.

A virtual environment (`venv`) can be used to isolate project dependencies, but it is not inherently required by the `.spec` files. Install Python, PyQt5, and PyInstaller in the environment you intend to use for the build.

## Before building

1. Install a compatible Python version on the target operating system.
2. Install PyQt5 and PyInstaller in the Python environment used for the build.
3. Make sure the repository has the expected root-level items:
   - `JBPad.py`
   - `Data/` — required for `onedir` builds; `onefile` builds do not copy it.
   - `resources/`
   - `build/`
4. Open a terminal in the **repository root** — the directory containing `JBPad.py`.

The specifications use the current working directory to locate project files. Running them from a different directory can cause paths to resolve incorrectly.

## Build commands

Run the appropriate command from the repository root.

### Windows 7+ x86

```bash
python -m PyInstaller --clean --noconfirm build/Windows/JBPad_Windows7.spec
```

Use a compatible 32-bit Windows 7 build environment.

### Windows 10+ x64

```bash
python -m PyInstaller --clean --noconfirm build/Windows/JBPad_Windows10.spec
```

### Linux — `onedir`

```bash
python -m PyInstaller --clean --noconfirm build/Linux/JBPad_Linux.spec
```

### Linux — `onefile`

```bash
python -m PyInstaller --clean --noconfirm build/Linux/JBPad_Linux_onefile.spec
```

### macOS — `onedir`

```bash
python -m PyInstaller --clean --noconfirm build/macOS/JBPad_macOS.spec
```

### macOS — `onefile`

```bash
python -m PyInstaller --clean --noconfirm build/macOS/JBPad_macOS_onefile.spec
```

If `python` does not launch the environment containing the required dependencies, specify the appropriate Python interpreter. For example, on Windows, use `py -3.11 -m PyInstaller` or the full path to the required interpreter.

PyInstaller writes build artifacts under `build/` and distribution output under `dist/` by default. The exact internal layout depends on the PyInstaller version and the specification; use the actual build output and the table below as a guide.

## Understanding the build outputs

| Specification | Build type | Target | Main output | `Data/` handling |
|---|---|---|---|---|
| `build/Windows/JBPad_Windows7.spec` | `onedir` | Windows 7+ x86 | `dist/JBPad/`, including `JBPad.exe` and `_Windows7+_x32/` | Copies source `Data/` to `dist/JBPad/Data/` |
| `build/Windows/JBPad_Windows10.spec` | `onedir` | Windows 10+ x64 | `dist/JBPad/`, including `JBPad.exe` and `_Windows10+_x64/` | Copies source `Data/` to `dist/JBPad/Data/` |
| `build/Linux/JBPad_Linux.spec` | `onedir` | Linux | `dist/JBPad/`, including the `JBPad` executable and dependencies | Copies source `Data/` to `dist/JBPad/Data/` |
| `build/Linux/JBPad_Linux_onefile.spec` | `onefile` | Linux | `dist/JBPad` executable | Does not copy `Data/` |
| `build/macOS/JBPad_macOS.spec` | `onedir` | macOS | `dist/JBPad.app/` and `dist/Data/` | Copies source `Data/` to `dist/Data/` |
| `build/macOS/JBPad_macOS_onefile.spec` | `onefile` | macOS | `dist/JBPad.app/` | Does not copy `Data/` |

All six specifications include `resources/` in the PyInstaller build and explicitly include the hidden import `PyQt5.sip`. The exact location of bundled resources within a distribution can vary with the PyInstaller layout; do not assume `resources/` must sit beside the executable.

The specifications do **not** copy `Setting.ini` or the license files. Those are added separately when preparing the distribution.

### Rebuilding and `Data/`

The `Data/` directory inside `onedir` build outputs is recreated during a build; changes in that copy should not be used as permanent data storage.

The Linux and macOS `onefile` specifications intentionally do not copy `Data/`. These executables are used as components when assembling All_OS, which has one shared `Data/` directory.

## Preparing platform components

The names produced by PyInstaller are build names, not necessarily the final release names. For the official All_OS package, prepare the components as follows:

| Platform | Component to include in All_OS | Source build |
|---|---|---|
| macOS | `JBPad_macOS.app/` | macOS `onefile` build (`dist/JBPad.app/`, renamed for release) |
| Linux | `JBPad_Linux` | Linux `onefile` build (`dist/JBPad`, renamed for release) |
| Windows 10+ x64 | `_Windows10+_x64/` and `JBPad_x64.exe` | Windows 10+ `onedir` build |
| Windows 7+ x86 | `_Windows7+_x32/` and `JBPad_x32.exe` | Windows 7+ `onedir` build |

For Windows, the `.spec` files create an executable named `JBPad.exe`; the release-preparation step renames it to `JBPad_x64.exe` or `JBPad_x32.exe`. For Linux, the `onefile` executable is created as `JBPad` and renamed to `JBPad_Linux`. For macOS, the bundle is created as `JBPad.app` and renamed to `JBPad_macOS.app`.

These suffixes are release-packaging conventions. They do not change the program's source code or, by themselves, its behavior.

## Assembling All_OS

All_OS combines the platform-specific components listed above with shared files. It is assembled from the outputs of the relevant platform builds; it is not generated by any single `.spec` file.

The shared items are:

- `Data/`
- `LICENSE`
- `LGPL-3.0.txt`
- `Licenses.txt`
- `Setting.ini` (optional, but included in the official distribution)

Use the platform-specific executable and dependency components from their respective builds. Take shared items from the repository root or from the prepared release files. The `Data/` directory is shared by all platforms and should appear only once at the common level of the All_OS distribution. A single common copy of `Data/` is sufficient.

The `resources/` directory is a shared source input used by the platform builds and is included by the specifications. It is not listed as a separate common external item in the All_OS layout above.

## Important notes

- Build on the target operating system with a compatible environment; these specifications do not provide cross-compilation.
- Run PyInstaller commands from the repository root.
- Do not assume that the `onedir` output is a single executable; its dependencies are part of the distribution.
- The Linux and macOS `onefile` outputs are components for All_OS, not complete All_OS packages.
- `Setting.ini` and the license files must be added separately during release preparation.
- Creating a Windows installer is optional. Instructions for using the configured CreateInstall project are provided in [`README.md`](packaging/Windows/CreateInstall/README.md) and [`README.ru.md`](packaging/Windows/CreateInstall/README.ru.md).