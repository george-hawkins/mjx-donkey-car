DroneBridge on the Mac
======================

The WeAct ESP32-D0WD-V3 uses a WCH CH34x series USB-to-serial chip which requires a [driver](https://github.com/WCHSoftGroup/ch34xser_macos) to be installed on MacOS.

WCH seems to be a fairly well known brand (similar chips are used in products from Adafruit).

In the end, I actually used my Linux machine as the necessary driver is included.

The Seeed Xiao S3 doesn't need the installation of a driver. The S3 has builtin USB support so there's no requirement for a third-party chip.
