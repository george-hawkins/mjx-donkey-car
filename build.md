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

**Update:** the issue has since been resolved. Note: the documentation points one at <https://firmware.ardupilot.org/Tools/Bootloaders/> - but it seems that <https://github.com/ArduPilot/ardupilot/tree/master/Tools/bootloaders> is more up-to-date and `firmware.ardupilot.org` isn't automatically synced with it.

First, download the bootloader file - `speedybeef4v4_bl.bin` from <https://github.com/ArduPilot/ardupilot/tree/master/Tools/bootloaders>

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

The ArduPilot [RC input](https://github.com/ArduPilot/ardupilot/blob/master/libraries/AP_HAL_ChibiOS/hwdef/speedybeef4v4/README.md#rc-input) section of the `hwdef` `README` for the SpeedyBee F405 v4 actually says "PPM is not supported" but as it works fine with Betaflight, I assume it's just pointing out that support is disable _by default_ (but one could compile a suitable image with PPM enabled).

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

I had to set up an Altitude Angel account as part of the initial Mission Planner installation (this allows Mission Planner to use Altitude Angel [drone safety map](https://dronesafetymap.com/) data and other features).

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

**Update:** you can set `COMPASS_USE` via _Setup / Mandatory Hardware / Compass_ and tick/untick _Use Compass 1_.

I don't know which except for the first is crucial - the RC4 channel isn't used and defaults to its max (of 2154) and the arm check complained it wasn't in neutral (why it doesn't RC2 (which is the same), I don't know.

It looks like you need the GPS and compass connected even if you've excluded them from ARMING_CHECK otherwise arm checks complain compass is in bad health (doesn't seem to care about GPS), hence `COMPASS_USE` as well. So, **next time** plug in GPS.

The buzzer is super quiet if powered just by USB.

Motor B corresponds to orange wire and works.

Yellow wire doesn't seem to do anything.

I think I had to put in common ground between my 5V source and the FC setup (I connected one of the ground pins of the JHEMCU converter to ground on the 5V breadboard setup).

Much better is to just wire in the ESC and uses its BEC - that works without any extra wiring.

The red LED on the ESC seems to blink continuously - I don't know if this because it's getting no PWM signal or because it's not connected to a brushless motor.

**Update:** it blinks even if the motor is connected - it blinks until the PWM signal is connected. After that it blinks when the motor is turning.

In the motor test, the default is just to apply 5% throttle to each motor - raise this to something higher if you want more than a twitch out of the motor you're testing.

At 5% one of my servos didn't respond at all and one just twitched. And note that at 100% the servo just turns thru 50% of it's range as it just goes full one way from it's mid point and back to the mid point rather than going from its min to its max.

Oddly, the steering servo seems to work even while in disarmed state - i.e. you don't need to go into motor test to test it.

The throttle, i.e. the wire to the ESC, however has to be tested via the motor test (or by fully arming the FC).

As before, I find it odd that most everywhere the motors are labelled 1 to 4 while in the motor tester they're labeled a to d _and_ it's a non-obvious mapping.

For the rover:

steering = motor 1 = b
throttle = motor 3 = a

Yes, that's not a mistake _a_ isn't 1.

For a four motor quadcopter setup the motors are labeled 1 to 4 starting at front right and going clockwise while, for motor testing, they're labeled A to C starting front right as well but going clockwise.

See <https://github.com/george-hawkins/arf-drone/blob/docusaurus/docs/assets/images/assembly/frame/arm-numbering.svg>

TODO: 

Connect the GPS so you can get rid of bad compass (now that I've got `COMPASS_USE` set to 0, it seems to be gone from the Mssages tab but still appears in the HUD).
Connect up the brushed motor
Blank the FC and see that you can still test the motors.
You don't need the TX powered up to test the motors - initially I thought this was necessary
BUT check it's not necessary just because I disabled RC ARM checks.
REMEMBER you may still have to set RC4_TRIM etc. as above - work out how to get to a state where this isn't needed.
Get some photos of the full setup with charger as desktop power supply.
Note: the horn on the MJX servo comes from the Emax servo.
Go to the _Install firmware_ tab - I'm curious if Rover icon shows there given that everything looks like a quad in the frametype tab.
Look at _Telemetry module_ section below.

**Compass**: I tried doing the ArduPilot compass calibration but the green bar kept reaching its max before just resetting to 0. I think the issue is as described [here](https://discuss.ardupilot.org/t/compass-calibration-never-completes/66085/6), i.e. it won't work if the gyro and accelerometer aren't reporting data that coincides with the movements of the compass. I.e. both must be mounted on a common platform  before it'll work.

The compass really does have to be disabled if you haven't calibrated it for motor test to work.

So, I think you really do need everything setup on a big piece of card - with telem module and battery so you can move it all round.

This is essentially what Painless360 says at the 12m 42s mark as he starts the proces [here](https://www.youtube.com/watch?v=_ketmb8u2UI&list=PLYsWjANuAm4rXSCRfiZkpuBmUP0u-lLby) but I wasn't paying attention.

**Note:** always remember to turn on the ESC - I've been looking at the setup, the FC's all lit up etc. but the motors don't work because the ESC isn't on.

The Foxeer GPS has no arrow printed on it to point to the front - I think you just have to assume the connector is at the back. Cf with Matek M10Q-5883 that has a small arrow on its front edge:

<https://cdn-v2.getfpv.com/media/catalog/product/cache/3979b3fd908fbb12b31974edb6316b2e/m/a/mateksys-m10q-5883-gnss-_-compass_1.jpg>

**Update:** the _specifications_ tab on the Foxeer product page for the GPS states:

> Compass Orientation: Plug facing direction of flight and obviously antenna up

So, the opposite of what I assumed!

LEDs:

* red flickers when powered - it never goes solid.
* green is solid initially and starts flickering once it's achieved some level (unspecific) of position lock.

Telemetry module
----------------

Don't forget TODO above.

UART3 seems to be the only completely free one: <https://github.com/ArduPilot/ardupilot/blob/2bef8f2/libraries/AP_HAL_ChibiOS/hwdef/speedybeef4v4/hwdef.dat#L70>

I don't why it's labelled CAM it its `hwdef` [README](https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_HAL_ChibiOS/hwdef/speedybeef4v4)

Googling didn't get me anywhere - CAM seems to be camera, e.g. the the `CAM_xyz` [camera parameters](https://ardupilot.org/copter/docs/parameters.html#cam-parameters).

But the only camera related functionality that involves a UART seems to be related to a RunCam specific protocol covered [here](https://ardupilot.org/plane/docs/common-camera-runcam.html).

**Update:** "CAM" I think isn't actually an ArduPilot reference, I think instead it's referring to the fact that the block of pins that includes SERIAL3 is marked as CAM on the FC as shown here:

<https://store-fhxxhuiq8q.mybigcommerce.com/product_images/img_SpeedyBee_F405_V4_Stack/SB_F405V4-Other-7.jpg>

As shown in the SpeedyBee [wiring diagram](https://store-fhxxhuiq8q.mybigcommerce.com/product_images/img_SpeedyBee_F405_V4_Stack/SB_F405V4-Other-2.jpg), it's meant for an analog camera.

So, in this block, you've got:

```
5V |  G
---+---
R3 | T3
```

It'll be a pain in the ass to solder that as the pins aren't even offset like on the opposite side.

_Maybe_ it's possible to solder diagonally onto pins:

```
  | |   | |
+-|-|-+-|-|-+
| | | | | | |
| \ | | \ | |
|   | |   | |
+---|-+---|-+
|   | |   | |
|  /  |  /  |
|     |     |
+-----+-----+
```

Anyway, even it the `hwdef` README, their example of taking a UART for FrSky Telemetry uses SERIAL3.

So, I think you want:

```
SERIAL3_PROTOCOL 2 // MAVLink2
```

There's also `SERIAL3_OPTIONS`, `SERIAL3_BAUD`, these may have to be set too.

E.g. in the `hwdef.dat` for the QioTek Zealot F427, you can see:

```
# USART2 for Mavlink2 wifi module set baudrate to 921600
...
define DEFAULT_SERIAL2_PROTOCOL SerialProtocol_MAVLink2
define DEFAULT_SERIAL2_BAUD 921600
```

**Updates:**

* `SERIAL3_PROTOCOL` was none by default, changed to Mavlink2.
* `SERIAL3_BAUD` was 38400 by default, changed to 57600 as this is the rate specified [here](https://ardupilot.org/copter/docs/common-configuring-a-telemetry-radio-using-mission-planner.html)) for the Mission Planner radio connected to your PC/laptop. I later tried increasing to higher rates but even 115,200 didn't work.
* Pressed _Write Params_.
* Once, I'd set the parameters, I thought I'd be able to at least read the settings from radio (see below) with the FC still connected by USB. But to get any further, you have to disconnect the FC and connect the other radio by USB. I powered the FC via a USB charger and its radio and the one plugged into my laptop connected to each immediately without any action on my part (green LED went solid - see [here](https://docs.holybro.com/radio/sik-telemetry-radio-v3/led-and-connection) for how to interpret LEDs).
* The Holybro SiK radio uses a FTDI FT231X UART-to-USB chip which (surprisingly) surprisingly isn't a pre-installed driver on Windows 11. The driver can be found [here](https://ftdichip.com/drivers/vcp-drivers/). Initially, I downloaded and installed the _setup executable_ linked to on the row for _Windows (Desktop)_ - this installed without issue but didn't work. So, still on the _Windows (Desktop)_ row, I downloaded the `.zip` file linked to in the ARM column. I extracted that, opened _Device Manager_, found _FT231X USB UART_ under _Other devices_, double-clicked it, clicked _Update Driver_, select _Browse my computer for drivers_ and selected the extract folder. Oddly, this didn't quite work either, it then showed up in _Other devices_ with a new name (just "USB UART Device" _I think_) and I double-clicked it again and this time selected the root extracted folder (previously, I'd navigated down to to the `ARM64\\Release` subfolder. Whether things just needed to done twice for some reason or selecting the root folder was the issue, I don't know. Anyway it worked then and showed up as a COM port.
* As Sparkfun use this FTDI chip, they have an easy to follow guide [here](https://learn.sparkfun.com/tutorials/how-to-install-ftdi-drivers/all) that covers intalling the driver on all platforms. I suspect if you're not on an ARM VM, the standard _setup executable_ will work fine.
* Go to _Setup / Optional Hardware / Sik Radio_. I tried the _Load Settings_ button but kept getting _Failed to enter command mode_ - it turns out that this only works if Mission Planner is **not** already connected to the radio. Once that was resolved, it did load (it takes quite a few seconds of apparently doing nothing) and showed the details for both the local and remote radio. And showed that they both had firmware version "RFD SiK 2.0 on HM-TRP". I tried the _Upload Firmware (Local)_, it just immediately tried to upload firmware and completed but the radio entered a bricked mode (the red LED stayed solid which means its still in firmware update mode). I could unbrick it by running QGroundControl, going to the _Firmware_ section and unplugging the radio and reconnecting it - on reconnect QGroundControl automatically updated its firmware (and this time, the LEDs went back to normal). The process was all pointless as the latest firmware version is 2.0 (where the firmware comes from - the [SiK repo](https://github.com/ArduPilot/SiK) is clearly under moderately active development but hasn't published a release there since version 1.9 in early 2014).
* Loading parameters when connecting is very slow - I've had it hang during this phase, just clicking _Cancel_ and connecting again seems to work.
* Note: using the supplied micro USB cable (with red connector at one end) with the supplied micro-USB to USB-C adapter didn't work for connecting the radio to the laptop (the radio showed no sign of having power). It turns out this is an OTG cable so it's meant for connecting to ground control s/w running on a phone or tablet. I tried this but same result (no power). I tried a different cable and Android recognised the device and offered to connect it to the SpeedyBee Betaflight app that I already had installed. I looked for Android ground control apps but it seems [Tower](https://github.com/DroidPlanner/Tower) hasn't been updated for 7 years, the version of QGroundControl (last released in 2021) on the Google Play store is too old for my device (tho' there seem to regular updates to the [Android section](https://github.com/mavlink/qgroundcontrol/tree/master/android) of the GitHub repo and they release APKs here [releases](https://github.com/mavlink/QGroundControl/releases) so these might work). Mission Planner for Android would install on my phone and when I plugged in the radio, Android correctly suggested connecting it through to Mission Planner but Mission Planner failed to see it when I pressed _Connect_.

See also <https://github.com/ArduPilot/ardupilot/blob/master/libraries/AP_SerialManager/AP_SerialManager.cpp>

**Note:** baud rate when entered as a parameter has to be one of these values: <https://ardupilot.org/copter/docs/parameters.html#serial3-baud-serial-3-gps-baud-rate>

E.g. 57 is 57600.

See what baud rate <https://github.com/DroneBridge/ESP32> configures by default - in the README, one sees an image with 57600 and in another a setting with 115200.

If mavlink doesn't look like it's working at all, see if it's an enabled feature (see elsewhere) for the SpeedyBee F405 V4 and compare with the features of the QioTek Zealot F427 (which presumable has mavlink enabled if a UART is specified to use it).

For SiK telemery in Mission Planner see <https://ardupilot.org/copter/docs/common-configuring-a-telemetry-radio-using-mission-planner.html> - I wonder if https://github.com/DroneBridge/ESP32 supports the _Load Settings_ button.

ESC 6v power distribution
-------------------------

A 2x3 piece of pin header.

Use stranded wire as it'll wick up solder and tin the pins, and solder the wire across the outside edges of the two rows.

Remember, it's a **6V** supply so, no one else will want this power other that:

1. ESC
2. Steeting servo
3. Lights
3. Fan 1
4. Fan 2 (optional)

If you look at the RX in the car, this is how its 4 outputs are labelled. The lights seem very secondary at the moment and fan 2 is unlikely - but still go for at least 4x2.

Lessons:

* Holding the wire in-place as you apply the soldering iron tip at the points where it touches the pins isn't easy.
* Initially, I held the header in a vice but the pins heated up the plastic of the header so much that they started to waggle about.
* So, I switched to doing it with the header inserted into a breadboard - this worked well.
* The little solder points that formed at the end of the pins were so sharp it was painful pushing on them when inserting servo plugs onto other side.
* In the end, I put the header back into a breadboard and "sanded" the pins on a piece of cardboard to remove these sharp points.

FlySky G7P
----------

We really don't need any of the smart features of the G7P - all the intelligence in our setup is in the FC.

However, I can't own something without trying to understand all its features.

The G7P is typically sold with a choice of 7 channel RX:

* FS-R7P - base model.
* FS-R7V - in-built gyro.
* FS-R7D - light controller (i.e. wire up headlights etc.).

I bought it with the FS-R7P RX - this is the cheapest standard 7 channel RX (and perfect for our setup as we actively don't want a gyro in the RX working against the gyro on the FC and light control is really just a fun feature).

It turns out that the FS-R7P etc. can be set to output S.BUS/i-BUS (which is clear from its manual but wasn't clear to me from the FlySky product page).

So, the FS-R7P will work perfectly with out FC directly. However, as we don't need any of its PWM outputs we could use an RX like the [FS-SRM](https://www.flysky-cn.com/srmspecifications) that comes without all those PWM pins.

Note: BVD (being able to see the LiPo voltage on the TX) is a nice feature of the FS-R7P and similar RXes but as the FC also sees the battery voltage its not that valuable (like having a gyro in the RX, it's one of those features that's nice to have in a setup where the vehicle itself is dumb, i.e. has no FC).

There are many YouTube reviews of the G7P but I suggest these two as they also include good overviews to get you started using the TX:

* RC Review's [Flysky G7P Review - better than the Flysky GT5?](https://www.youtube.com/watch?v=otPYzx7fU7I).
* RC Escape's [FlySky FS-G7P 2.4GHz 7CH ANT Protocol Radio Transmitter](https://www.youtube.com/watch?v=aDoT6LgR_tk).

They seem to have resolved all issues that I noticed being mentioned in the various review videos, e.g. my one came with a foam steering wheel and the firmware has been updated several times to add or improve features that people commented on. My TX came with the latest firmware available at the time (1.0.30 release mid 2023).

In addition to the reviews above, the channel _WTF RC Cars_ has a whole series of short how-to videos covering the G7P and the RXes that can be used with it. Ones I found useful include:

* [Set up the auxiliary channels](https://www.youtube.com/watch?v=xv5r0Fgbizc) - associate the knobs and switches on the TX with particular channels.
* [Replace the timer on the main screen with BVD and signal strength](https://www.youtube.com/watch?v=VRon1zvNHyM) - replace the huge but largely pointless 00:00.00 timer display with more useful values.
* [Set up failsafe](https://www.youtube.com/watch?v=H1RJCjKV8bE) - set up what the RX does if it looses connection with the TX.
* [FS-R7P BVD setup and binding](https://www.youtube.com/watch?v=Zuz7hNoOgVw) - at the 7m 52s mark, he covers the bind process (which is actually trivial - also note, you can just leave the _Frequency_ as _Analog_).

You can find the [G7P manual](https://www.flysky-cn.com/g7pdownloads) on the FlySky and also the manual for the [FS-R7P RX](https://www.flysky-cn.com/r7p-manual-1-1-1) and they're actually quite good.

Header and jumper wires
-----------------------

I mainly used pre-crimped jumper wires like these [15cm red ones](https://www.pololu.com/product/1722) from Pololu (I think it's a shame they don't sell multi-colored assortments in lengths greater than 5cm).

Many companies sell multi-colored assortments, e.g. [here](https://www.mikroe.com/wire-jumpers-male-to-female-15cm-10pcs) from Mikroe (in Europe, I bought these from [TME](https://www.tme.eu/)).

Note: make sure to get the ones with square plastic connectors (called Dupont connections) with square pins - some jumper wires come rounds connectors and pins.

Note: both the Pololu and Mikroe wires are plastic coated. For breadboarding the stiffness of plastic is a positive but when wiring things up in space-constrained setups, silicone coated wires are generally preferable. Generally, you make up your own length silicone wires so, I didn't find much in the way of pre-made jumper wires using silicone but there are [these ones](https://www.aliexpress.com/item/1005003208833622.html) from WeAct.

To connect the 6V positive and negative output of the ESC to the motor fan and servo, I two row header (generally sold in 2x40 strips) like these [ones](https://www.pololu.com/product/966) from Pololu.

Similar items on AliExpress:

* [Kailanda store](https://www.aliexpress.com/item/1005005691532643.html) (the 2.54mm 2x40 L11.5mm ones).
* [Ky Win Robot store](https://www.aliexpress.com/item/32848276499.html)

Solderless connectors
---------------------

Connecting wires without the soldering step by using heatshrink tubing with a builtin ring of low-temperature (140C) solder at the middle sounds interesting.

This is product that was originally marketed as SolderSeal&tm; and I came across them recommend [here](https://www.youtube.com/watch?v=vDsVwbWiVFI) by Adam Savage (when he uses them, he doesn't even bother twisting the wire ends together).

Two keys things seem to be:

* The solder does not really wick into the strands as it would with when using a soldering iron - despite that it, it creates a connection that has nearly the same resistence and strength.
* It requires a hotair gun that can produce at least 150C. Despite claims of 200C, many cheap hotair guns intended purely for heatshrink (e.g. something like [this](https://cdn-v2.getfpv.com/media/catalog/product/cache/b4872d6d0ceb3d2181c291dd3ccc7b81/1/1/110v-300w-portable-mini-heat-gun-tool---hot-air-gun-5_2.jpg)) won't melt the solder.

I have this [hotair gun](https://hobbyking.com/en_us/dual-power-heat-gun-750w-1500w-output-230v-50hz-version.html) from Hobbyking which seems to be hot enough. Unfortunately, they've discontinued it and I couldn't find a particularly convincing branded product on AliExpress. Rather pricey alternatives (for around US$50) include:

* Steinel HL 1821S
* Atten AT-A2231

Pricier still (around US$60):

* Makita HG5030K
* Bosch Easy Heat 500

Warning: many cheap heat guns, e.g. the Black&Decker HG1300 at US$20, are meant for stripping paint and have a minimum temperature of 400C which is too hot.

There are lots of videos on YouTube saying that these products are simply junk, e.g. this [one](https://www.youtube.com/watch?v=kzDjy3Fv_K4) from DoItYourselfDad is typical. However, in this [follow-up video](https://www.youtube.com/watch?v=Janu2I8ofyY), he essentially says that it's easy to use them incorrectly but if done correctly they actually work very well.

DoItYourselfDad says the product was originally developed by an Irish company, if so there's no sign of them any more and the trademark now seems to be held by Master and there current version of the product (see [here](https://www.masterappliance.com/solderseal-butt-splice-connector-jar-lead-free/)) doesn't seem to feature the waterproof seals that most other versions do (not that that's essential for most uses).

There are no end of knock-offs on AliExpress, generally sold by stores that just seem to have popped up yesterday. After a lot of searching, I bought them [here](https://www.aliexpress.com/item/1005002524941643.html) from Lincoiah - Lincoiah looks like a real manufacturer and is probably the original source for the products it's selling (and the AliExpress is registered to the real Lincoiah company).

Mission Planner via serial
--------------------------

It is possible for Mission Planner, running in a Windows VM, to connect directly to the FC via the telemetry serial port (as QGC, running on the Mac, can).

I used an Adafruit [CP2102N USB-to-serial converter](https://www.adafruit.com/product/5335) (as Prolific deliberately bricked my old converter so it can't work on Windows 11).

The CP2102N [driver](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads) is a little odd - it doesn't come with an installer. Instead, I unpacked it, opened _Device Manager_, found the device under _Other devices_, right clicked it, selected _Properties_, clicked _Update Driver_ and pointed it at the root folder of the unpacked `.zip` file.

**Update:** apparently, I could have skipped downloading the driver and in _Update Driver_, just select _Search automatically for drivers_ and it should have found things itself.

But Mission Planner still couldn't connect - it'd just fail with:

```
COM6 System.IO.IOException: A device which does not exist was specified.

    at System.IO.Ports.InternalResources.WinIOError(Int32 errorCode, String str)
    ...
```

It seems the Windows serial setup is none too sophisticated - you have to open the device again in _Device Manager_, go to the _Port Settings_ tab and change the _Bits per second_ from the 9600 value to the 57600, i.e. the same value you selected in the Mission Planner dropdown (and as previously configured for the relevant serial port in ArduPilot). And even then, the change didn't really seem to take effect (I still got the same `A device which does not exist` error) until I rebooted the VM.

But then everything did work fine.
