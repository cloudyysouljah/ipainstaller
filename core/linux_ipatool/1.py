import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

p = qtc.QProcess()
p.start("/home/leonid/projects/ipainstaller/core/linux_ipatool/ipatool-linux", ["-h"])
p.waitForFinished()
print(p.readAll())