import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

class InstalledAppsWindow(qtw.QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Installed apps")
		self.setWindowIcon(qtg.QIcon("icon.ico"))
		self.initUI()
		# self.connectSignals()

	def initUI(self):
		self.mainLayout = qtw.QVBoxLayout()
		# Device layout
		self.deviceTitle = qtw.QLabel("Device")
		# self.deviceTitleLayout.addWidget(self.deviceTitle)

		self.deviceLayout = qtw.QVBoxLayout()
		self.deviceLayout.setProperty("class", "device")
		self.deviceLabel = qtw.QLabel("Device not connected")
		self.deviceModel = qtw.QLabel("Model: - ")
		# self.deviceLabel.addLayout(self.deviceTitleLayout)
		self.deviceLayout.addWidget(self.deviceTitle, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
		self.deviceLayout.addWidget(self.deviceLabel)
		self.deviceLayout.addWidget(self.deviceModel)

		# Buttons layout 
		self.buttonsLayout = qtw.QVBoxLayout()
		self.installButton = qtw.QPushButton("Installed apps")
		self.buttonsLayout.addWidget(self.installButton)

		# Logger layout 
		self.loggerLayout = qtw.QVBoxLayout()
		self.log = qtw.QTextEdit()
		self.log.setReadOnly(True)
		self.log.setProperty("class", "log")
		self.loggerLayout.addWidget(self.log)

		# Main layout
		self.setLayout(self.mainLayout)
		self.mainLayout.addLayout(self.deviceLayout)
		self.mainLayout.addLayout(self.buttonsLayout)
		self.mainLayout.addLayout(self.loggerLayout)
		self.show()

	def closeEvent(self, event):
		event.accept()