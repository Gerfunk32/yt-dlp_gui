import os
import platform
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QTextEdit, QMessageBox, QLabel, QCheckBox, QFileDialog
)
from PyQt5.QtCore import QProcess, Qt, QUrl
from PyQt5.QtGui import QFont, QDesktopServices
from style import dark_theme

class YTDLPDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YT-DLP GUI")
        self.setGeometry(100, 100, 700, 420)
        self.setStyleSheet(dark_theme)

        self.last_download_path = None
        self.download_folder = self.get_default_folder()

        # Layouts
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Header
        header = QLabel("🎬 Download MP4 or MP3 from YouTube")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste video URL here...")
        self.url_input.setFont(QFont("Arial", 12))
        main_layout.addWidget(self.url_input)

        # Buttons
        self.download_mp4_btn = QPushButton("Download MP4")
        self.download_mp3_btn = QPushButton("Download MP3")
        button_layout.addWidget(self.download_mp4_btn)
        button_layout.addWidget(self.download_mp3_btn)
        main_layout.addLayout(button_layout)

        # Folder Picker
        self.choose_folder_btn = QPushButton("Choose Download Folder")
        self.choose_folder_btn.clicked.connect(self.choose_download_folder)
        main_layout.addWidget(self.choose_folder_btn)

        # Checkbox
        self.open_folder_checkbox = QCheckBox("Open folder when done")
        self.open_folder_checkbox.setChecked(True)
        main_layout.addWidget(self.open_folder_checkbox)

        # Status Output
        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        main_layout.addWidget(self.status_output)

        self.setLayout(main_layout)

        # QProcess
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)
        self.process.finished.connect(self.download_finished)

        # Connect buttons
        self.download_mp4_btn.clicked.connect(self.download_mp4)
        self.download_mp3_btn.clicked.connect(self.download_mp3)

    def get_default_folder(self):
        return os.path.expanduser("~/Music")

    def choose_download_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", self.download_folder)
        if folder:
            self.download_folder = folder
            self.status_output.append(f"📁 Download folder set to: {self.download_folder}")

    def download_mp4(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter a video URL.")
            return
        output_path = os.path.join(self.download_folder, "%(title)s.%(ext)s")
        command = f'yt-dlp -f mp4 -o "{output_path}" "{url}"'
        self.run_command(command)

    def download_mp3(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter a video URL.")
            return
        output_path = os.path.join(self.download_folder, "%(title)s.%(ext)s")
        command = f'yt-dlp -x --audio-format mp3 -o "{output_path}" "{url}"'
        self.run_command(command)

    def run_command(self, command):
        self.status_output.append(f"▶ Running: {command}")
        if platform.system == "Windows":
            self.process.start("cmd", ["-c", command])  # Uses "cmd" on Windows
        else:
            self.process.start("bash", ["-c", command])  # Uses "bash" on Linux & macOS

    def read_stdout(self):
        output = bytes(self.process.readAllStandardOutput()).decode("utf-8")
        self.status_output.append(output)

    def read_stderr(self):
        error = bytes(self.process.readAllStandardError()).decode("utf-8")
        self.status_output.append(error)

    def download_finished(self):
        self.status_output.append("✅ Download finished.")
        if self.open_folder_checkbox.isChecked():
            folder_url = QUrl.fromLocalFile(self.download_folder)
            QDesktopServices.openUrl(folder_url)
