#!/usr/bin/env python3
"""can_recv_draw.py
- Usage
$ python3 can_recv_draw.py
"""
#__all__ = ['sys']
__author__ = "Yoshio Akimoto <yoshio.akimoto@tetra-aviation.com>, Yoshihiro Nakagawa <yoshihiro.nakagawa@tetra-aviation.com>"
__date__ = "22 Decembar 2023"

__version__ = "0.9.2"
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
    [170,342], 
    [420,342],
    #Front Right
    [788,342],
    [1040,342],
    #Rear Left
    [170,412], 
    [420,412],
    #Rear Right
    [788,412],
    [1040,412],
    #Pusher
    [605, 275],
)

# Contactor Graphic location Data
contact_graph_xy =(
#Front Left
  [183-25,568-25], 
  [429-25,597-25],

#Front Right
  [802-25,597-25],
  [1049-25,568-25],

#Rear Left
  [183-25,253-25], 
  [429-25,227-25],

#Rear Right
  [802-25,227-25],
  [1049-25,253-25],

#Pusher
  [616-25,252-25],
)

#000013: CANID_ESC_voltage
#000020: CANID_ESC_throttle
#000021: CANID_ESC_act_throttle
#000022: CANID_ESC_bus_current
#000023: CANID_ESC_phase_current
#000081: CANID_CANBUS_Health_ask
#000082: CANID_CANBUS_Health_res

number_of_esc = 9

#global array
esc_data_v = np.zeros(9)
esc_throttle = np.zeros(9)
esc_active = np.zeros(9)
esc_active_timer = np.zeros(9)

contact_active = np.zeros(9)

class PlotGraph:
    def __init__(self):
          
        # UIを設定
        #self.win = pg.GraphicsWindow(show=True)
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('ESC Voltage')
        self.win.resize(800,600)
        self.plt = self.win.addPlot()
        self.plt.setXRange(0, number_of_esc)
        #self.plt.setYRange(0, 50)
        self.plt.setYRange(30, 56)
        self.curve = self.plt.plot(pen=(0, 0, 255))

        self.win.show()

        # データを更新する関数を呼び出す時間を設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        #self.data = np.zeros(number_of_esc)
        #esc_data_v = np.zeros(number_of_esc)

    #graphic data update
    def update(self):

        #Making number_of_esc sample datas (Random)
        #for i in range(0, number_of_esc):
        #    self.data[i] = self.voltage_list[i] + np.random.rand() * 5
        x = np.arange(number_of_esc)
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
        self.plt2.setXRange(0, number_of_esc)
        self.plt2.setYRange(0, 1000)
        self.curve2 = self.plt2.plot(pen=(0, 0, 255))

        self.win2.show()

        # データを更新する関数を呼び出す時間を設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        #self.data = np.zeros(number_of_esc)
        #esc_throttle = np.zeros(number_of_esc)


    #graphic data update
    def update(self):

        #Making number_of_esc sample datas (Random)
        #for i in range(0, number_of_esc):
        #    self.data[i] = self.voltage_list[i] + np.random.rand() * 5
        x = np.arange(number_of_esc)
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
        self.win.setWindowTitle('Avr.Voltage #9')
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
    for i in range(0, 1):   #Gachacon 1-6, Front Left wing   #range(0, 6) -> 0-5
        msg = can.Message(arbitration_id = 0x08100 + i + 1,
                     data= [1,2,3,4],
                     is_extended_id = True)
        bus2.send(msg)

    for i in range(2, 3):   #Gachacon 7-12, Front Right wing   #range(6, 12) -> 6-11
        msg = can.Message(arbitration_id = 0x08100 + i + 1,
                     data= [1,2,3,4],
                     is_extended_id = True)
        bus1.send(msg)

    for i in range(4, 5):   #Gachacon 13-18, Rear Left wing   #range(12, 18) -> 12-17
        msg = can.Message(arbitration_id = 0x08100 + i + 1,
                     data= [1,2,3,4],
                     is_extended_id = True)
        bus4.send(msg)

    for i in range(6, 7):   #Gachacon 19-8, Rear Right wing   #range(18, 8) -> 18-23
        msg = can.Message(arbitration_id = 0x08100 + i + 1,
                     data= [1,2,3,4],
                     is_extended_id = True)
        bus3.send(msg)

    #GUI status change
    for i in range(0, number_of_esc):
        esc_active[i] = 2   # 2= Yellow
        #esc_active_timer[i] = 3 * 10 # 3sec


def send_contactor_on():
    #000012: contactor_on
    for i in range(0, 1):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0xC0],
                     is_extended_id = True)
        bus2.send(msg)
        contact_active[i] = 1

    for i in range(2, 3):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0xC0],
                     is_extended_id = True)
        bus1.send(msg)
        contact_active[i] = 1

    for i in range(4, 5):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0xC0],
                     is_extended_id = True)
        bus4.send(msg)
        contact_active[i] = 1

    for i in range(6, 7):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0xC0],
                     is_extended_id = True)
        bus3.send(msg)
        contact_active[i] = 1


