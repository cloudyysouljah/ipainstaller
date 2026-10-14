import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase
from app_controller import AppController

if __name__ == "__main__":
	style = open("graphic/app_style.css", "r").read()

	app = QApplication(sys.argv)
	font_id = QFontDatabase.addApplicationFont("graphic/fnt_dotumche.ttf")
	app.setStyleSheet(style)

	appController = AppController()
	appController.start()

	sys.exit(app.exec())