DroneBridge on the Mac
======================

Skip to _Update_ section below.

---

The WeAct ESP32-D0WD-V3 uses a WCH CH34x series USB-to-serial chip which requires a driver to be installed on MacOS.

The drvier is available from:

* The WCH website - <https://www.wch-ic.com/downloads/CH34XSER_MAC_ZIP.html>
* GitHub - <https://github.com/WCHSoftGroup/ch34xser_macos>

The version on both sites is the same (1.8 as of Dec 21st, 2023).

Adafruit have better installation instructions than WCH [here](https://learn.adafruit.com/how-to-install-drivers-for-wch-usb-to-serial-chips-ch9102f-ch9102/mac-driver-installation).

WCH seems to be a fairly well known brand. Adafruit say [here](https://learn.adafruit.com/how-to-install-drivers-for-wch-usb-to-serial-chips-ch9102f-ch9102) that they are using the WCH USB-to-serial chips in their new designs rather than the SiLabs chips that they used to use.

In the end, I actually used my Linux machine as the necessary driver is included.

The Seeed Xiao S3 doesn't need the installation of a driver. The S3 has builtin USB support so there's no requirement for a third-party USB-to-serial chip.

Update
------

S3 and C3 boards don't require the installation of a driver and since DroneBridge/ESP32 v1.3, the C3 is supported.

I used a WeAct Studio [ESP32-C3H4 Core Board](https://www.aliexpress.com/item/1005004960064227.html). If you want to try a board that supports an external antenna (and so, _may_ have better range), try the Seeed Studio [Xiao ESP32C3](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html). Or if you want something as tiny as the Xiao but with a built-in antenna, try this no-brand [ESP32-C3 Super Mini](https://www.aliexpress.com/item/1005005757810089.html) board (Adafruit have the similar [QT Py ESP32-C3](https://www.adafruit.com/product/5405) for quite a lot more but still just US$10).

So, all that's required is...

**1.** Install `esptool`:

```
$ python3 -m venv env
$ source env/bin/activate
$ pip install --upgrade pip
$ pip install esptool
```

**2.** Find the device corresponding to the connected C3 board:

```
$ ls /dev/cu.usbmodem*
$ device=/dev/cu.usbmodem1101
```

**3.** Erase the flash on the board:

```
$ esptool.py -p $device erase_flash
```

**4.** Get the latest C3 release from the [releases page](https://github.com/DroneBridge/ESP32/releases) and:

```
$ mv ~/Downloads/DroneBridge_v1_3_ESP32C3.zip .
$ unzip DroneBridge_v1_3_ESP32C3.zip
$ cd DroneBridge_v1_3_ESP32C3/
```

**5.** And then flash the contained `.bin` files to the board:

```
$ esptool.py \
    -p $device \
    -b 460800 \
    --before default_reset \
    --after hard_reset \
    --chip esp32c3  write_flash \
    --flash_mode dio \
    --flash_size 2MB \
    --flash_freq 80m \
    0x0 bootloader.bin \
    0x8000 partition-table.bin \
    0x10000 db_esp32.bin \
    0x110000 www.bin
```

**6.** Then open the link <http://192.168.2.1/> in a browser (the link <http://dronebridge.local/> may also work).

I found the link never worked on my Pixel (for either a classic ESP32 board or a C3 one) but worked fine (except for this [issue](https://github.com/DroneBridge/ESP32/issues/53) which has been addressed) on my MacBook Air. Interestingly, the author reports the opposite experience [here](https://github.com/DroneBridge/ESP32/releases/tag/v1.3) (search for "load errors" line).

Important
---------

Don't forget to change from _WiFi Access Point Mode_ to _WiFi Client Mode_ when entering your WiFi SSID and passphrase otherwise it just starts an AP using the same SSID and passphrase.

The C3 never seemed to be able to connect to my WiFi.

I spent a lot of time wondering why QGC couldn't connect and it turned out it was the DroneBridge didn't have the correct baud setting for the FC - it defaulted to 115k and I'd set my FC to 56k.

Setting up the UDP link in QGC is a bit weird:

* Click the Q icon (upper left).
* Select _Application Settings_.
* Go to _Comm Links_.
* Click _Add_ and change the _Type_ to _UDP_ and set the name to e.g. "DroneBridge" and enter 14550 as the _Port_.

When DroneBridge is in AP point mode it sees each device that joins its network and automatically starts publishing to port 14550 on that device.

If the DroneBridge was not in AP mode, I _guess_ you'd specify it as a _Server Address_ as I can't see how it would know who to publish to. But probably easier to use TCP.

UDP won't work for Mission Planner running in a VMware Fusion VM as port forwarding requires a Pro license.

But TCP does work - you have to select TCP, click connect then specify 192.168.2.1 as the host and confirm 5760 as the port.

Note: several times, I've had Mission Planner appear to succeed in connecting but if I waggle the FC no corresponding motion is seen on the Mission Planner artifical horizon. Disconnecting and reconnecting seems to fix this.