def send_contactor_off():
    #000012: contactor_off
    for i in range(0, 1):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0x00],
                     is_extended_id = True)
        bus2.send(msg)
        contact_active[i] = 2

    for i in range(2, 3):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0x00],
                     is_extended_id = True)
        bus1.send(msg)
        contact_active[i] = 2

    for i in range(4, 5):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0x00],
                     is_extended_id = True)
        bus4.send(msg)
        contact_active[i] = 2

    for i in range(6, 7):        
        msg = can.Message(arbitration_id = 0x01200 + i + 1,
                     data= [0x00],
                     is_extended_id = True)
        bus3.send(msg)
        contact_active[i] = 2


class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Window set
        #self.resize(720, 400)
        self.resize(1232, 688)
        self.setWindowTitle('Body Info.')

        # Button 1 set
        button1 = QPushButton('ECU CHK', self)
        button1.clicked.connect(send_ecu_check)
        button1.move(1000,10)

        # Button 2 set
        button2 = QPushButton('CONTACT ON', self)
        button2.clicked.connect(send_contactor_on)
        button2.move(1000,50)

        # Button 3 set
        button3 = QPushButton('CONTACT OFF', self)
        button3.clicked.connect(send_contactor_off)
        button3.move(1000,80)

        # データを更新する関数を呼び出す時間を設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def paintEvent(self, event):
  
        painter = QPainter(self)
	    
        # Draw body Image
        #painter.drawPixmap(0,0,QPixmap("./document/mk5_sn4_image.png"))
        painter.drawPixmap(0,0,QPixmap("./document/mkx_sn1_image.png"))

        # ESC status monitor count down
        #for i in range(0, number_of_esc):   
        #    if esc_active_timer[i] ==0: 
        #        esc_active[i] = 0 # 0 : Black
        #
        #    elif esc_active[i] != 2: # 2 : Yellow
        #        esc_active_timer[i] = esc_active_timer[i] -1 

        # ESC status Draw
        painter.setPen(Qt.red)
        for i in range(0, number_of_esc):
            if esc_active[i] == 3:
                painter.setBrush(Qt.green)
            elif esc_active[i] == 2:
                painter.setBrush(Qt.yellow)                
            elif esc_active[i] == 1:
                painter.setBrush(Qt.red)                
            else:
                painter.setBrush(Qt.black)                
            painter.drawRect(esc_graph_xy[i][0], esc_graph_xy[i][1],25,25)

        # Contactor status Draw
        painter.setBrush(Qt.NoBrush)
        for i in range(0, number_of_esc):
            if contact_active[i] == 1:
                painter.setPen(Qt.red)
            else:
                painter.setPen(Qt.white)
            rectangle = QtCore.QRectF(contact_graph_xy[i][0], contact_graph_xy[i][1], 50.0, 50.0)       
            painter.drawEllipse(rectangle)
    
        # White paint Full screen.
        #painter.setPen(Qt.NoPen)
        #painter.setBrush(Qt.white)
        #painter.drawRect(self.rect())


# すでに用意されているコールバック関数(can.Listenerクラスのon_message_received関数)をオーバーライド
class CallBackFunction(can.Listener):
    def on_message_received(self, msg):
        #print("hoge")
        #print(hex(msg.arbitration_id))
        #print(msg)
        #print(msg.data)
        #print(msg.data.hex())
        
        #Making 32 sample datas (Random)
        #for i in range(0, 32):
            #esc_data_v[i] = 40 + np.random.rand() * 5
            
        #000013: CANID_ESC_voltage
        #ESC Volt (ID=0x13) Pickup
        if re.search("0x13", hex(msg.arbitration_id)) != None:
            #print(msg)
            #ESC ID
            #print(hex(msg.arbitration_id)[-2:])
            #ESC Volt data
            #print((msg.data.hex())[1:])

            #Making number_of_esc sample datas (Random)
            #for i in range(0, number_of_esc):
            #    esc_data_v[i] = 40 + np.random.rand() * 5

            id = int(hex(msg.arbitration_id)[-2:],16)

            #if id == 8:
            #print(id)
            
            #if id <= number_of_esc: # MAX ID number check
            if id < number_of_esc: # MAX ID number check
                voltage_hex = (msg.data.hex())[1:]
                esc_data_v[id] = int(voltage_hex,16)/10
                #esc_data_v[id] = int((msg.data.hex())[1:],16)
                #esc_data_v[id] = int((msg.data.hex())[1:],16)/10
                #print('{}, {}'.format(id, esc_data_v[id]))
                #print(", ")
                #print(esc_data_v[id])
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
            #if id <= number_of_esc: # MAX ID number check
            if id < number_of_esc: # MAX ID number check
                esc_throttle[id] = int((msg.data.hex())[1:],16)
                esc_active[id] = 3 # green
                #esc_active_timer[id] = 3*10 # 3sec

        #000082: CANID_CANBUS_Health_res
        #ESC Active (ID=0x82) Pickup
        if re.search("0x82", hex(msg.arbitration_id)) != None:
            print(msg)

            id = int(hex(msg.arbitration_id)[-2:],16)
            #if id <= number_of_esc: # MAX ID number check
            if id < number_of_esc: # MAX ID number check
                esc_active[id] = 3 # 3:green
                #esc_active_timer[id] = 3*10 # 3sec
            #pass
        #pass
    #pass
#pass

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
  
  