import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc
import os

import graphic.auth_dialog as auth_dialog

class MainWindow(qtw.QWidget):
	closeSignal = qtc.pyqtSignal()
	authSignal = qtc.pyqtSignal(str, str)
	def __init__(self):
		super().__init__()
		self.setWindowTitle("ipa-installer")
		self.setWindowIcon(qtg.QIcon("icon.ico"))
		self.authDialog = auth_dialog.AuthDialog()
		self.initUI()
		self.connectButtons()
		# self.connectSignals()

	def initUI(self):
		self.mainLayout = qtw.QVBoxLayout()
		# Device layout
		self.deviceTitle = qtw.QLabel("Device")
		# self.deviceTitleLayout.addWidget(self.deviceTitle)

		self.deviceFrame = qtw.QFrame()
		self.deviceFrame.setProperty("class", "device")
		self.deviceLayout = qtw.QVBoxLayout(self.deviceFrame)
		self.deviceLabel = qtw.QLabel("Device not connected")
		self.deviceModel = qtw.QLabel("Model: - ")
		# self.deviceLabel.addLayout(self.deviceTitleLayout)
		self.deviceLayout.addWidget(self.deviceTitle, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
		self.deviceLayout.addWidget(self.deviceLabel)
		self.deviceLayout.addWidget(self.deviceModel)

		# Buttons layout 
		self.buttonsLayout = qtw.QVBoxLayout()
		self.authButton = qtw.QPushButton("Authorization")
		self.installButton = qtw.QPushButton("Installed apps")
		self.buttonsLayout.addWidget(self.authButton)
		self.buttonsLayout.addWidget(self.installButton)

		# Logger layout 
		self.loggerLayout = qtw.QVBoxLayout()
		self.log = qtw.QTextEdit()
		self.log.setReadOnly(True)
		self.log.setProperty("class", "log")
		self.loggerLayout.addWidget(self.log)

		# Main layout
		self.setLayout(self.mainLayout)
		self.mainLayout.addWidget(self.deviceFrame)
		self.mainLayout.addLayout(self.buttonsLayout)
		self.mainLayout.addLayout(self.loggerLayout)
		self.show()

	def connectButtons(self):
		self.authButton.clicked.connect(self.authDialog.show)
		self.authDialog.accepted.connect(self.auth)
		# self.installButton.clicked.connect(InstalledAppsWindow)
	# 	self.connectedSignal.connect(self.updateDevice)

	def auth(self):
		self.authSignal.emit(self.authDialog.get_login(), self.authDialog.get_passwd())

	def updateLog(self, message):
		self.log.append(message)
		self.log.moveCursor(qtg.QTextCursor.MoveOperation.End)

	def updateDevice(self, connect_status, device_id, device_name):
		if connect_status:
			self.deviceLabel.setText(f"Device connected")
			self.deviceModel.setText(f"Model: {device_name}")
		else:
			self.deviceLabel.setText("Device not connected")
			self.deviceModel.setText(f"Model: -")

	def closeEvent(self, event):
		self.closeSignal.emit()
		event.accept()