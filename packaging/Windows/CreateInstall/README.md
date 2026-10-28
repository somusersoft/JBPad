# CreateInstall --- Windows Installer Projects

This directory contains CreateInstall projects for building Windows
installers for JBPad, along with the source files used by those
projects.

The installers are optional convenience packages for Windows users.
JBPad itself is a portable application and does not require an
installer.

**Installer authoring tool:** CreateInstall Free 8.11.2\
**Download:** https://www.createinstall.com/download-free-trial.html

## Contents

- [Installer features](#installer-features)
- [Building the JBPad installers](#building-the-jbpad-installers)
- [Adapting the projects for another
  application](#adapting-the-projects-for-another-application)
  - [1. Prepare the files](#1-prepare-the-files)
  - [2. Edit the project settings](#2-edit-the-project-settings)
  - [3. Edit the installation
    script](#3-edit-the-installation-script)
  - [4. Build and test the
    installer](#4-build-and-test-the-installer)
- [Uninstallation and user data](#uninstallation-and-user-data)

## Installer features

The projects implement a simple installation workflow for a desktop
application:

1. Language selection.
2. Installation-folder selection.
3. Installation completion, with an option to launch the application.

The installer extracts the application files to the selected folder and
creates a desktop shortcut. It does not write to the Windows registry.

The uninstaller is included in the installed application folder. Its
handling of the application's `Data/` directory is described in
[Uninstallation and user data](#uninstallation-and-user-data).

## Building the JBPad installers

Install CreateInstall Free 8.11.2, then:

1. Open the project file for the required architecture:
   - `installer_JBpad32.ci` for the 32-bit Windows package.
   - `installer_JBpad64.ci` for the 64-bit Windows package.
2. Click **Create Installation** (the exact label may vary with the
   CreateInstall interface language).
3. Wait for the build to finish.

The resulting installer is placed in the `build/` directory.

The project uses relative paths, so it is not tied to a particular
absolute directory on the original developer's computer.

## Adapting the projects for another application

These projects can be used as a starting point for packaging another
Windows desktop application. You will need to replace the JBPad files
and update the project settings.

The examples below use `MyApp` as a placeholder application name. The
names and labels of some CreateInstall settings may differ depending on
the interface language or version.

### 1. Prepare the files

1. Copy the entire `CreateInstall` directory to a convenient location.
2. Remove the JBPad application files from `source/` and place the
   files required by your application there. Depending on your
   application, these may include:
   - the executable file;
   - additional application directories and resources;
   - configuration files;
   - the application's `.ico` file;
   - license and third-party notices, where applicable.
3. Create a separate icon for the installer and place it in the root of
   the copied `CreateInstall` directory.

The installer icon is used by the installation wizard and is displayed
for the installer file in Windows File Explorer. According to the
CreateInstall documentation, the icon should not exceed 64 × 64 pixels.
A multi-size `.ico` containing 16 × 16, 24 × 24, 48 × 48, and 64 × 64
images is recommended.

The application icon and installer icon serve different purposes: the
application icon can be used for the desktop shortcut, while the
installer icon represents the installer itself.

### 2. Edit the project settings

Open the relevant `.ci` project file in CreateInstall.

Replace the JBPad-specific values with values for your application.

#### Project tab --- Output

Change the name of the generated installer.

For example:

`JBPad_1.0_Windows7+_x32_setup.exe` → `MyApp_setup.exe`

#### Project tab --- Program information

Change the displayed application name.

For example:

`JBPad 1.0` → `MyApp`

#### Project tab --- Installation

Change the default installation path.

For example:

`#userpath#\JBPad_Windows7+_x32` → `#userpath#\folder_for_MyApp`

In CreateInstall, the global variable `#userpath#` refers to the user
path, documented as `C:\Users\User\` (with the actual Windows user name
in place of `User`). The example therefore places the application in a
separate `folder_for_MyApp` directory under that path.

### 3. Edit the installation script

Open the **Installation Script** tab. The settings described below are
in the tree in the middle of the window, under the root item named
**Installation**.

#### Installation --- Icon file

Set the **Icon file** parameter to the installer icon you created.

For example:

`$prjpath$\JBPad_setup.ico` → `$prjpath$\MyApp_setup.ico`

This example assumes that `MyApp_setup.ico` is in the root of the copied
`CreateInstall` directory.

#### Requirements check

Choose the oldest Windows version supported by your application. If
necessary, update the error message.

If the installer is launched on an unsupported version of Windows, the
message is displayed and installation is stopped.

#### Installation path dialog --- Add folder when selecting

Change the **Add folder when selecting** value to the name of the
application directory.

For example:

`JBPad_Windows7+_x32` → `folder_for_MyApp`

If the user selects `C:\` as the base path, the installer appends the
folder name and proposes `C:\folder_for_MyApp`.

#### Installation files

Remove the JBPad file entries and add the files for your application
from `source/`.

Relative paths using the CreateInstall project-path variable `$prjpath$`
are recommended. They make the project easier to move to another
computer or directory without editing every path.

For example, this absolute path:

`D:\Temp\CreateInstall\source\MyApp.ico`

can be expressed as:

`$prjpath$\source\MyApp.ico`

This example assumes that `source/` is directly inside the project
directory.

#### Create shortcut

Update the desktop-shortcut settings. For example:

- **Shortcut name:** `JBPad_x32` → `MyApp`
- **File name:** `JBPad_x32.exe` → `MyApp.exe`
- **Icon file:** `JBPad.ico` → `MyApp.ico`

Use the actual names of the files that will be installed. The shortcut
icon should point to the `.ico` file for your application.

#### Launch application

Change the executable name to the file that will be installed.

For example:

`JBPad_x32.exe` → `MyApp.exe`

This must refer to the installed application executable, not to the
installer.

### 4. Build and test the installer

Check that all referenced files exist and that the project paths point
to the correct locations.

Click **Create Installation** and wait for the build to finish. The
generated installer will appear in `build/`.

## Uninstallation and user data

The `Data/` directory contains the application's localization files,
themes, help files, and user-created notebooks.

During uninstallation, the installer removes the application files and
desktop shortcut. If the user has not created any files of their own in
`Data/`, the uninstaller removes `Data/` and the application directory
completely.

If the user has created at least one file in `Data/`, the uninstaller
removes the other application files but preserves the user-created file
or files and the `Data/` directory containing them. As a result, the
remaining directory should contain the user-created data rather than the
application's bundled localization, theme, or help files.

This behavior is intentional and helps protect user-created notebooks
from accidental loss. After uninstalling the application, inspect any
remaining `Data/` directory and copy the files you want to keep before
deleting it manually.

## Notes

- CreateInstall Free 8.11.2 was used to create the JBPad installer
  projects.
- These projects are optional packaging examples; CreateInstall is not
  required to build or run JBPad itself.
- When adapting the projects, check the applicable licenses for your
  application, bundled libraries, and packaging tools.
