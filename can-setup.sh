#!/bin/sh
sudo ip link set dev can0 down
sudo ip link set dev can1 down
sudo ip link set dev can2 down
sudo ip link set dev can3 down
sudo ip link set dev can4 down

sudo ip link set dev can0 type can bitrate 125000
sudo ip link set dev can1 type can bitrate 125000
sudo ip link set dev can2 type can bitrate 125000
sudo ip link set dev can3 type can bitrate 125000
sudo ip link set dev can4 type can bitrate 125000

sudo ip ifconfig can0 txqueuelen 1000
sudo ip ifconfig can1 txqueuelen 1000
sudo ip ifconfig can2 txqueuelen 1000
sudo ip ifconfig can3 txqueuelen 1000
sudo ip ifconfig can4 txqueuelen 1000

#cangw -A -s can_spi1.2 -d can_spi0.0 -e
#cangw -A -s can_spi1.2 -d can_spi0.1 -e
#cangw -A -s can_spi1.2 -d can_spi1.0 -e
#cangw -A -s can_spi1.2 -d can_spi1.1 -e

#cangw -A -s can_spi0.0 -d can_spi1.2 -e
#cangw -A -s can_spi0.1 -d can_spi1.2 -e
#cangw -A -s can_spi1.0 -d can_spi1.2 -e
#cangw -A -s can_spi1.1 -d can_spi1.2 -e

sudo ip link set dev can0 up
sudo ip link set dev can1 up
sudo ip link set dev can2 up
sudo ip link set dev can3 up
sudo ip link set dev can4 up
