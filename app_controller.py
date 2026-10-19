import sys
from PyQt6.QtCore import QObject
from graphic.main_window import MainWindow
# from graphic.installed_apps_window import InstalledAppsWindow
# from graphic.auth_dialog import AuthDialog
from core.handler import IphoneManager

class AppController(QObject):
	def __init__(self):
		super().__init__()

		self.mainWindow = MainWindow()
		self.manager = IphoneManager(sys.platform)

		self.connectSignals()

	def connectSignals(self): 
		self.manager.connectedSignal.connect(self.mainWindow.updateDevice)
		self.manager.logSignal.connect(self.mainWindow.updateLog)

		self.mainWindow.closeSignal.connect(self.manager.stop)
		# self.mainWindow.authSignal.connect(self.manager.authDevice)

	def start(self):
		self.mainWindow.show()
		self.manager.start()