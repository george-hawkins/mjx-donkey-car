Build
=====

QGroundControl
--------------

Ideally, I'd use [Mission Planner](https://ardupilot.org/planner/) but it's only available for Windows. Previously, I've run it from a Windows VM on my Mac which works OK.

But this time I'm going to try [QGroundControl](http://qgroundcontrol.com/) (QGC) - it's nowhere near as commonly used in the hobbyist community but it does run natively on Mac.

Just download the `.dmg` from [here](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/download_and_install.html#macOS).

The app isn't signed and MacOS's latest wease is that you have to do the right-click and selecting _Open_ sequence twice - the first time it offers you the option to throw it away and only on the second try does it offer to open it.

Note: macOS often reports that QGC crashed on closing - just click _OK_.

SpeedyBee
---------

Download latest Rover [beta firmware](https://firmware.ardupilot.org/Rover/beta/speedybeef4v4/) (there's been no stable Rover release since 2022) for the SpeedyBee F405 V4.

Download [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html) (you have to provide a valid email address to download the software so, you might as well register a full account).

Note: the _Get Software_ section may look blank initially - just wait, it's doing an AJAX query to get a table of the latest versions for the various platforms (Windows, Mac and Linux).

Hold-down the BOOT button on the FC while connecting via USB-C. There's no particular indication that it's in DFU mode other than that the flashing blue LED above the red LED never comes on.

Then open the STM32CubeProgrammer and go to the page on [loading firmware onto an STM32 FC](https://ardupilot.org/copter/docs/common-loading-firmware-onto-chibios-only-boards.html). Scroll down to the picture of the STM32CubeProgrammer annotated with arrows numbered 1 to 5 and go through the related steps (i.e. select connection method etc.) and finally hit the _Download_ button (step 7 in the second picture).

That's it - disconnect and reconnect the FC to reboot it into non-DFU mode.

Now, open QGC and it should detect the board and jump to _Vehicle Setup_ and report "Your vehicle requires setup prior to flight" (this is expected).

The following step may be unnecessary but I'm unsure on whether it resets the flash used to store parameters when you do an upgrade like this. So, go to the _Parameters_ tab, select _Tools_ (upper-right) and select _Reset all to firmware's defaults_ and then select _Reboot vehicle_.

I find it odd that resetting the parameters is near instantaneous when reading them, on connecting the device, takes a noticeable amount of time.

### dfu-util

Far easier, once the SpeedyBee F405 V4 bootloader is available (as of Dec 16th, 2023, only the bootloader for the V3 board was available) is to use `dfu-util`.

**Note:** I tried using the bootloader for the V3 board - it almost works but it's the bootloader that tells QGC what kind of board it is and so there's no way to get it to load the V4 firmware rathter than the V3 firmware.

First, download the bootloader file - `speedybeef4v4_bl.bin` (once available) - from <https://firmware.ardupilot.org/Tools/Bootloaders/>

Then:

```
$ brew install dfu-util
$ dfu-util -a 0 --dfuse-address 0x08000000 -D speedybeef4v3_bl.bin
```

Disconnect the FC and start QGC, click the Q icon (upper-left) and select _Vehicle Setup_. Go to the _Firmware_ tab and reconnect the FC.

In the _Firmware Setup_ dialog:

* Select _ArduPilot_.
* Leave the first dropdown showing _ChibiOS_ and change the second dropdown to _Rover_.

As there have been no stable releases, it says _No Firmware Available_. Tick the _Advanced settings_ checkbox and switch from _stable_ to _beta_.

Click _OK_ and it'll start flashing the firmware and then reboot the board.

### Betaflight

If you want to reintall Betaflight later, just start the Configurator then connect the board with the BOOT button held down. The Configurator should detect it as a device in DFU mode and you then need to flash it with _No reboot sequence_ and _Full chip erase_ enabled.
