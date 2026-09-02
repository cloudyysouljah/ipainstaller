import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

class AuthDialog(qtw.QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Authentication")
		self.setWindowIcon(qtg.QIcon("icon.ico"))

		self.login = None
		self.passwd = None

		self.initUI()
		self.connectSignals()

	def initUI(self):
		self.loginText = qtw.QLineEdit()
		self.loginText.setPlaceholderText("Login")
		self.loginLayout = qtw.QHBoxLayout()
		self.loginLayout.addWidget(self.loginText)

		self.passwdText = CustomPasswordTextLine()
		self.passwdText.setPlaceholderText("Password")
		self.passwdText.setEchoMode(qtw.QLineEdit.EchoMode.Password)
		self.passwdLayout = qtw.QHBoxLayout()
		self.passwdLayout.addWidget(self.passwdText)

		self.mainLayout = qtw.QVBoxLayout()
		self.mainLayout.addLayout(self.loginLayout)
		self.mainLayout.addLayout(self.passwdLayout)
		self.QBtn = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok 
							| qtw.QDialogButtonBox.StandardButton.Cancel)
		self.mainLayout.addWidget(self.QBtn)
		self.setLayout(self.mainLayout)

	def connectSignals(self):
		self.loginText.textChanged.connect(self.setLogin)
		self.passwdText.textChanged.connect(self.setPasswd)
		self.QBtn.accepted.connect(self.accept)
		self.QBtn.rejected.connect(self.reject)

	def setLogin(self, login):
		self.login = login

	def setPasswd(self, passwd):
		self.passwd = passwd

	def get_login(self):
		return self.login

	def get_passwd(self):
		return self.passwd

class CustomPasswordTextLine(qtw.QLineEdit):
	def __init__(self):
		super().__init__()
		self.passwdVisible = False
		self.setEchoMode(qtw.QLineEdit.EchoMode.Password)
		self.setPlaceholderText("Password")
		self.initUI()

	def initUI(self):
		self.toggleAction = qtg.QAction(qtg.QIcon("graphic/eye_open.png"), "", self)
		self.toggleAction.setCheckable(True)
		self.addAction(self.toggleAction, qtw.QLineEdit.ActionPosition.TrailingPosition)
		self.toggleAction.toggled.connect(self.showPasswd)

	def showPasswd(self):
		if self.passwdVisible:
			self.setEchoMode(qtw.QLineEdit.EchoMode.Password)
		else:
			self.setEchoMode(qtw.QLineEdit.EchoMode.Normal)
		self.setPasswdVisible(not self.passwdVisible)

	def setPasswdVisible(self, passwdVisible):
		self.passwdVisible = passwdVisible