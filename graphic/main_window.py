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
		self.setWindowTitle("IPA Installer")
		self.setWindowIcon(qtg.QIcon("icon.ico"))
		self.authDialog = auth_dialog.AuthDialog()
		self.initUI()
		# self.connectButtons()
		# self.connectSignals()

	def initUI(self):
		self.mainLayout = qtw.QVBoxLayout()
		self.titleLabel = qtw.QLabel("IPA Installer")
		self.subtitleLabel = qtw.QLabel("Your apps. Your way.")
		self.titleLabel.setProperty("class", "title")
		
		# Device layout
		self.deviceTitle = qtw.QLabel("Your device")
		self.deviceTitle.setStyleSheet("font-weight: bold;")
		# self.titleLayout = qtw.QHBoxLayout()
		self.deviceFrame = qtw.QFrame()
		self.deviceFrame.setMinimumWidth(300)
		self.deviceFrame.setFixedHeight(88)
		self.deviceFrame.setProperty("class", "device")
		self.deviceLayout = qtw.QHBoxLayout(self.deviceFrame)
		self.deviceLayout.setContentsMargins(12, 11, 16, 11)
		self.deviceLayout.setSpacing(10)
		self.infoLayout = qtw.QVBoxLayout()
		self.infoLayout.setContentsMargins(0, 0, 0, 0)
		self.infoLayout.setSpacing(4)
		self.infoLayout.setAlignment(qtc.Qt.AlignmentFlag.AlignVCenter)
		self.deviceLabel = qtw.QLabel("Device not connected")
		self.deviceLabel.setProperty("class", "device-status")
		self.deviceModel = qtw.QLabel()
		self.deviceModel.setStyleSheet("font-weight: bold;")
		self.deviceImage = qtw.QLabel()
		self.deviceImage.setFixedSize(64, 64)
		self.deviceImage.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

		# Auth layout 
		# self.authLayout = qtw.QHBoxLayout()
		# self.authStatus = qtw.QLabel("Auth status: ")
		# self.authCircle = qtw.QLabel()
		# self.authCircle.setFixedSize(20, 20)
		# self.authCircle.setProperty("class", "auth-circle-unconnected")
		# self.authLayout.addWidget(self.authStatus)
		# self.authLayout.addWidget(self.authCircle, alignment=qtc.Qt.AlignmentFlag.AlignLeft)

		# self.deviceLabel.addLayout(self.deviceTitleLayout)
		# self.deviceLayout.addWidget(self.deviceTitle, alignment=qtc.Qt.AlignmentFlag.AlignLeft)
		self.deviceLayout.addWidget(self.deviceImage)
		self.deviceLayout.addLayout(self.infoLayout, 1)
		self.infoLayout.addWidget(self.deviceModel)
		self.infoLayout.addWidget(self.deviceLabel)
		# self.deviceLayout.addLayout(self.authLayout)

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
		self.mainLayout.addWidget(self.titleLabel, 
		                          alignment=qtc.Qt.AlignmentFlag.AlignLeft | 
								  qtc.Qt.AlignmentFlag.AlignTop)
		self.mainLayout.addWidget(self.subtitleLabel, 
		                          alignment=qtc.Qt.AlignmentFlag.AlignLeft | 
								  qtc.Qt.AlignmentFlag.AlignTop)
		self.mainLayout.addWidget(self.deviceTitle, 
		                          alignment=qtc.Qt.AlignmentFlag.AlignLeft | 
								  qtc.Qt.AlignmentFlag.AlignTop)
		self.mainLayout.addWidget(self.deviceFrame)
		# self.mainLayout.addLayout(self.buttonsLayout)
		# self.mainLayout.addLayout(self.loggerLayout)
		self.show()

	# def connectButtons(self):
		# self.authButton.clicked.connect(self.authDialog.show)
		# self.authDialog.accepted.connect(self.auth)
		# self.installButton.clicked.connect(InstalledAppsWindow)
	# 	self.connectedSignal.connect(self.updateDevice)

	# def auth(self):
	# 	self.authSignal.emit(self.authDialog.getLogin(), self.authDialog.getPasswd())

	def updateImage(self, path):
		self.deviceImage.setPixmap(qtg.QPixmap(path))

	def updateAuth(self, authStatus):
		self.data_status_label.setObjectName("data-receive-btn-active")
		self.data_status_label.style().unpolish(self.data_status_label)
		self.data_status_label.style().polish(self.data_status_label)

	def updateLog(self, message):
		self.log.append(message)
		self.log.moveCursor(qtg.QTextCursor.MoveOperation.End)

	def updateDevice(self, connectStatus, deviceId, deviceName):
		self.updateDeviceLabel(connectStatus)
		if connectStatus:
			self.deviceModel.setText(deviceName)
			if os.path.exists(f"sources/png/{deviceName}.png"):
				self.updateImage(f"sources/png/{deviceName}.png")
			else:
				self.updateImage(f"sources/png/unknown.png")
		else:
			self.deviceModel.setText(f"Model: -")
			self.deviceImage.setPixmap(qtg.QPixmap("sources/png/unknown.png"))

	def updateDeviceLabel(self, state):
		if state:
			self.deviceLabel.setText("● Device connected")
			self.deviceLabel.setStyleSheet("color: #20B455; font-weight: bold;")
		else:
			self.deviceLabel.setText("● Device not connected")
			self.deviceLabel.setStyleSheet("color: #D64545; font-weight: bold;")

	def closeEvent(self, event):
		self.closeSignal.emit()
		event.accept()
