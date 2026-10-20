import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc
import os

import graphic.auth_dialog as auth_dialog

class CustomPushButton(qtw.QPushButton):
	def __init__(self, text, parent=None):
		super().__init__(text, parent)
		self.setCursor(qtc.Qt.CursorShape.PointingHandCursor)

		self.setFixedHeight(30)
		self.setProperty("class", "custom-button")

	# def mousePressEvent(self, event):
		# print("huy")
		# event.accept()

	# def keyPressEvent(self, event):
		
		# self.setProperty("class", "custom-button")


class CustomTitleBar(qtw.QWidget):
	def __init__(self, parent: qtw.QMainWindow):
		super().__init__(parent)
		self.parentWindow = parent
		self.dragPosition = qtc.QPoint()

		self.setAttribute(qtc.Qt.WidgetAttribute.WA_StyledBackground, True)
		self.setObjectName("CustomTitleBar")
		self.setStyleSheet("""
			QWidget#CustomTitleBar {
				background-color: #DFE6F1;
				border-top-left-radius: 19px;
				border-top-right-radius: 19px;
			}
			QWidget#CustomTitleBar QLabel {
				background-color: transparent;
			}
		""")

		# Build Layout
		layout = qtw.QHBoxLayout(self)
		layout.setContentsMargins(10, 0, 10, 0)
		layout.setSpacing(5)
		self.setFixedHeight(30)

		# Icon 
		self.icon = qtw.QLabel()
		self.icon.setPixmap(qtg.QPixmap("icon.ico"))
		layout.addWidget(self.icon)

		# Window Title
		self.titleLabel = qtw.QLabel("IPA Installer")
		self.titleLabel.setStyleSheet("color: #1D1D1F; " \
									  "font-weight: bold; " \
									  "font-size: 13px;")
		layout.addWidget(self.titleLabel)
		layout.addStretch()

		# Window Buttons
		self.btnMin = qtw.QPushButton("—")
		self.btnMax = qtw.QPushButton("▢")
		self.btnClose = qtw.QPushButton("✕")

		# Styling the buttons
		btnStyle = """
			QPushButton {
				background-color: transparent;
				color: #1D1D1F;
				border: none;
				font-size: 14px;
				width: 25px;
				height: 20px;
			}
			QPushButton:hover {
				background-color: #444444;
			}
		"""
		closeBtnStyle = btnStyle + "QPushButton:hover { background-color: #E81123; }"

		for btn in (self.btnMin, self.btnMax):
			btn.setStyleSheet(btnStyle)
			layout.addWidget(btn)

		self.btnClose.setStyleSheet(closeBtnStyle)
		layout.addWidget(self.btnClose)

		# self.setStyleSheet("""
		# 	QWidget {
		# 		background-color: #DFE6F1;
		# 	}
		# """)

		self.btnMin.clicked.connect(self.parentWindow.showMinimized)
		self.btnMax.clicked.connect(self.toggleMaximize)
		self.btnClose.clicked.connect(self.parentWindow.close)

	def toggleMaximize(self):
		if self.parentWindow.isMaximized():
			self.parentWindow.showNormal()
			self.btnMax.setText("▢")
		else:
			self.parentWindow.showMaximized()
			self.btnMax.setText("❐")

	def mousePressEvent(self, event: qtg.QMouseEvent):
		if event.button() == qtc.Qt.MouseButton.LeftButton:
			self.dragPosition = event.globalPosition().toPoint() - self.parentWindow.frameGeometry().topLeft()
			event.accept()

	def mouseMoveEvent(self, event: qtg.QMouseEvent):
		if event.buttons() == qtc.Qt.MouseButton.LeftButton:
			self.parentWindow.move(event.globalPosition().toPoint() - self.dragPosition)
			event.accept()

