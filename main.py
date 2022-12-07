from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import subprocess, json, os
import ffmpeg
from discordsqueezer_ui import Ui_MainWindow

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.fileBtn.clicked.connect(self.fileBtnRun)
        self.ui.compressBtn.clicked.connect(self.compressBtnRun)

        self.show()
    
    def fileBtnRun(self):
        global fname
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Select video", "", "MP4 Video (*.mp4)")
        print(fname)
        self.ui.fileBox.setText(fname[0])

    def compressBtnRun(self):
        if(self.ui.regularBtn.isChecked()):
            targetSize = 8
        elif(self.ui.nitrobasicBtn.isChecked()):
            targetSize = 50
        elif(self.ui.nitroBtn.isChecked()):
            targetSize = 500
        
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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec())
