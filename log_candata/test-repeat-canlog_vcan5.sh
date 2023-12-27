sudo ../vcan-setup.sh
#sudo modprobe vcan
#sudo ip link add dev vcan0 type vcan
#sudo ip link set vcan0 type can bitrate 125000   #not need for virtual can
#sudo ip link set up vcan0

while true
do
#canplayer vcan0=can_spi0.0 vcan0=can_spi0.1 vcan0=can_spi1.0 vcan0=can_spi1.1 vcan0=can_spi1.2 -I ./candump-2022-02-22_161128_test03-04.log
#sudo vcan-setup.sh
canplayer vcan_spi0.0=can_spi0.0 vcan_spi0.1=can_spi0.1 vcan_spi1.0=can_spi1.0 vcan_spi1.1=can_spi1.1 vcan_spi0.0=can_spi1.2 -I ./candump-2022-02-22_141205_test02-01.log
done
