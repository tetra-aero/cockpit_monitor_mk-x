#!/usr/bin/env python3
"""can_recv_draw.py
- Usage
$ python3 can_recv_draw.py
"""
#__all__ = ['sys']
__author__ = "Yoshio Akimoto <yoshio.akimoto@tetra-aviation.com>, Yoshihiro Nakagawa <yoshihiro.nakagawa@tetra-aviation.com>"
__date__ = "14 October 2022"

__version__ = "1.0.0"
__credits__ = "teTra Aviation Corp."

import sys
import os.path
import string
import re

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt

#from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QFileDialog, QGridLayout, QGraphicsView, QGraphicsScene
#from PyQt5 import QtGui

#import RPi.GPIO as GPIO
#import time

import can

# ESC status Graphic location Data
esc_graph_xy =(
#Front Left
  [70,70], 
  [70,94],
  [136,70],
  [136,94],
  [200,70],
  [200,94],

#Front Right
  [350,70],
  [350,94],
  [414,70],
  [414,94],
  [480,70],
  [480,94],

#Rear Left
  [70,270], 
  [70,294],
  [136,270],
  [136,294],
  [200,270],
  [200,294],

#Rear Right
  [350,270],
  [350,294],
  [414,270],
  [414,294],
  [480,270],
  [480,294],

)


# Contactor Graphic location Data
contact_graph_xy =(
#Front Left
  [51,14], 
  [51+2,121],
  [117,14],
  [117+2,121],
  [182,14],
  [182+3,121],

#Front Right
  [330,14],
  [330+2,121],
  [395,14],
  [395+2,121],
  [461+1,14],
  [461+2,121],

#Rear Left
  [51,212], 
  [53,318],
  [117,212],
  [119,318],
  [183,212],
  [185,318],

#Rear Right
  [330,212],
  [332,318],
  [395,212],
  [397,318],
  [461,212],
  [463,318],

)


#000013: CANID_ESC_voltage
#000020: CANID_ESC_throttle
#000021: CANID_ESC_act_throttle
#000022: CANID_ESC_bus_current
#000023: CANID_ESC_phase_current
#000081: CANID_CANBUS_Health_ask
#000082: CANID_CANBUS_Health_res

#global array
esc_data_v = np.zeros(24)
esc_throttle = np.zeros(24)
esc_active = np.zeros(24)
esc_active_timer = np.zeros(24)

contact_active = np.zeros(24)

class PlotGraph:
    def __init__(self):
          
        # UIを設定
        #self.win = pg.GraphicsWindow(show=True)
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('ESC Voltage')
        self.win.resize(800,600)
        self.plt = self.win.addPlot()
        self.plt.setXRange(0, 24)
        #self.plt.setYRange(0, 50)
        self.plt.setYRange(30, 56)
        self.curve = self.plt.plot(pen=(0, 0, 255))

        self.win.show()

        # データを更新する関数を呼び出す時間を設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        #self.data = np.zeros(32)
        #esc_data_v = np.zeros(32)

    #graphic data update
    def update(self):

        #Making 32 sample datas (Random)
        #for i in range(0, 32):
        #    self.data[i] = self.voltage_list[i] + np.random.rand() * 5
        x = np.arange(24)
        #y1 = np.linspace(0, 20, num=64)

        #棒グラフ描画
        # <!> 重要 : プロットを描画する前に、古い描画を消しておく（重ね描きになってしまう） 
        self.plt.clear()
        # data配列をデータとした、緑の棒グラフを作成
        bg1 = pg.BarGraphItem(x=x, height=esc_data_v, width=0.6, brush='g')
        self.plt.addItem(bg1)

