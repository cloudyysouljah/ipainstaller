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

	mainWindow = MainWindow()
	mainWindow.show()

	manager = IphoneManager("linux")
	manager.connectedSignal.connect(mainWindow.updateDevice)
	manager.logSignal.connect(mainWindow.updateLog)
	mainWindow.closeSignal.connect(manager.stop)
	mainWindow.authSignal.connect(manager.authDevice)
	manager.start()

	sys.exit(app.exec())