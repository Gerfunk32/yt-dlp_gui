# main.py

import sys
import os
import platform
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from downloader import YTDLPDownloader

def main():
    app = QApplication(sys.argv)

    # Set window icon
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "DLPICON.png")
    print(f"Looking for icon at: {icon_path}")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        print("Found Icon")
    else:
        print("Icon not found.")

    if platform.system() == "Windows":
        print("Dos Based Execution")
    else:
        print("Unix Based Execution")

    window = YTDLPDownloader()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
