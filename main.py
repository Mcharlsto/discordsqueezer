from PyQt5 import QtWidgets, uic
import sys
import subprocess, json
import ffmpeg

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)

        self.fileBtn.clicked.connect(self.fileBtnRun)
        self.compressBtn.clicked.connect(self.compressBtnRun)

        self.show()
    
    def fileBtnRun(self):
        global fname
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Select video", "", "MP4 Video (*.mp4)")
        print(fname)
        self.fileBox.setText(fname[0])

    def compressBtnRun(self):
        if(self.regularBtn.isChecked()):
            targetSize = 8
        elif(self.nitrobasicBtn.isChecked()):
            targetSize = 50
        elif(self.nitroBtn.isChecked()):
            targetSize = 500
        
        info = ffmpeg.probe(fname[0])
        duration = (info['format']['duration'])
        print("Duration sec: " + duration)
        print("Target size mb: " + str(targetSize))

        video = ffmpeg.input(fname[0])
        outputFile = fname[0].replace(".mp4", "") + "_squeezed.mp4"
        video = ffmpeg.output(video, outputFile)
        ffmpeg.run(video)
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()