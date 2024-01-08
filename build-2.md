Build
=====

![ESP32 boards](images/esp32-boards.png)

From left to right:

* LILYGO [TTGO ESP32-Micro CH9102](https://www.aliexpress.com/item/32879336509.html) - this is the only one that doesn't use USB-C, it has USB micro-B connector. Much of the dev-board is empty space - most of the electronics are in the small module soldered to the top of the board. The huge antenna at the top is the [8dBi IPEX antenna](https://www.aliexpress.com/item/32847895603.html) designed to go with it.
* WeAct Studio [ESP32-D0WD-V3](https://www.aliexpress.com/item/1005005645111663.html) with onboard PCB antenna.
* Seeed Studio [XIAO ESP32S3](https://www.seeedstudio.com/XIAO-ESP32S3-p-5627.html) with external antenna.
* WeAct Studio [ESP32-C3FH4](https://www.aliexpress.com/item/1005004960064227.html) with onboard PCB antenna.
* Unbranded [Super Mini ESP32-C3](https://www.aliexpress.com/item/1005005757810089.html) with onboard ceramic antenna.

---

I used a small fret saw to cut apart the 3-row pin header - it worked surprisingly well.

I didn't tin the GPS wire ends.

Oddy, all that came in the GPS bag was the cable (with connector on just one end) and the GPS module - there was no heat shrink. Just like this customer image on Banggood:

<https://imgaz.staticbg.com/customers_images/newlarge/c9/32/2023112104141592-1986091.jpg>

Or these images from a Japanese online store:

* <https://cart.fc2img.com/user_img/goldstonejapan/efacad00c4caf57d9085b9f8a5925d95.JPG>
* <https://cart.fc2img.com/user_img/goldstonejapan/11df52144749239b78e4121e0faec7af.JPG>

I just yanked out the signal wire when creating the servo cable to deans connectors setup.

The buzzer only sounds if there's battery power - I actually replaced the buzzer, believing it dead, before discovering this.

To use PPM, you have to select it as the RX protocol when flashing Betaflight (it defaults to S.BUS and other more modern protocols).

ESP32 - in short only a classic ESP32 board will work, if using the WeAct ESP32-D0WD-V3, you need to install a driver for the USB-to-UART chip they use (on Linux, it's builtin).

Once, I'd connected the DroneBridge to my home AP, trying to set it back to acting as an AP again caused it not to not reappear as an AP and I had to reflash it. Nothing looked obviously wrong when running `idf.py monitor` - I wonder if it was doing something stupid like trying the create an AP with the SSID and password given it to it to connect to my home AP.
