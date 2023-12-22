# cockpit_monitor_mk-x
Cockpit panel GUI teTra Mk-X

- v1.0.0
![v1.0.0 sample](/document/Screenshot_from_2023-12-22_21-03-31.png)

## Requirement
```
sudo apt install can-utils
sudo apt install net-tools
pip3 install python-can
```

## Debug
- case of vcan
    - terminal 1
```
sudo vcan-setup.sh
canplayer vcan_spi0.0=can_spi0.0 vcan_spi0.1=can_spi0.1 vcan_spi1.0=can_spi1.0 vcan_spi1.1=can_spi1.1 vcan_spi0.0=can_spi1.2 -I ./candump-2022-02-22_141205_test02-01.log
```
    - terminal 2
```
python3 can_recv_draw.py
```

