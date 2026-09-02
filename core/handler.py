# import threading
import time
import sys
import subprocess
import graphic.main_window
import models
from PyQt6.QtCore import QThread, QProcess, pyqtSignal

@staticmethod
def decodeAnswer(answer):
	answer = answer.decode("utf-8").rstrip()
	return answer

# class AuthResponse(QProcess):
# 	def __init__(self, auth):
# 		super().__init__()
# 		self.auth = auth

# 	def 

class IphoneManager(QThread):
	connectedSignal = pyqtSignal(bool, str, str)
	logSignal = pyqtSignal(str)
	def __init__(self, system):
		super().__init__()
		self.updating = True
		self.connected_device = False
		self.auth = False
		self.system = system

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
							self.set_connected_device(True)
					else:
						self.connectedSignal.emit(False, None, None)
					self.msleep(1000)
				if self.system == "win32":
					update_process = subprocess.Popen([""], )
					self.msleep(1000)
					
			except Exception as e:
				print(e)

	def authDevice(self, login, passwd):
		if self.system == "linux":
			authProcess = subprocess.Popen([f"core/linux_ipatool/ipatool-linux auth login -e {login} -p {passwd}"], 
												stdout=subprocess.PIPE)
			# authProcess.wait()
			self.logging(authProcess)

		if self.system == "win32":
			subprocess.Popen([], stdout=subprocess.PIPE, shell=True)

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