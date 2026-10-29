import sys
from PyQt6.QtCore import QObject
from graphic.main_window import MainWindow
# from graphic.installed_apps_window import InstalledAppsWindow
from graphic.auth_dialog import AuthDialog
from core.handler import IphoneManager
from core.handler import SubProcess

class AppController(QObject):
	def __init__(self):
		super().__init__()

		self.mainWindow = MainWindow()
		self.manager = IphoneManager(sys.platform)
		self.subProcess = SubProcess()
		self.AuthDialog = AuthDialog()

		self.connectSignals()

	def connectSignals(self): 
		self.manager.connectedSignal.connect(self.mainWindow.updateDevice)
		self.manager.needFAsignal.connect(self.AuthDialog.createFAdialog)
		self.manager.successSignal.connect(self.mainWindow.updateAuth)
		# self.manager.logSignal.connect(self.mainWindow.updateLog)
		# self.manager

		self.mainWindow.closeSignal.connect(self.manager.stop)
		self.mainWindow.authSignal.connect(self.manager.authProcess)
		self.mainWindow.codeSignal.connect(self.manager.sendCode)

	def start(self):
		self.mainWindow.show()
		self.manager.start()