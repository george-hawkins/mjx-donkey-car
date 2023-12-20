DroneBridge on the Mac
======================

The WeAct ESP32-D0WD-V3 uses a WCH CH34x series USB-to-serial chip which requires a driver to be installed on MacOS.

The drvier is available from:

* The WCH website - <https://www.wch-ic.com/downloads/CH34XSER_MAC_ZIP.html>
* GitHub - <https://github.com/WCHSoftGroup/ch34xser_macos>

The version on both sites is the same (1.8 as of Dec 21st, 2023).

Adafruit have better installation instructions than WCH [here](https://learn.adafruit.com/how-to-install-drivers-for-wch-usb-to-serial-chips-ch9102f-ch9102/mac-driver-installation).

WCH seems to be a fairly well known brand. Adafruit say [here](https://learn.adafruit.com/how-to-install-drivers-for-wch-usb-to-serial-chips-ch9102f-ch9102) that they are using the WCH USB-to-serial chips in their new designs rather than the SiLabs chips that they used to use.

In the end, I actually used my Linux machine as the necessary driver is included.

The Seeed Xiao S3 doesn't need the installation of a driver. The S3 has builtin USB support so there's no requirement for a third-party USB-to-serial chip.
