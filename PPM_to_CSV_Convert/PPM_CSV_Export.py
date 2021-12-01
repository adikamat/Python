import os
import csv
from PyQt4 import QtGui, QtCore
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

class ConvertToCsvUI(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.initUI()

    def initUI(self):
        # First Line - Select FIle + Filename Label
        self.title = QtGui.QPushButton('Select File')
        self.title.clicked.connect(self.SelectNewDirectory)
        self.file = QtGui.QLabel('')

        # Second line - Percentage
        # self.progressBar = QtGui.QProgressBar(self)
        self.Status = QtGui.QLabel('')

        # Third Line - Push Button
        self.fix_all_button = QtGui.QPushButton("Generate CSV")
        self.fix_all_button.clicked.connect(self.ExportCsv)

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.title, 0, 0, 1, 1)
        grid.addWidget(self.file, 0, 1, 1, 3)

        grid.addWidget(self.Status, 1, 0, 1, 4)

        # grid.addWidget(self.title, 1, 0)
        grid.addWidget(self.fix_all_button, 2, 3)

        self.setLayout(grid)

        self.setGeometry(100, 100, 250, 250)
        self.setWindowTitle('Convert JPEG to CSV in PPM format')
        self.show()

    def SelectNewDirectory(self):

        dialog = QtGui.QFileDialog.getOpenFileName(self, "JPEG file", "~", "JPEG Files (*.jpg)")
        # dialog.setSidebarUrls([QtCore.QUrl.fromLocalFile(place)])
        if dialog != "":
            self.file.setText(dialog)
            self.Status.setText('')

    def ExportCsv(self):

        # Open the JPEG file
        img = Image.open(str(self.file.text()))
        pix = img.load()

        self.Status.setText('Converting.....')
        self.setDisabled(True)
        self.repaint()

        # Write to csv file
        output_file = os.path.splitext(img.filename)[0] + '.csv'
        with open(output_file, 'wb') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow(['P3'])
            csv_writer.writerow((img.width, img.height))
            csv_writer.writerow([255])
            i = 0
            for y in range(img.height):
                for x in range(img.width):
                    r = pix[x, y][0]
                    g = pix[x, y][1]
                    b = pix[x, y][2]
                    csv_writer.writerow((r, g, b))
                    # i = i + 1
                    # self.progressBar.setValue(i)
                    # self.update()

        self.setDisabled(False)
        self.Status.setText('Conversion Complete')


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ex = ConvertToCsvUI()
    ex.setGeometry(100, 100, 500, 500)
    ex.show()
    sys.exit(app.exec_())
