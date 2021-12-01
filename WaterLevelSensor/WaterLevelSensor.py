import paho.mqtt.client as mqtt
import collections
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import datetime
from PyQt4 import QtGui

class WaterLevelSensorUI(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.waterLevelVals = collections.deque(maxlen=10)
        self.timeStamp = collections.deque(maxlen=10)

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.loop_start()

        self.setupUI()

    def setupUI(self):
        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("/feeds/waterlevel")


    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        self.timeStamp.append(str(datetime.datetime.now()))
        self.waterLevelVals.append(msg.payload)

        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.clear()
        # plot data
        obj= {}
        obj['x'] = self.timeStamp
        obj['y'] = self.waterLevelVals
        ax.plot(self.waterLevelVals, '*-')
        # ax.plot('xlabel', 'ylabel', data=obj)
        # refresh canvas
        self.canvas.draw()

    def closeEvent(self, event):
        self.client.loop_stop()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    ex = WaterLevelSensorUI()
    ex.setGeometry(100, 100, 1200, 800)
    ex.show()
    sys.exit(app.exec_())
