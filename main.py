import sys
from graphic.main_window import MainWindow
from core.handler import IphoneManager
from PyQt6.QtWidgets import QApplication 
from PyQt6.QtGui import QFontDatabase

if __name__ == "__main__":
	style = open("graphic/app_style.css", "r").read()

	app = QApplication(sys.argv)
	font_id = QFontDatabase.addApplicationFont("graphic/fnt_dotumche.ttf")
	app.setStyleSheet(style)

	main_window = MainWindow()
	main_window.show()

	manager = IphoneManager("linux")
	manager.connectedSignal.connect(main_window.updateDevice)
	manager.logSignal.connect(main_window.updateLog)
	manager.updateThread.start()

	sys.exit(app.exec())