class PlotGraph2:
    def __init__(self):
        
        # UIを設定 2
        #self.win2 = pg.GraphicsWindow()
        self.win2 = pg.GraphicsLayoutWidget(show=True)
        self.win2.setWindowTitle('ESC throttle')
        self.plt2 = self.win2.addPlot()
        self.plt2.setXRange(0, 24)
        self.plt2.setYRange(0, 1000)
        self.curve2 = self.plt2.plot(pen=(0, 0, 255))

        self.win2.show()

        # データを更新する関数を呼び出す時間を設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        #self.data = np.zeros(32)
        #esc_throttle = np.zeros(32)


    #graphic data update
    def update(self):

        #Making 32 sample datas (Random)
        #for i in range(0, 32):
        #    self.data[i] = self.voltage_list[i] + np.random.rand() * 5
        x = np.arange(24)
        #y1 = np.linspace(0, 20, num=64)

        #棒グラフ描画
        # <!> 重要 : プロットを描画する前に、古い描画を消しておく（重ね描きになってしまう） 
        self.plt2.clear()
        # data配列をデータとした、赤の棒グラフを作成
        bg2 = pg.BarGraphItem(x=x, height=esc_throttle, width=0.6, brush='r')
        self.plt2.addItem(bg2)


class LineGraph:
    def __init__(self):
        # UIを設定
        #self.win = pg.GraphicsWindow()
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle('Avr.Voltage #24')
        self.plt = self.win.addPlot()
        self.plt.setYRange(30, 56)
        self.plt.setXRange(0, 10*60*10) #10min
        self.curve = self.plt.plot(pen=(0, 255, 0))

        # データを更新する関数を呼び出す時間を設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        self.data = np.zeros(100)

    def update(self):
        #self.data = np.delete(self.data, 0)
        avr_esc_data_v = np.mean(esc_data_v)
        #self.data = np.append(self.data, esc_data_v[0])
        self.data = np.append(self.data, avr_esc_data_v)
        self.curve.setData(self.data)



# CANバスの初期化 (#6,#7は未実装。予備)
'''
bus1 = can.interface.Bus(channel = 'can_spi0.0', bustype='socketcan', bitrate=125000, canfilters=None)   #Front Right wing from AvioDsubBoard and Physical Harness
bus2 = can.interface.Bus(channel = 'can_spi0.1', bustype='socketcan', bitrate=125000, canfilters=None)   #Front Left  wing from AvioDsubBoard and Physical Harness
bus3 = can.interface.Bus(channel = 'can_spi1.0', bustype='socketcan', bitrate=125000, canfilters=None)   #Rear  Right wing from AvioDsubBoard and Physical Harness
bus4 = can.interface.Bus(channel = 'can_spi1.1', bustype='socketcan', bitrate=125000, canfilters=None)   #Rear  Left  wing from AvioDsubBoard and Physical Harness
'''
#bus5 = can.interface.Bus(channel = 'can_spi1.2', bustype='socketcan', bitrate=125000, canfilters=None)
#bus6 = can.interface.Bus(channel = 'can_spi2.0', bustype='socketcan', bitrate=125000, canfilters=None)
#bus7 = can.interface.Bus(channel = 'can_spi2.1', bustype='socketcan', bitrate=125000, canfilters=None)
#bus1 = can.interface.Bus(channel = 'vcan0', bustype='socketcan', bitrate=125000, canfilters=None)

bus1 = can.interface.Bus(channel = 'vcan_spi0.0', bustype='socketcan', bitrate=125000, canfilters=None)
bus2 = can.interface.Bus(channel = 'vcan_spi0.1', bustype='socketcan', bitrate=125000, canfilters=None)
bus3 = can.interface.Bus(channel = 'vcan_spi1.0', bustype='socketcan', bitrate=125000, canfilters=None)
bus4 = can.interface.Bus(channel = 'vcan_spi1.1', bustype='socketcan', bitrate=125000, canfilters=None)

#bus5 = can.interface.Bus(channel = 'vcan_spi1.2', bustype='socketcan', bitrate=125000, canfilters=None)
#bus6 = can.interface.Bus(channel = 'vcan_spi2.0', bustype='socketcan', bitrate=125000, canfilters=None)
#bus7 = can.interface.Bus(channel = 'vcan_spi2.1', bustype='socketcan', bitrate=125000, canfilters=None)

