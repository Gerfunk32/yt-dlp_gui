
import sys
import os
import platform
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QFont

def create_linux_desktop_entry(save_path, app_dir):
    icon_src = os.path.join(app_dir, "DLPICON.png")
    desktop_entry = f"""[Desktop Entry]
Name=YT-DLP GUI
Comment=Download MP4 or MP3 via yt-dlp
Exec=python3 {app_dir}/main.py
Icon={icon_src}
Terminal=false
Type=Application
Categories=AudioVideo;Utility;
"""
    with open(save_path, "w") as f:
        f.write(desktop_entry)
    os.chmod(save_path, 0o755)

def create_windows_shortcut(save_path, app_dir):
    import winshell
    from win32com.client import Dispatch
    target = os.path.join(app_dir, "main.py")
    icon = os.path.join(app_dir, "DLPICON.ico")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(save_path)
    shortcut.Targetpath = "python.exe"
    shortcut.Arguments = f'"{target}"'
    shortcut.WorkingDirectory = app_dir
    shortcut.IconLocation = icon if os.path.exists(icon) else target
    shortcut.save()

class ShortcutInstaller(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Install YT-DLP GUI Shortcut")
        self.setGeometry(300, 300, 400, 180)

        layout = QVBoxLayout()
        self.label = QLabel("Choose where to create your launcher shortcut:")
        self.label.setFont(QFont("Arial", 12))
        layout.addWidget(self.label)

        self.button = QPushButton("Select Install Location")
        self.button.clicked.connect(self.select_location)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def select_location(self):
        app_dir = os.path.abspath(os.path.dirname(__file__))
        platform_name = platform.system()

        if platform_name == "Windows":
            path, _ = QFileDialog.getSaveFileName(self, "Save Shortcut As", os.path.join(app_dir, "YT-DLP_GUI.lnk"), "Shortcuts (*.lnk)")
            if path:
                create_windows_shortcut(path, app_dir)
                QMessageBox.information(self, "Success", "✅ Windows shortcut created.")
        else:
            path, _ = QFileDialog.getSaveFileName(self, "Save Desktop Entry As", os.path.join(app_dir, "yt-dlp-gui.desktop"), "Desktop Entry (*.desktop)")
            if path:
                create_linux_desktop_entry(path, app_dir)
                QMessageBox.information(self, "Success", "✅ Linux desktop launcher created.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    installer = ShortcutInstaller()
    installer.show()
    sys.exit(app.exec_())
