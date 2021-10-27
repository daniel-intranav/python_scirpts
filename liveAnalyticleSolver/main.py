"""
Intranav GmbH © 2021
check tag positioning
"""

import sys
import numpy as np
import math
from multilaterate import *

from PyQt5 import uic, QtGui
from PyQt5.Qt import Qt, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from numpy.core.function_base import linspace
from numpy.lib.ufunclike import isneginf


SPEED_OF_LIGHT = 299702547000

c_ = [1, 3]
x_ = [0, 5, -3.4]
y_ = [0, 3.9, -36.8]
test = []


towers = np.array([[-2166, 13137], [-4715.0, 10720.0], [-1773, 7694], [  754., 10178.]])
rec_times = np.array([0.0, 1.604954391609681e-09, -1.3815821375828818e-08, -1.2063200216516634e-08])

class Window(QMainWindow, QDialog):

    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("live_analyticle_solver.ui", self)

        self.setWindowTitle("live Analyticle Solver")

        self._y = []
        self._x = linspace(-50, 50, 900)
        self.x1 = 0
        self.x2 = 0
        self.y11 = 0
        self.y12 = 0
        self.y13 = 0
        self.y14 = 0
        self.y21 = 0
        self.y22 = 0
        self.y23 = 0
        self.y24 = 0


        self.horizontalSlider_x_2.valueChanged.connect(self.sliderChanged)
        self.horizontalSlider_y_2.valueChanged.connect(self.sliderChanged)
        self.horizontalSlider_x_3.valueChanged.connect(self.sliderChanged)
        self.horizontalSlider_y_3.valueChanged.connect(self.sliderChanged)
        self.horizontalSlider_c_1.valueChanged.connect(self.sliderChanged)
        self.horizontalSlider_c_2.valueChanged.connect(self.sliderChanged)

        self.plainTextEdit_x_2.textChanged.connect(self.textChanged)
        self.plainTextEdit_y_2.textChanged.connect(self.textChanged)
        self.plainTextEdit_x_3.textChanged.connect(self.textChanged)
        self.plainTextEdit_y_3.textChanged.connect(self.textChanged)
        self.plainTextEdit_c_1.textChanged.connect(self.textChanged)
        self.plainTextEdit_c_2.textChanged.connect(self.textChanged)

    def sliderChanged(self):

        self.plainTextEdit_x_2.textChanged.disconnect()
        self.plainTextEdit_y_2.textChanged.disconnect()
        self.plainTextEdit_x_3.textChanged.disconnect()
        self.plainTextEdit_y_3.textChanged.disconnect()
        self.plainTextEdit_c_1.textChanged.disconnect()
        self.plainTextEdit_c_2.textChanged.disconnect()

        self.plainTextEdit_x_2.setPlainText(str(self.horizontalSlider_x_2.value()))
        self.plainTextEdit_y_2.setPlainText(str(self.horizontalSlider_y_2.value()))
        self.plainTextEdit_x_3.setPlainText(str(self.horizontalSlider_x_3.value()))
        self.plainTextEdit_y_3.setPlainText(str(self.horizontalSlider_y_3.value()))
        self.plainTextEdit_c_1.setPlainText(str(self.horizontalSlider_c_1.value()))
        self.plainTextEdit_c_2.setPlainText(str(self.horizontalSlider_c_2.value()))
        
        self.plainTextEdit_x_2.textChanged.connect(self.textChanged)
        self.plainTextEdit_y_2.textChanged.connect(self.textChanged)
        self.plainTextEdit_x_3.textChanged.connect(self.textChanged)
        self.plainTextEdit_y_3.textChanged.connect(self.textChanged)
        self.plainTextEdit_c_1.textChanged.connect(self.textChanged)
        self.plainTextEdit_c_2.textChanged.connect(self.textChanged)

        # update Hyperbola and intersection points       
        self.updateHyperbola()
        self.analyticSolver()

        # draw hyperbola and intersections points
        self.drawCanvas()

    def textChanged(self):
        
        self.horizontalSlider_x_2.valueChanged.disconnect()
        self.horizontalSlider_y_2.valueChanged.disconnect()
        self.horizontalSlider_x_3.valueChanged.disconnect()
        self.horizontalSlider_y_3.valueChanged.disconnect()
        self.horizontalSlider_c_1.valueChanged.disconnect()
        self.horizontalSlider_c_2.valueChanged.disconnect()
        
        self.horizontalSlider_x_2.setSliderPosition(int(self.plainTextEdit_x_2.toPlainText()))
        self.horizontalSlider_y_2.setSliderPosition(int(self.plainTextEdit_y_2.toPlainText()))
        self.horizontalSlider_x_3.setSliderPosition(int(self.plainTextEdit_x_3.toPlainText()))
        self.horizontalSlider_y_3.setSliderPosition(int(self.plainTextEdit_y_3.toPlainText()))
        self.horizontalSlider_c_1.setSliderPosition(int(self.plainTextEdit_c_1.toPlainText()))
        self.horizontalSlider_c_2.setSliderPosition(int(self.plainTextEdit_c_2.toPlainText()))

        self.horizontalSlider_x_2.valueChanged.connect(self.sliderChanged)
        self.horizontalSlider_y_2.valueChanged.connect(self.sliderChanged)
        self.horizontalSlider_x_3.valueChanged.connect(self.sliderChanged)
        self.horizontalSlider_y_3.valueChanged.connect(self.sliderChanged)
        self.horizontalSlider_c_1.valueChanged.connect(self.sliderChanged)
        self.horizontalSlider_c_2.valueChanged.connect(self.sliderChanged)
        
        # update Hyperbola and intersection points       
        self.updateHyperbola()
        self.analyticSolver()

        # draw hyperbola and intersections points
        self.drawCanvas()

    def updateHyperbola(self):
        global test
        self._y = []

        x_[1] = self.horizontalSlider_x_2.value()
        y_[1] = self.horizontalSlider_y_2.value()
        x_[2] = self.horizontalSlider_x_3.value()
        y_[2] = self.horizontalSlider_y_3.value()
        c_[0] = self.horizontalSlider_c_1.value()
        c_[1] = self.horizontalSlider_c_2.value()
        tast = [0, c_[0], c_[1]]
        test = get_loci(np.array(tast) ,np.array([x_, y_]), 1, 1, 200)

        for i in range(0, 2):
            y = []
            for x in self._x:
                # y.append( (c_[0]*np.sqrt((- c_[0]**2 + x_[1]**2 + y_[1]**2)*(- c_[0]**2 + 4*x**2 - 4*x*x_[1] + x_[1]**2 + y_[1]**2)) + c_[0]**2*y_[1] - x_[1]**2*y_[1] - y_[1]**3 + 2*x*x_[1]*y_[1])/(2*(c_[0]**2 - y_[1]**2)))
                y.append(-(c_[0]*np.sqrt((- c_[0]**2 + x_[1]**2 + y_[1]**2)*(- c_[0]**2 + 4*x**2 - 4*x*x_[1] + x_[1]**2 + y_[1]**2)) - c_[0]**2*y_[1] + x_[1]**2*y_[2] + y_[1]**3 - 2*x*x_[1]*y_[1])/(2*(c_[0]**2 - y_[1]**2)))
            self._y.append(y)
            
            y = []
            for x in self._x:
                y.append( (c_[1]*np.sqrt((- c_[1]**2 + x_[2]**2 + y_[2]**2)*(- c_[1]**2 + 4*x**2 - 4*x*x_[2] + x_[2]**2 + y_[2]**2)) + c_[1]**2*y_[2] - x_[2]**2*y_[2] - y_[2]**3 + 2*x*x_[2]*y_[2])/(2*(c_[1]**2 - y_[2]**2)))
                # y.append(-(c_[1]*np.sqrt((- c_[1]**2 + x_[2]**2 + y_[2]**2)*(- c_[1]**2 + 4*x**2 - 4*x*x_[2] + x_[2]**2 + y_[2]**2)) - c_[1]**2*y_[2] + x_[2]**2*y_[2] + y_[2]**3 - 2*x*x_[2]*y_[2])/(2*(c_[1]**2 - y_[2]**2)))
            self._y.append(y)
        

    def analyticSolver(self):

        for i in range(0, 1):
            self.x1 = -(x_[i+1]**3*y_[i+2]**2 + x_[i+2]**3*y_[i+1]**2 - c_[i]**2*x_[i+2]**3 - c_[i+1]**2*x_[i+1]**3 - x_[i+1]*y_[i+1]*y_[i+2]**3 - x_[i+2]*y_[i+1]**3*y_[i+2] + c_[i]*y_[i+2]*np.sqrt((- c_[i]**2 + x_[i+1]**2 + y_[i+1]**2)*(- c_[i+1]**2 + x_[i+2]**2 + y_[i+2]**2)*(- c_[i]**2 + 2*c_[i]*c_[i+1] - c_[i+1]**2 + x_[i+1]**2 - 2*x_[i+1]*x_[i+2] + x_[i+2]**2 + y_[i+1]**2 - 2*y_[i+1]*y_[i+2] + y_[i+2]**2)) - c_[i+1]*y_[i+1]*np.sqrt((- c_[i]**2 + x_[i+1]**2 + y_[i+1]**2)*(- c_[i+1]**2 + x_[i+2]**2 + y_[i+2]**2)*(- c_[i]**2 + 2*c_[i]*c_[i+1] - c_[i+1]**2 + x_[i+1]**2 - 2*x_[i+1]*x_[i+2] + x_[i+2]**2 + y_[i+1]**2 - 2*y_[i+1]*y_[i+2] + y_[i+2]**2)) + c_[i]**2*c_[i+1]**2*x_[i+1] + c_[i]**2*c_[i+1]**2*x_[i+2] - c_[i]**2*x_[i+1]*y_[i+2]**2 - c_[i+1]**2*x_[i+1]*y_[i+1]**2 - c_[i]**2*x_[i+2]*y_[i+2]**2 - c_[i+1]**2*x_[i+2]*y_[i+1]**2 + x_[i+1]*y_[i+1]**2*y_[i+2]**2 + x_[i+2]*y_[i+1]**2*y_[i+2]**2 - c_[i]*c_[i+1]**3*x_[i+1] - c_[i]**3*c_[i+1]*x_[i+2] + c_[i]*c_[i+1]*x_[i+1]*x_[i+2]**2 + c_[i]*c_[i+1]*x_[i+1]**2*x_[i+2] + c_[i]*c_[i+1]*x_[i+1]*y_[i+2]**2 + c_[i]*c_[i+1]*x_[i+2]*y_[i+1]**2 + c_[i]**2*x_[i+2]*y_[i+1]*y_[i+2] + c_[i+1]**2*x_[i+1]*y_[i+1]*y_[i+2] - x_[i+1]*x_[i+2]**2*y_[i+1]*y_[i+2] - x_[i+1]**2*x_[i+2]*y_[i+1]*y_[i+2])/(2*(c_[i+1]**2*(x_[i+1]**2 + y_[i+1]**2) + x_[i+2]**2*(c_[i]**2 - y_[i+1]**2) + y_[i+2]**2*(c_[i]**2 - x_[i+1]**2) - 2*y_[i+1]*y_[i+2]*(c_[i]*c_[i+1] - x_[i+1]*x_[i+2]) - 2*c_[i]*c_[i+1]*x_[i+1]*x_[i+2]))
            self.x2 = -(x_[i+1]**3*y_[i+2]**2 + x_[i+2]**3*y_[i+1]**2 - c_[i]**2*x_[i+2]**3 - c_[i+1]**2*x_[i+1]**3 - x_[i+1]*y_[i+1]*y_[i+2]**3 - x_[i+2]*y_[i+1]**3*y_[i+2] - c_[i]*y_[i+2]*np.sqrt((- c_[i]**2 + x_[i+1]**2 + y_[i+1]**2)*(- c_[i+1]**2 + x_[i+2]**2 + y_[i+2]**2)*(- c_[i]**2 + 2*c_[i]*c_[i+1] - c_[i+1]**2 + x_[i+1]**2 - 2*x_[i+1]*x_[i+2] + x_[i+2]**2 + y_[i+1]**2 - 2*y_[i+1]*y_[i+2] + y_[i+2]**2)) + c_[i+1]*y_[i+1]*np.sqrt((- c_[i]**2 + x_[i+1]**2 + y_[i+1]**2)*(- c_[i+1]**2 + x_[i+2]**2 + y_[i+2]**2)*(- c_[i]**2 + 2*c_[i]*c_[i+1] - c_[i+1]**2 + x_[i+1]**2 - 2*x_[i+1]*x_[i+2] + x_[i+2]**2 + y_[i+1]**2 - 2*y_[i+1]*y_[i+2] + y_[i+2]**2)) + c_[i]**2*c_[i+1]**2*x_[i+1] + c_[i]**2*c_[i+1]**2*x_[i+2] - c_[i]**2*x_[i+1]*y_[i+2]**2 - c_[i+1]**2*x_[i+1]*y_[i+1]**2 - c_[i]**2*x_[i+2]*y_[i+2]**2 - c_[i+1]**2*x_[i+2]*y_[i+1]**2 + x_[i+1]*y_[i+1]**2*y_[i+2]**2 + x_[i+2]*y_[i+1]**2*y_[i+2]**2 - c_[i]*c_[i+1]**3*x_[i+1] - c_[i]**3*c_[i+1]*x_[i+2] + c_[i]*c_[i+1]*x_[i+1]*x_[i+2]**2 + c_[i]*c_[i+1]*x_[i+1]**2*x_[i+2] + c_[i]*c_[i+1]*x_[i+1]*y_[i+2]**2 + c_[i]*c_[i+1]*x_[i+2]*y_[i+1]**2 + c_[i]**2*x_[i+2]*y_[i+1]*y_[i+2] + c_[i+1]**2*x_[i+1]*y_[i+1]*y_[i+2] - x_[i+1]*x_[i+2]**2*y_[i+1]*y_[i+2] - x_[i+1]**2*x_[i+2]*y_[i+1]*y_[i+2])/(2*(c_[i+1]**2*(x_[i+1]**2 + y_[i+1]**2) + x_[i+2]**2*(c_[i]**2 - y_[i+1]**2) + y_[i+2]**2*(c_[i]**2 - x_[i+1]**2) - 2*y_[i+1]*y_[i+2]*(c_[i]*c_[i+1] - x_[i+1]*x_[i+2]) - 2*c_[i]*c_[i+1]*x_[i+1]*x_[i+2]))
            
            x = self.x1

            if not np.isnan(x) and not np.isinf(x):
                self.y11 =  (c_[i]*np.sqrt((- c_[i]**2 + x_[i+1]**2 + y_[i+1]**2)*(- c_[i]**2 + 4*x**2 - 4*x*x_[i+1] + x_[i+1]**2 + y_[i+1]**2)) + c_[i]**2*y_[i+1] - x_[i+1]**2*y_[i+1] - y_[i+1]**3 + 2*x*x_[i+1]*y_[i+1])/(2*(c_[i]**2 - y_[i+1]**2))
                self.y12 = -(c_[i]*np.sqrt((- c_[i]**2 + x_[i+1]**2 + y_[i+1]**2)*(- c_[i]**2 + 4*x**2 - 4*x*x_[i+1] + x_[i+1]**2 + y_[i+1]**2)) - c_[i]**2*y_[i+1] + x_[i+1]**2*y_[i+1] + y_[i+1]**3 - 2*x*x_[i+1]*y_[i+1])/(2*(c_[i]**2 - y_[i+1]**2))
                self.y13 =  (c_[i+1]*np.sqrt((- c_[i+1]**2 + x_[i+2]**2 + y_[i+2]**2)*(- c_[i+1]**2 + 4*x**2 - 4*x*x_[i+2] + x_[i+2]**2 + y_[i+2]**2)) + c_[i+1]**2*y_[i+2] - x_[i+2]**2*y_[i+2] - y_[i+2]**3 + 2*x*x_[i+2]*y_[i+2])/(2*(c_[i+1]**2 - y_[i+2]**2))
                self.y14 = -(c_[i+1]*np.sqrt((- c_[i+1]**2 + x_[i+2]**2 + y_[i+2]**2)*(- c_[i+1]**2 + 4*x**2 - 4*x*x_[i+2] + x_[i+2]**2 + y_[i+2]**2)) - c_[i+1]**2*y_[i+2] + x_[i+2]**2*y_[i+2] + y_[i+2]**3 - 2*x*x_[i+2]*y_[i+2])/(2*(c_[i+1]**2 - y_[i+2]**2))
            
            x = self.x2
            if not np.isnan(x) and not np.isinf(x):
                self.y21 =  (c_[i]*np.sqrt((- c_[i]**2 + x_[i+1]**2 + y_[i+1]**2)*(- c_[i]**2 + 4*x**2 - 4*x*x_[i+1] + x_[i+1]**2 + y_[i+1]**2)) + c_[i]**2*y_[i+1] - x_[i+1]**2*y_[i+1] - y_[i+1]**3 + 2*x*x_[i+1]*y_[i+1])/(2*(c_[i]**2 - y_[i+1]**2))
                self.y22 = -(c_[i]*np.sqrt((- c_[i]**2 + x_[i+1]**2 + y_[i+1]**2)*(- c_[i]**2 + 4*x**2 - 4*x*x_[i+1] + x_[i+1]**2 + y_[i+1]**2)) - c_[i]**2*y_[i+1] + x_[i+1]**2*y_[i+1] + y_[i+1]**3 - 2*x*x_[i+1]*y_[i+1])/(2*(c_[i]**2 - y_[i+1]**2))
                self.y23 =  (c_[i+1]*np.sqrt((- c_[i+1]**2 + x_[i+2]**2 + y_[i+2]**2)*(- c_[i+1]**2 + 4*x**2 - 4*x*x_[i+2] + x_[i+2]**2 + y_[i+2]**2)) + c_[i+1]**2*y_[i+2] - x_[i+2]**2*y_[i+2] - y_[i+2]**3 + 2*x*x_[i+2]*y_[i+2])/(2*(c_[i+1]**2 - y_[i+2]**2))
                self.y24 = -(c_[i+1]*np.sqrt((- c_[i+1]**2 + x_[i+2]**2 + y_[i+2]**2)*(- c_[i+1]**2 + 4*x**2 - 4*x*x_[i+2] + x_[i+2]**2 + y_[i+2]**2)) - c_[i+1]**2*y_[i+2] + x_[i+2]**2*y_[i+2] + y_[i+2]**3 - 2*x*x_[i+2]*y_[i+2])/(2*(c_[i+1]**2 - y_[i+2]**2))

        pass

    def drawCanvas(self):


        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.grid()

        _max_value = 0
        _min_value = 0

        # draw hyperbola
        for y in self._y:

            if _max_value < max(y) and not any(np.isnan(np.array(y))) and not any(np.isinf(np.array(y))):
                _max_value = max(y)

            if _min_value > min(y) and not any(np.isnan(np.array(y))) and not any(np.isinf(np.array(y))):
                _min_value = min(y)

            # if not any(np.isnan(np.array(y))) and not any(np.isinf(np.array(y))):
            #     self.MplWidget.canvas.axes.plot(self._x, y)

        # draw interscetion points of hyperbola
        if not np.isnan(self.x1) or not np.isinf(self.x1):
            self.MplWidget.canvas.axes.scatter(self.x1, self.y11, marker='x', color='#DC143C',s = 90)
            self.MplWidget.canvas.axes.scatter(self.x1, self.y12, marker='x', color='#15b01a',s = 90)
            self.MplWidget.canvas.axes.scatter(self.x1, self.y13, marker='x', color='#00ffff',s = 90)
            self.MplWidget.canvas.axes.scatter(self.x1, self.y14, marker='x', color='#ffff00',s = 90)
        # draw interscetion points of hyperbola
        if not np.isnan(self.x2) or not np.isinf(self.x2):
            self.MplWidget.canvas.axes.scatter(self.x2, self.y21, marker='x', color='#8c000f',s = 90)
            self.MplWidget.canvas.axes.scatter(self.x2, self.y22, marker='x', color='#008000',s = 90)
            self.MplWidget.canvas.axes.scatter(self.x2, self.y23, marker='x', color='#0343df',s = 90)
            self.MplWidget.canvas.axes.scatter(self.x2, self.y24, marker='x', color='#daa520',s = 90)

        if len(test[0][0]) > 1:
            self.MplWidget.canvas.axes.plot(test[0][0], test[0][1])
            self.MplWidget.canvas.axes.plot(test[1][0], test[1][1])

        self.MplWidget.canvas.axes.set_xlim(-100, 100)
        self.MplWidget.canvas.axes.set_ylim(-100, 100)
        self.MplWidget.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()