def send_ecu_check():
    #000081: CANID_CANBUS_Health_ask
    for i in range(0, 6):   #Gachacon 1-6, Front Left wing   #range(0, 6) -> 0-5
        msg = can.Message(arbitration_id = 0x08100 + i + 1,
                     data= [1,2,3,4],
                     is_extended_id = True)
        bus2.send(msg)

    for i in range(6, 12):   #Gachacon 7-12, Front Right wing   #range(6, 12) -> 6-11
        msg = can.Message(arbitration_id = 0x08100 + i + 1,
                     data= [1,2,3,4],
                     is_extended_id = True)
        bus1.send(msg)

    for i in range(12, 18):   #Gachacon 13-18, Rear Left wing   #range(12, 18) -> 12-17
        msg = can.Message(arbitration_id = 0x08100 + i + 1,
                     data= [1,2,3,4],
                     is_extended_id = True)
        bus4.send(msg)

    for i in range(18, 24):   #Gachacon 19-24, Rear Right wing   #range(18, 24) -> 18-23
        msg = can.Message(arbitration_id = 0x08100 + i + 1,
                     data= [1,2,3,4],
                     is_extended_id = True)
        bus3.send(msg)

    #GUI status change
    for i in range(0, 24):
        esc_active[i] = 2   # 2= Yellow
        #esc_active_timer[i] = 3 * 10 # 3sec

def send_contactor_on():
    #000012: contactor_on
    for i in range(0, 6):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0xC0],
                     is_extended_id = True)
        bus2.send(msg)
        contact_active[i] = 1

    for i in range(6, 12):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0xC0],
                     is_extended_id = True)
        bus1.send(msg)
        contact_active[i] = 1

    for i in range(12, 18):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0xC0],
                     is_extended_id = True)
        bus4.send(msg)
        contact_active[i] = 1

    for i in range(18, 24):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0xC0],
                     is_extended_id = True)
        bus3.send(msg)
        contact_active[i] = 1


def send_contactor_off():
    #000012: contactor_off
    for i in range(0, 6):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0x00],
                     is_extended_id = True)
        bus2.send(msg)
        contact_active[i] = 2

    for i in range(6, 12):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0x00],
                     is_extended_id = True)
        bus1.send(msg)
        contact_active[i] = 2

    for i in range(12, 18):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0x00],
                     is_extended_id = True)
        bus4.send(msg)
        contact_active[i] = 2

    for i in range(18, 24):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0x00],
                     is_extended_id = True)
        bus3.send(msg)
        contact_active[i] = 2



class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Window set
        self.resize(720, 400)
        self.setWindowTitle('Body Info.')

        # Button 1 set
        button1 = QPushButton('ECU CHK', self)
        button1.clicked.connect(send_ecu_check)
        button1.move(580,10)


        # Button 2 set
        button2 = QPushButton('CONTACT ON', self)
        button2.clicked.connect(send_contactor_on)
        button2.move(580,50)


        # Button 3 set
        button3 = QPushButton('CONTACT OFF', self)
        button3.clicked.connect(send_contactor_off)
        button3.move(580,80)


        # データを更新する関数を呼び出す時間を設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def paintEvent(self, event):
  
        painter = QPainter(self)

	# Draw body Image
        painter.drawPixmap(0,0,QPixmap("mk5_image.png"))


        # ESC status monitor count down
        #for i in range(0, 24):   
        #    if esc_active_timer[i] ==0: 
        #        esc_active[i] = 0 # 0 : Black
        #
        #    elif esc_active[i] != 2: # 2 : Yellow
        #        esc_active_timer[i] = esc_active_timer[i] -1 


        # ESC status Draw
        painter.setPen(Qt.red)
        for i in range(0, 24):
            if esc_active[i] == 3:
                painter.setBrush(Qt.green)
            elif esc_active[i] == 2:
                painter.setBrush(Qt.yellow)                
            elif esc_active[i] == 1:
                painter.setBrush(Qt.red)                
            else:
                painter.setBrush(Qt.black)                
            painter.drawRect(esc_graph_xy[i][0], esc_graph_xy[i][1],15,20)

        # Contactor status Draw
        painter.setBrush(Qt.NoBrush)
        for i in range(0, 24):
            if contact_active[i] == 1:
                painter.setPen(Qt.red)
            else:
                painter.setPen(Qt.white)
            rectangle = QtCore.QRectF(contact_graph_xy[i][0], contact_graph_xy[i][1], 49.0, 49.0)       
            painter.drawEllipse(rectangle)
    
        # White paint Full screen.
        #painter.setPen(Qt.NoPen)
        #painter.setBrush(Qt.white)
        #painter.drawRect(self.rect())









