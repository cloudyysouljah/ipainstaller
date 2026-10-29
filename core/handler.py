# import threading
import time
import sys
import subprocess
import graphic.main_window
import models
import json
from PyQt6.QtCore import QThread, QProcess, pyqtSignal

@staticmethod
def decodeAnswer(answer):
	answer = answer.decode("utf-8").rstrip()
	return answer

class SubProcess(QProcess):
	successSignal = pyqtSignal(str)
	errorSignal = pyqtSignal(str)
	def __init__(self):
		super().__init__()

		self.stdout_data = bytearray()
		self.stderr_data = bytearray()

		self.readyReadStandardOutput.connect(self.readStdout)
		self.readyReadStandardError.connect(self.readStderr)
		self.finished.connect(self.isSuccess)
		self.errorOccurred.connect(self.processError)

	def run(self, command, args):
		if self.state() != QProcess.ProcessState.NotRunning:
			print("Process is already running")
			return
		self.stdout_data.clear()
		self.stderr_data.clear()
		self.start(command, args)

	def readStdout(self):
		self.stdout_data.extend(bytes(self.readAllStandardOutput()))

	def readStderr(self):
		self.stderr_data.extend(bytes(self.readAllStandardError()))

	def processError(self, error):
		print("Process error:", self.errorString())
		if error == QProcess.ProcessError.FailedToStart:
			self.errorSignal.emit(self.errorString())

	def isSuccess(self, exit_code, exit_status):
		self.readStdout()
		self.readStderr()
		stdout = self.stdout_data.decode("utf-8", errors="replace")
		stderr = self.stderr_data.decode("utf-8", errors="replace")
		message = "\n".join(part.strip() for part in (stdout, stderr) if part.strip())
		if exit_status == QProcess.ExitStatus.NormalExit and exit_code == 0:
			self.successSignal.emit(message)
		else:
			self.errorSignal.emit(message or f"Process exited with code {exit_code}")

class IphoneManager(QThread):
	connectedSignal = pyqtSignal(bool, str, str)
	logSignal = pyqtSignal(str)
	needFAsignal = pyqtSignal()
	successSignal = pyqtSignal(bool)
	def __init__(self, system):
		super().__init__()
		self.updating = True
		self.connected_device = False
		self.auth = False
		self.system = system

		self.subProcess = SubProcess()
		self.subProcess.successSignal.connect(self.handleAuthSuccess)
		self.subProcess.errorSignal.connect(self.handleAuthError)

	def run(self):		
		while self.updating:
			try:
				if self.system == "linux":
					updateProcess = subprocess.Popen(["idevice_id", "-l"], 
										stdout=subprocess.PIPE)
					# self.logging(updateProcess)
					updateProcess.wait()
					updateStdout = updateProcess.stdout.read()
					# self.logging(updateProcess)
					if updateProcess.returncode == 0:
						uuid = decodeAnswer(updateStdout)
						modelProcess = subprocess.Popen(
											["ideviceinfo", "-u" , uuid , "-k", "ProductType"], 
											stdout=subprocess.PIPE)
						# self.logging(modelProcess)
						modelProcess.wait()
						if modelProcess.returncode == 0:
							model = models.models.get(decodeAnswer(modelProcess.stdout.read()))
							self.connectedSignal.emit(True, uuid, model)
							self.setConnectedDevice(True)
					else:
						self.connectedSignal.emit(False, None, None)
					self.msleep(1000)
				if self.system == "win32":
					update_process = subprocess.Popen([""], )
					self.msleep(1000)
					
			except Exception as e:
				print(e)

	def authProcess(self, login, passwd):
		self.subProcess.run("core/linux/ipatool_linux",
			["auth", "login", "-e", login, "-p", passwd, "--format", "json", 
			"--non-interactive"])

	def sendCode(self, code):
		self.subProcess.run("core/linux/ipatool_linux",
			["auth", "2fa", "-c", code, "--format", "json", "--non-interactive"])
		# self.subProcess.isSuccess()
		# self.handleAuthResponse(self.subProcess.stdout_data.decode("utf-8"))
		# self.msleep(1000)

	def handleAuthSuccess(self, message):
		# print(message)
		self.setAuth(True)
		self.handleAuthResponse(message)

	def handleAuthError(self, message):
		# print(message)
		self.setAuth(False)
		self.handleAuthResponse(message)

	def handleAuthResponse(self, message):
		# print(1)
		# print(message)
		for line in message.splitlines():
			# print(line)
			if not line.strip():
				continue
			try:
				response = json.loads(line)
				print(response)
			except json.JSONDecodeError:
				# print("2121")
				# self.logSignal.emit(line)
				continue
			if isinstance(response, dict):
				text = response.get("error") or response.get("message")
				# if isinstance(text, str):
				# 	# self.logSignal.emit(text)
				# 	continue
			# print(json.dumps(response, ensure_ascii=False))
			# print(text.split(";")[0])
			if response.get("message") is not None:
				if text.split(";")[0] == "2FA code is required":
					self.needFAsignal.emit()
			if response.get("success") == True:
				self.successSignal.emit(False)
			# self.logSignal.emit(json.dumps(response, ensure_ascii=False))

	def setUpdating(self, updating):
		self.updating = updating

	def getUpdating(self):
		return self.updating

	def setConnectedDevice(self, connected):
		self.connected_device = connected
	
	def getConnectedDevice(self):
		return self.connected_device

	def setAuth(self, auth):
		self.auth = auth

	def getAuth(self):
		return self.auth

	def stop(self):
		self.setUpdating(False)

	def logging(self, process):
		with process.stdout:
			for line in iter(process.stdout.readline, b''):
				self.logSignal.emit(line.decode("utf-8").strip())
				time.sleep(0.05)
