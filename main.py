#!/usr/bin/python
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import os
import ffmpeg
from discordsqueezer_ui import Ui_MainWindow

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        if(sys.platform == "linux"):
            print("Running on Linux.")
            self.setWindowIcon(QtGui.QIcon("/usr/share/icons/hicolor/512x512/apps/discordsqueezer.png"))

        self.ui.fileBtn.clicked.connect(self.fileBtnRun)
        self.ui.compressBtn.clicked.connect(self.compressBtnRun)

        self.show()
    
    def fileBtnRun(self):
        global fname
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Select video", "", "MP4 Video (*.mp4)")
        self.ui.fileBox.setText(fname[0])

    def compressBtnRun(self):
        if(self.ui.regularBtn.isChecked()):
            targetSize = 8 * 0.9
        elif(self.ui.nitrobasicBtn.isChecked()):
            targetSize = 50 * 0.95
        elif(self.ui.nitroBtn.isChecked()):
            targetSize = 500 * 0.99

        info = ffmpeg.probe(fname[0])
        duration = (info['format']['duration'])
        audioDict = (info['streams'][1])
        audioBitrate = float(audioDict['bit_rate']) / 1000

        print("Duration sec: " + duration)
        print("Target size mb: " + str(targetSize))

        video = ffmpeg.input(fname[0])
        outputFile = fname[0].replace(".mp4", "") + "_squeezed.mp4"
        bitrate = (targetSize * 8192)/int(float(duration))
        bitrate = bitrate - audioBitrate
        video = ffmpeg.output(video, outputFile, video_bitrate=bitrate*1000)
        if os.path.exists(outputFile):
            os.remove(outputFile)

        ffmpeg.run(video)

        if(sys.platform == "linux"):
            if(os.environ.get('XDG_SESSION_TYPE') == "wayland"):
                os.system("wl-copy -t text/uri-list file://" + outputFile)
            else:
                os.system("echo file://" + outputFile + "| xclip -t text/uri-list -selection clipboard")
        elif(sys.platform == "win32"):
            print("windows")
            os.system("windows_clipboard.exe " + outputFile)


        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Video file has been compressed and copied to clipboard ")
        msg.setWindowTitle("Compress complete")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec())