# すでに用意されているコールバック関数(can.Listenerクラスのon_message_received関数)をオーバーライド
class CallBackFunction(can.Listener):
  def on_message_received(self, msg):
#    print("hoge")
#    print(hex(msg.arbitration_id))
#    print(msg)
#    print(msg.data)
#    print(msg.data.hex())

    #Making 32 sample datas (Random)
    #for i in range(0, 32):
    #    esc_data_v[i] = 40 + np.random.rand() * 5


    #000013: CANID_ESC_voltage
    #ESC Volt (ID=0x13) Pickup
    if re.search("0x13", hex(msg.arbitration_id)) != None:
        #print(msg)
        #ESC ID
        #print(hex(msg.arbitration_id)[-2:])
        #ESC Volt data
        #print((msg.data.hex())[1:])

        #Making 32 sample datas (Random)
        #for i in range(0, 32):
        #    esc_data_v[i] = 40 + np.random.rand() * 5

        id = int(hex(msg.arbitration_id)[-2:],16)
        if id <= 24: # MAX ID number check
            esc_data_v[id] = int((msg.data.hex())[1:],16)/10
            esc_active[id] = 3 # green
            #esc_active_timer[id] = 3*10 # 3sec

    #000020: CANID_ESC_throttle
    #ESC throttle (ID=0x20) Pickup
    if re.search("0x20", hex(msg.arbitration_id)) != None:
        #print(msg)
        #ESC ID
        #print(hex(msg.arbitration_id)[-2:])
        #ESC Volt data
        #print((msg.data.hex())[1:])

        id = int(hex(msg.arbitration_id)[-2:],16)
        if id <= 24: # MAX ID number check
            esc_throttle[id] = int((msg.data.hex())[1:],16)
            esc_active[id] = 3 # green
            #esc_active_timer[id] = 3*10 # 3sec

    #000082: CANID_CANBUS_Health_res
    #ESC Active (ID=0x82) Pickup
    if re.search("0x82", hex(msg.arbitration_id)) != None:
        print(msg)

        id = int(hex(msg.arbitration_id)[-2:],16)
        if id <= 34: # MAX ID number check
            esc_active[id] = 3 # 3:green
            #esc_active_timer[id] = 3*10 # 3sec
        

# コールバック関数のインスタンス生成
call_back_function = CallBackFunction()

# コールバック関数登録
can.Notifier(bus1, [call_back_function, ])
can.Notifier(bus2, [call_back_function, ])
can.Notifier(bus3, [call_back_function, ])
can.Notifier(bus4, [call_back_function, ])
#can.Notifier(bus5, [call_back_function, ])
#can.Notifier(bus6, [call_back_function, ])
#can.Notifier(bus7, [call_back_function, ])


# 何もしない処理（受信のコールバックのみ）
if __name__ == "__main__":
    app = QApplication([])

    #beep_pin = 6 #No.31 pin 
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(beep_pin, GPIO.OUT)
    #GPIO.output(beep_pin, False)

    graphWin = PlotGraph()
    graphWin2 = PlotGraph2()
    graphWin3 = LineGraph()

    graphWin4 = Widget()
    graphWin4.show()
    graphWin4.raise_()

    #for i in range(4):
    #    GPIO.output(beep_pin, True) 
    #    time.sleep(0.2)
    #    GPIO.output(beep_pin, False)
    #    time.sleep(0.1)

    #graphWin4 = PlotGraph2()
    #graphWin5 = PlotGraph2()
    #graphWin6 = PlotGraph2()
    #graphWin = main()   
    
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        #QtGui.QApplication.instance().exec_()
        pg.exec()

#except KeyboardInterrupt:
        print('exit')
        #GPIO.output(beep_pin, False)
        bus1.shutdown()
        bus2.shutdown()
        bus3.shutdown()
        bus4.shutdown()
#        bus5.shutdown()
##  bus6.shutdown()
##  bus7.shutdown()
  
  