class MainWindow(qtw.QWidget):
	closeSignal = qtc.pyqtSignal()
	authSignal = qtc.pyqtSignal(str, str)
	def __init__(self):
		super().__init__()
		self.setWindowFlags(qtc.Qt.WindowType.FramelessWindowHint)
		self.setAttribute(qtc.Qt.WidgetAttribute.WA_TranslucentBackground)
		self.setWindowIcon(qtg.QIcon("icon.ico"))
		self.authDialog = auth_dialog.AuthDialog()
		self.connected = False
		self.initUI()
		self.connectButtons()

	def initUI(self):
		self.title_bar = CustomTitleBar(self)
		self.mainFrame = qtw.QFrame(self)
		self.mainFrame.setProperty("class", "mainFrame")
		self.mainLayout = qtw.QVBoxLayout(self.mainFrame)
		self.mainLayout.setContentsMargins(0, 0, 0, 0)
		self.mainLayout.setSpacing(0)
		self.contentLayout = qtw.QVBoxLayout()
		self.contentLayout.setContentsMargins(9, 6, 9, 9)
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
		# self.authButton = CustomPushButton()
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
		self.infoLayout.addWidget(self.deviceModel, 
		                          alignment=qtc.Qt.AlignmentFlag.AlignLeft | 
								  qtc.Qt.AlignmentFlag.AlignTop)
		self.infoLayout.addWidget(self.deviceLabel)
		# self.deviceLayout.addLayout(self.authLayout)

		# Buttons layout 
		self.buttonsLayout = qtw.QVBoxLayout()
		self.authButton = CustomPushButton("● Authenticate", self)
		self.authButton.setEnabled(False)
		# self.installButton = qtw.QPushButton("Installed apps")
		self.buttonsLayout.addWidget(self.authButton)
		# self.buttonsLayout.addWidget(self.installButton)

		# Logger layout 
		self.loggerLayout = qtw.QVBoxLayout()
		self.log = qtw.QTextEdit()
		self.log.setReadOnly(True)
		self.log.setProperty("class", "log")
		self.loggerLayout.addWidget(self.log)

		# Main layout
		self.windowLayout = qtw.QVBoxLayout(self)
		self.windowLayout.setContentsMargins(0, 0, 0, 0)
		self.windowLayout.addWidget(self.mainFrame)
		self.mainLayout.addWidget(self.title_bar)
		self.mainLayout.addLayout(self.contentLayout)
		self.contentLayout.addWidget(self.titleLabel, 
								  alignment=qtc.Qt.AlignmentFlag.AlignLeft | 
								  qtc.Qt.AlignmentFlag.AlignTop)
		self.contentLayout.addWidget(self.subtitleLabel, 
								  alignment=qtc.Qt.AlignmentFlag.AlignLeft | 
								  qtc.Qt.AlignmentFlag.AlignTop)
		self.contentLayout.addWidget(self.deviceTitle, 
								  alignment=qtc.Qt.AlignmentFlag.AlignLeft | 
								  qtc.Qt.AlignmentFlag.AlignTop)
		self.contentLayout.addWidget(self.deviceFrame)
		self.contentLayout.addLayout(self.buttonsLayout)
		# self.mainLayout.addLayout(self.buttonsLayout)
		# self.mainLayout.addLayout(self.loggerLayout)
		# self.show()

	def connectButtons(self):
		self.authButton.clicked.connect(self.authDialog.show)
		self.authDialog.authSignal.connect(self.auth)
		
		# self.installButton.clicked.connect(InstalledAppsWindow)
		# self.connectedSignal.connect(self.updateDevice)

	def auth(self):
		self.authSignal.emit(self.authDialog.getLogin(), self.authDialog.getPasswd())

	def updateImage(self, path):
		self.deviceImage.setPixmap(qtg.QPixmap(path))

	def updateAuth(self, authStatus):
		self.dataStatusLabel.setObjectName("data-receive-btn-active")
		self.dataStatusLabel.style().unpolish(self.data_status_label)
		self.dataStatusLabel.style().polish(self.data_status_label)

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
		self.authButton.setEnabled(connectStatus)

	def updateDeviceLabel(self, state):
		if state:
			self.deviceLabel.setText("● Need authorization")
			self.deviceLabel.setStyleSheet("color: #FF9933; font-weight: bold;")
		else:
			self.deviceLabel.setText("● Device not connected")
			self.deviceLabel.setStyleSheet("color: #D64545; font-weight: bold;")

	def closeEvent(self, event):
		self.closeSignal.emit()
		event.accept()
