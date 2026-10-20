import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

class NeedFA_AuthDialog(qtw.QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Authentication")
		self.setWindowIcon(qtg.QIcon("icon.ico"))

		self.codeLine = qtw.QLineEdit()
		self.codeLine.setPlaceholderText("Code") 
		self.faCode = None

		self.QBtn = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok 
					| qtw.QDialogButtonBox.StandardButton.Cancel)

		self.QBtn.accepted.connect(lambda: self.setCode(self.codeLine.text()))

	def setCode(self, code):
		self.faCode = code

class AuthDialog(qtw.QDialog):
	authSignal = qtc.pyqtSignal(str, str)
	def __init__(self, parent=None):
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

	def accept(self):
		if not self.login:
			self.showError("Login is empty")
			return
		if not self.passwd:
			self.showError("Password is empty")
			return
		self.authSignal.emit(self.login, self.passwd)
		return super().accept()

	def showError(self, error):
		qtw.QMessageBox.critical(self, "Error", error)

	def setLogin(self, login):
		self.login = login

	def setPasswd(self, passwd):
		self.passwd = passwd

	def getLogin(self):
		return self.login

	def getPasswd(self):
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