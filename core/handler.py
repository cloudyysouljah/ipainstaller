import threading
import time
import sys
import subprocess
import graphic.main_window
from PyQt6.QtCore import QObject, pyqtSignal

@staticmethod
def decodeAnswer(answer):
	answer = answer.decode("utf-8").rstrip()
	return answer

class IphoneManager(QObject):
	connectedSignal = pyqtSignal(bool, str, str)
	logSignal = pyqtSignal(str)
	def __init__(self, system):
		super().__init__()
		self.updating = True
		self.system = system
		self.updateThread = threading.Thread(target=self.deviceUpdate)

	def deviceUpdate(self):
		while self.updating:
			if self.system == "linux":
				updateProcess = subprocess.Popen(["idevice_id -l"], stdout=subprocess.PIPE, shell=True)
				# self.logging(updateProcess)
				updateProcess.wait()
				updateStdout = updateProcess.stdout.read()
				self.logging(updateProcess)
				if updateProcess.returncode == 0:
					uuid = decodeAnswer(updateStdout)
					modelProcess = subprocess.Popen([f"ideviceinfo -u {uuid} -k ProductType"], stdout=subprocess.PIPE, shell=True)
					# self.logging(modelProcess)
					modelProcess.wait()
					if modelProcess.returncode == 0:
						model = decodeAnswer(modelProcess.stdout.read())
						self.connectedSignal.emit(True, uuid, model)
				else:
					self.connectedSignal.emit(False, None, None)
				time.sleep(0.3)
			if self.system == "win32":
				update_process = subprocess.Popen([""], )
				time.sleep(0.3)

	def stop(self):
		self.updating = False

	def logging(self, process):
		with process.stdout:
			for line in iter(process.stdout.readline, b''):
				self.logSignal.emit(line.decode("utf-8").strip())
				time.sleep(0.05)