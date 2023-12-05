#!/usr/bin/env python3
"""can_recv.py
CAN0～CAN5メッセージ受信

- Usage
$ python3 can_recv.py
"""
#__all__ = ['sys']
__author__ = "Yoshio Akimoto <yoshio.akimoto@tetra-aviation.com>, Yoshihiro Nakagawa <yoshihiro.nakagawa@tetra-aviation.com>"
__date__ = "14 October 2022"

__version__ = "1.0.0"
__credits__ = "teTra Aviation Corp."

import can

# CANバスの初期化 (#6,#7は未実装。予備)
bus1 = can.interface.Bus(channel = 'can_spi0.0', bustype='socketcan', bitrate=125000, canfilters=None)
bus2 = can.interface.Bus(channel = 'can_spi0.1', bustype='socketcan', bitrate=125000, canfilters=None)
bus3 = can.interface.Bus(channel = 'can_spi1.0', bustype='socketcan', bitrate=125000, canfilters=None)
bus4 = can.interface.Bus(channel = 'can_spi1.1', bustype='socketcan', bitrate=125000, canfilters=None)
bus5 = can.interface.Bus(channel = 'can_spi1.2', bustype='socketcan', bitrate=125000, canfilters=None)
#bus6 = can.interface.Bus(channel = 'can_spi2.0', bustype='socketcan', bitrate=125000, canfilters=None)
#bus7 = can.interface.Bus(channel = 'can_spi2.1', bustype='socketcan', bitrate=125000, canfilters=None)
#bus1 = can.interface.Bus(channel = 'vcan_spi0.0', bustype='socketcan', bitrate=125000, canfilters=None)
#bus2 = can.interface.Bus(channel = 'vcan_spi0.1', bustype='socketcan', bitrate=125000, canfilters=None)
#bus3 = can.interface.Bus(channel = 'vcan_spi1.0', bustype='socketcan', bitrate=125000, canfilters=None)
#bus4 = can.interface.Bus(channel = 'vcan_spi1.1', bustype='socketcan', bitrate=125000, canfilters=None)
#bus5 = can.interface.Bus(channel = 'vcan_spi1.2', bustype='socketcan', bitrate=125000, canfilters=None)
#bus6 = can.interface.Bus(channel = 'vcan_spi2.0', bustype='socketcan', bitrate=125000, canfilters=None)
#bus7 = can.interface.Bus(channel = 'vcan_spi2.1', bustype='socketcan', bitrate=125000, canfilters=None)


# すでに用意されているコールバック関数(can.Listenerクラスのon_message_received関数)をオーバーライド
class CallBackFunction(can.Listener):
  def on_message_received(self, msg):
#    print("hoge")
#    print(hex(msg.arbitration_id)
    print(msg)
#    print(msg.data)
#    print(msg.data.hex())

# コールバック関数のインスタンス生成
call_back_function = CallBackFunction()

# コールバック関数登録
can.Notifier(bus1, [call_back_function, ])
can.Notifier(bus2, [call_back_function, ])
can.Notifier(bus3, [call_back_function, ])
can.Notifier(bus4, [call_back_function, ])
can.Notifier(bus5, [call_back_function, ])
#can.Notifier(bus6, [call_back_function, ])
#can.Notifier(bus7, [call_back_function, ])


# 何もしない処理（受信のコールバックのみ）
try:
  while True:
    pass

except KeyboardInterrupt:
  print('exit')
  bus1.shutdown()
  bus2.shutdown()
  bus3.shutdown()
  bus4.shutdown()
  bus5.shutdown()
#  bus6.shutdown()
#  bus7.shutdown()
  
  
