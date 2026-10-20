# import threading
import time
import sys
import subprocess
import graphic.main_window
import models
from PyQt6.QtCore import QThread, QProcess, pyqtSignal
from pathlib import Path

@staticmethod
def decodeAnswer(answer):
	answer = answer.decode("utf-8").rstrip()
	return answer

class SubProcess(QProcess):
	successSignal = pyqtSignal()
	errorSignal = pyqtSignal()
	def __init__(self):
		super().__init__()
		self.readyReadStandardOutput.connect(self.readStdout)
		self.readyReadStandardError.connect(self.readStderr)
		self.finished.connect(self.isSuccess)
		self.errorOccurred.connect(self.processError)

	def run(self, command, args):
		if self.state() != QProcess.ProcessState.NotRunning:
			print("Process is already running")
			return
		self.start(command, args)

	def readStdout(self):
		print("stdout:", bytes(self.readAllStandardOutput()).decode(
			"utf-8", errors="replace"
		))

	def readStderr(self):
		print("stderr:", bytes(self.readAllStandardError()).decode(
			"utf-8", errors="replace"
		))

	def processError(self, error):
		print("Process error:", self.errorString())
		if error == QProcess.ProcessError.FailedToStart:
			self.errorSignal.emit()

	def isSuccess(self):
		print(self.exitCode())
		if self.exitStatus() == QProcess.ExitStatus.NormalExit and self.exitCode() == 0:
			print("Success")
			self.successSignal.emit()
		else:
			print("Error")
			self.errorSignal.emit()

class IphoneManager(QThread):
	connectedSignal = pyqtSignal(bool, str, str)
	logSignal = pyqtSignal(str)
	def __init__(self, system):
		super().__init__()
		self.updating = True
		self.connected_device = False
		self.auth = False
		self.system = system

		self.subProcess = SubProcess()

	def run(self):
		while self.updating:
			try:
				if self.system == "linux":
					updateProcess = subprocess.Popen(["idevice_id -l"], 
													 stdout=subprocess.PIPE, 
													 shell=True)
					# self.logging(updateProcess)
					updateProcess.wait()
					updateStdout = updateProcess.stdout.read()
					# self.logging(updateProcess)
					if updateProcess.returncode == 0:
						uuid = decodeAnswer(updateStdout)
						modelProcess = subprocess.Popen([f"ideviceinfo -u {uuid} -k ProductType"], 
														   stdout=subprocess.PIPE, 
														   shell=True)
						# self.logging(modelProcess)
						modelProcess.wait()
						if modelProcess.returncode == 0:
							model = decodeAnswer(modelProcess.stdout.read())
							self.connectedSignal.emit(True, uuid, model)
					else:
						self.connectedSignal.emit(False, None, None)
						self.msleep(1000)
				if self.system == "win32":
					ideviceExePath = Path(__file__).resolve().parent / "win_tools" / "idevice_id.exe"
					updateProcess = subprocess.Popen([ideviceExePath, "-l"], 
													  stdout=subprocess.PIPE, 
													  shell=True)
					# self.logging(updateProcess)
					updateProcess.wait()
					updateStdout = updateProcess.stdout.read()
					# self.logging(updateProcess)
					if updateProcess.returncode == 0:
						uuid = decodeAnswer(updateStdout)
						print(uuid)
						ideviceExePath = Path(__file__).resolve().parent / "win_tools" / "ideviceinfo.exe"
						modelProcess = subprocess.Popen(
							[str(ideviceExePath), "-u", uuid, "-k", "ProductType"],
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE,
						)
						# self.logging(modelProcess)
						modelProcess.wait()
						if modelProcess.returncode == 0:
							model = models.models.get(decodeAnswer(modelProcess.stdout.read()))
							print(model)
							self.connectedSignal.emit(True, uuid, model)
					else:
						self.connectedSignal.emit(False, None, None)
					self.msleep(1000)
			except Exception as e:
				print(e)

	def authProcess(self, login, passwd):
		if self.system == "linux":
			self.subProcess.run("/home/leonid/projects/ipainstaller/core/linux_ipatool/ipatool-linux",
			["auth", "login", "-e", login, "-p", passwd])
		if self.system == "win32":
			self.subProcess.run("core\\windows_ipatool\\ipatool.exe", ["auth", "login", "-e", login, "-p", passwd])

	def set_updating(self, updating):
		self.updating = updating

	def get_updating(self):
		return self.updating

	def set_connected_device(self, connected):
		self.connected_device = connected
	
	def get_connected_device(self):
		return self.connected_device

	def set_auth(self, auth):
		self.auth = auth

	def get_auth(self):
		return self.auth

	def stop(self):
		self.set_updating(False)

	def logging(self, process):
		with process.stdout:
			for line in iter(process.stdout.readline, b''):
				self.logSignal.emit(line.decode("utf-8").strip())
				time.sleep(0.05)
