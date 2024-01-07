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

Download the `ardurover_with_bl.hex` file from the SpeedyBee F405 V4 [beta firmware page](https://firmware.ardupilot.org/Rover/beta/speedybeef4v4/). As of Jan 2nd, 2024 there's been no stable Rover release since 2022 so, you have to use a beta release.

**Update:** a new stable Rover 4.4.0 release came out on Dec 19th, 2023 (and at this time, the beta and stable `.hex` are identical).

Download [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html) (you have to provide a valid email address to download the software so, you might as well register a full account).

Note: the _Get Software_ section may look blank initially - just wait, it's doing an AJAX query to get a table of the latest versions for the various platforms (Windows, Mac and Linux).

Hold-down the BOOT button on the FC while connecting via USB-C. There's no particular indication that it's in DFU mode other than that the flashing blue LED above the red LED never comes on.

Then open the STM32CubeProgrammer and go to the page on [loading firmware onto an STM32 FC](https://ardupilot.org/copter/docs/common-loading-firmware-onto-chibios-only-boards.html). Scroll down to the picture of the STM32CubeProgrammer annotated with arrows numbered 1 to 5 and go through the related steps (i.e. select connection method etc.) and finally hit the _Download_ button (step 7 in the second picture).

That's it - disconnect and reconnect the FC to reboot it into non-DFU mode.

Now, open QGC and it should detect the board and jump to _Vehicle Setup_ and report "Your vehicle requires setup prior to flight" (this is expected).

The following step may be unnecessary but I'm unsure on whether it resets the flash used to store parameters when you do an upgrade like this. So, go to the _Parameters_ tab, select _Tools_ (upper-right) and select _Reset all to firmware's defaults_ and then select _Reboot vehicle_.

**Update:** for Mission Planner, see [here](https://ardupilot.org/copter/docs/common-parameter-reset.html) - go to _Config_, then _Full Parameter Tree_ (left-hand side) and then press _Reset to Default_ (righ-hand side). The FC is automatically rebooted - when I did this it failed (with a stacktrace shown in a dialog) but just pressing the _Connect_ button afterward worked.

I find it odd that resetting the parameters is near instantaneous when reading them, on connecting the device, takes a noticeable amount of time.

### dfu-util

Far easier, once the SpeedyBee F405 V4 bootloader is available (as of Dec 16th, 2023, only the bootloader for the V3 board was available) is to use `dfu-util`.

**Note:** I tried using the bootloader for the V3 board - it almost works but it's the bootloader that tells QGC what kind of board it is and so there's no way to get it to load the V4 firmware rathter than the V3 firmware. See the ArduPilot issue [#25874](https://github.com/ArduPilot/ardupilot/issues/25874) that I logged.

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

Disabled features and PPM/S-BUS
-------------------------------

Initially, I wired up the PPM pins of the JHEMCU PWM to PPM/S-BUS converter (and the non-inverted RX signal pin of the FC).

When you install Betaflight, there's a _Radio Protocol_ dropdown and it defaults to _CSRF,GHST,SBUS_ (at least for the SpeedyBee F405 V4 board) so, it's clear you have to switch to PPM if that's what you want.

With PPM selected, everything worked fine in Betaflight.

Ardupilot can autodetect between S-BUS and PPM so, I thought no special setup would be required. However, it completely failed to read any input from the RX.

It turns out that many Ardupilot features are disabled by default so that everything will fit within the available RAM (see more [here](https://ardupilot.org/copter/docs/common-limited-firmware.html)). There's a table of disabled features for each flight controller [here](https://ardupilot.org/rover/docs/binary-features.html) and the one for the SpeedyBee F405 V4 shows a substantial list of disabled features. And it turns out that the only RX protocol that's disabled is PPM (as no modern RXs use PPM anymore).

So, I switched my setup to S-BUS on both the JHEMCU converter and my FC and Ardupilot could read the RX input (and this could be seen in Mission Planner).

JHEMCU converter
----------------

When the converter powers up initially the red LED above the block of PWM pins is solid as are the green LED beside the PPM pins and the blue LED pins beside the S-BUS pins.

Solid means those pins are treated as input pins.

Once the TX is powered up, the converter works out that there's input data on the PWM pins and switches the PPM and S-BUS pins to output. Their LEDs start flashing to indicate they're in output mode while the red LED remains solid.

For the FlySky GT5, the steering is CH1, the throttle is CH2 and the toggle switch on the grip is CH3.

TODO: check if the unbranded MJX TX maps things the same way.

In Ardupilot Rover, **roll is used for steering** and the default setup is throttle on CH1 and roll on CH3.

So, I connected:

* CH1 of the RX to CH1 of the JHEMCU board.
* CH2 of the RX to CH3 of the JHEMCU board.
* CH3 of the RX to CH5 of the JHEMCU board.

This means Ardupilot sees roll/steering and throttle on the expected channels and sees the grip's toggle switch on CH5 (the first channel that does not have a predefined meaning).

TODO:

* If soldering the JHEMCU board again, I might pull all the unneeded pins from the 5x3 header block and just solder those that are actually needed.
* If soldering the FC RX pins again, I'd use a longer cable with a female connector on the end rather than my currect setup with a shrouded male connector and then an intermediate female-to-female cable.


Mission Planner
---------------

TODO: Mission Planner drawing to the screen is extremely slow - this is odd given that everything else seems pretty snappy in the VM. Is this a known issue (perhaps a result of Mission Planner's 32 bit nature) and is it fixable, e.g. some DirectX driver that plays well with 32 bit apps like Mission Planner?

Windows, like macOS, tries to make it difficult to run anything that isn't signed as being from a recognized published.

In Windows, when you try to run it, it suggests deleting it and gives cancel as the alternative option with no obvious option to actually run it.

You have to select the "see more" bit of the text in the warning dialog and only there do you see the option to run.

A very similar thing happens when the Mission Planner installation also tries to initiate the installation of various drivers.

I had to set up an Altitude Angel account as part of the initial Mission Planner installation (this allows Mission Planner to use Altitude Angel [drone safety map](https://dronesafetymap.com/) data and other features.

TODO: note down the actual dialog text (the above is just what I remember).

---

When the FC is plugged in, the FC's bootloader temporarily appears as a USB device but then disappears and the FC's flight stack (Ardupilot) appears.

As VMWare Fusion detects each of these devices, it asks if you want to connect them to the Mac or to the Windows VM.

Ignore the first VMWare dialog (for the bootloader device), it'll disappear after a second. After a second or two more, it'll show a dialog for "Generic speedybeef4v4", click _Connect to Windows_ for this one.

Initially, the connect dropdown is set to _AUTO_ - when I clicked _Connect_, it correctly detected the FC on COM5 (and from then on it defaulted to COM5).

Note: on detecting the FC, it set the baud rate to 9600 - I _believe_ that the baudrate is irrelevant for these kind of USB-to-serial setups and  as far as I can see all values work and 1,200 baud works as fast as 1,500,000 baud.

ESC and servo
-------------

HERE: rather than using motor 1 and 2 on the ESC connector of the FC, I suspect I should have plugged the signal pin for the ESC into motor 3. See <https://ardupilot.org/rover/docs/common-pixhawk-wiring-and-quick-start.html#connect-motors> - try driving a servo off each motor pin in turn and see what lines up with what (rather than plugging in ESC and servo from start).

See also <https://ardupilot.org/rover/docs/rover-motor-and-servo-configuration.html> the _ESC configuration_ section for how motors are bound.

You need to insert an SD card formatted as exFAT otherwise in messages you see:

```
PreArm: logging failed
```

I set PreArm checks not to include compass and GPS.

Reboot is in a really weird place - press ctrl-F and you'll find it in the right-hand column of buttons in the lower half.

The motor test kept failing with "autopilot denied command".

I had to:

* Set the RC4_TRIM to 2154 and RC4_MIN to 2124 and RC4_MAX to 2184.
* COMPASS_USE to 0
* Disable compass and GPS in ARMING_CHECK.

I don't know which except for the first is crucial - the RC4 channel isn't used and defaults to its max (of 2154) and the arm check complained it wasn't in neutral (why it doesn't RC2 (which is the same), I don't know.

It looks like you need the GPS and compass connected even if you've excluded them from ARMING_CHECK otherwise arm checks complain compass is in bad health (doesn't seem to care about GPS), hence `COMPASS_USE` as well. So, **next time** plug in GPS.

The buzzer is super quiet if powered just by USB.

Motor B corresponds to orange wire and works.

Yellow wire doesn't seem to do anything.

I think I had to put in common ground between my 5V source and the FC setup (I connected one of the ground pins of the JHEMCU converter to ground on the 5V breadboard setup).

Much better is to just wire in the ESC and uses its BEC - that works without any extra wiring.

The red LED on the ESC seems to blink continuously - I don't know if this because it's getting no PWM signal or because it's not connected to a brushless motor.

In the motor test, the default is just to apply 5% (or is it 15%) throttle to each motor - raise this to something higher if you want more than a twitch out of the motor you're testing.

Oddly, the steering servo seems to work even while in disarmed state - i.e. you don't need to go into motor test to test it.

So, current status is:

* YELLOW WIRE DOES NOTHING.
* TRY ADDING ANOTHER WIRE (BEFORE REMOVING YELLOW) FOR MOTOR 3 AND TRYING.
* IS IT JUST STEERING THAT'S ALLOWED WITHOUT ARMING?
* DID THE MJX SERVO JUST NOT WORK BECAUSE THROTTLE % IN MOTOR TEST WAS TOO LOW?
