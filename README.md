README
======

---

I was looking for some three-way splitter to split off power from the battery cabling to the Pi or Nano SBC to achieve something like the Holybro PM02:

<https://holybro.com/collections/power-modules-pdbs/products/pm02-v3-12s-power-module>

Note: this outputs 3.2A at 5.2V - way too little for what I want.

But I think the end the simplest is a screw terminal block like this:

<https://uk.rs-online.com/web/p/standard-terminal-blocks/8407951>

Note: 36A seems to be the highest current these things are rated for.

Connect one deans pigtail to one side and twist together the ends of the other deans pigtail with the thinner wires off to power the SBC and connect them in the other side.

Or even simpler:

* Cut the deans connector off the end of the car's battery cable.
* Tin the ends of those cables and the thiner cables you're going to run to the SBC setup.
* Or see if you can twist the wires together before tinning - this'd mean they'd be less likely to separate later.
* Join the wires so, the SBD wires run back along the battery cables rather than extending away from them.
* Then solder these combined wires onto a fresh deans connector - this'd work much nicer with an XT60, where (with the thinner cable beneath) you can "mash" both into the XT60 cup-like connectors. With deans, the connector is just a flat surface rather than a cup.

---

The Pololu 5V 5.5A step-down voltage regulator - is fairly pricey at US$25 <https://www.pololu.com/product/4091>

5.5A seems to be as high as Pololu go for 5V regulators and this seems to be about the most you want for a Pi 5 with high-power peripherals.

Note: I have a similar-ish discontinued variant of this somewhere: <https://www.pololu.com/product/2865>

Actually, you can get 9A (but with hard to source components): <https://www.pololu.com/product/2866> and even 15A but at a pricey US$80: <https://www.pololu.com/product/2881>

Raspberry Pi 5 power limiting - the Pi 5 will, by default, provide _less_ power via USB as it needs more itself.

If you "wish to drive high-power peripheral, [you need a] USB-C power adapter which supports a 5V, 5A (25W) operating mode. If the Raspberry Pi 5 firmware detects this supply, it increases the USB current limit to 1.6A, providing 5W of extra power for downstream USB devices".

So, if using a supply that doesn't have USB-C's ability to signal this ability, I _guess_ you have to use "the option to override the current limit".

---

Question: is using an SD card rather than an SSD or an eMMC module on a Pi be an issue - this video <https://www.youtube.com/watch?v=Bf7kSNWbcrU> mentions that the slowness of the SD card may be relevant.

---

I pre-ordered an 8GB Raspberry Pi 5 from <https://shop.pimoroni.com/>

And registered for a restock update from Reichelt.

Note: Ubuntu does seem to yet have an LTS that supports the Pi 5 - on their [Raspberry Pi page](https://ubuntu.com/download/raspberry-pi), they just list Ubuntu 23.10 as being ready for the Pi 5.

---

This guy made an interesting start on a ROS based self-driving RC car: <https://www.youtube.com/watch?v=Bf7kSNWbcrU>

Unfortunately, he never got around to the later chapters.

He's using stuff from the MIT Racecar project: <https://mit-racecar.github.io/hardware/>

Including VESC - an open source ESC that can provide tachometer/odometry data - I wonder if [BLHeli_32](https://github.com/bitdump/BLHeli/tree/master/BLHeli_32%20ARM) can do something similar?

BLHeli_32 certainly provides RPM telemetry data which sounds similar.

---

Super ROS 2 intro: <https://www.youtube.com/playlist?list=PLunhqkrRNRhYAffV8JDiFOatQXuU-NnxT>

---

ROS 1 had rosserial. Tiziano Fiorenzani shows how to use it to add your classic RC controller between your ROS <https://www.youtube.com/watch?v=WLVfZXxpHYI>

Tiziano Fiorenzani shows how to use it to add an Arduino as an intermediary between your ROS capable Pi (or whatever) and the steering and throttle controls so, that the Arduino can take inputs from either the Pi or the RX bound to your RC controller.

To be honest, I can't see why he didn't connect the RX straigh to the Pi and then work out how to publish its PWN values such that ROS could consume it (in the same way it consumes the joypad or keyboard inputs).

Anyway, rosserial isn't available for ROS 2. It's equivalent is microROS which can't be used with anything as resource constrained as a classic Arduino but can e.g. be used with the incredibly cheap Raspberry Pi Pico (which outperforms a Teensy LC by far in RAM and flash but has less RAM than a Teensy 4).

<https://micro.ros.org/docs/overview/hardware/>

But anyway, as noted, I suspect _rosserial_ nor _microROS_ are tha appropriate solution to Tiziano's problem - and that one should look as ros_control, see Articulated Robotics' videos:

* <https://www.youtube.com/watch?v=J02jEKawE5U>
* <https://youtu.be/4QKsDf1c4hc?si=Ep0f2IU5iqf8NCxt>

---

Setup:

* Brushed motor
* Servo
* ESC
* FC
* TX
* RX
* Regulator - see Pololu above.

I suspect, you can work out if V4 Speedybee needs changes in ArduCopter relative to V3 by comparing Betaflight configs:

* <https://github.com/betaflight/unified-targets/blob/master/configs/default/SPBE-SPEEDYBEEF405V3.config>
* <https://github.com/betaflight/unified-targets/blob/master/configs/default/SPBE-SPEEDYBEEF405V4.config>

Actually, there seem to be lots of changes.

ArduCopter: <https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_HAL_ChibiOS/hwdef/speedybeef4v3>

ArduCopter [Speedy Bee F4 V3 reference page](https://ardupilot.org/copter/docs/common-speedybeef4-v3.html).

See, also:

* <https://github.com/iNavFlight/inav/tree/master/src/main/target/SPEEDYBEEF405V3>
* <https://github.com/iNavFlight/inav/tree/master/src/main/target/SPEEDYBEEF405V4>

JB has a great video <https://www.youtube.com/watch?v=L-6r2iX1p6s> on servos with BF so maybe:

* Get things working with BF
* Then ArduCopter
* Then Articulated's ROS series
* Then Donkey Car

MJX parts
---------

The MJX 16208 has a shell that's held on with a flip-up-catch mechanism while the 16209 has one held on with the usual clips.

Oddly, the MJX site nor the page for the [16209](http://www.mjxrc.net/goodshow/16209-1-16209.html) has a downloadable PDF manual.

There are manuals in Chinese on their Chinese language site and the English manual does exist, e.g. you can find it [here](https://www.hobbiesaustralia.com.au/mjx-1-16-hyper-go-4wd-off-road-brushless-2s-rc-mon~29032) on the Hobbies Australia site.

And the Anwei page for the [16209](https://amewi.com/Hyper-GO-Monstertruck-brushless-4WD-1-16-RTR-blaurot) does have the manual in [German and English](https://amewi.com/downloads/manuals/22627_22628_22629_DE_EN.pdf)

Note: some of the part numbers seem to have been updated since the manuals came out - e.g. the motor is shown as B284B but the spare is sold as B284C.

The manual shows all the parts numbers along with diagrams showing how to assemble everything.

Parts:

Body clips: M001
Oil-filled shocks: 16500R
Steering Linkage: 16431
Wheel Assembly: 16300B
F/R Body Pillars: 16281
Bolts for body pillars: M2684
Truggy tires: 16300C

Tool for steering linkage

MJX parts from AliExpress
-------------------------

* [Wheels to motors](https://www.aliexpress.com/item/1005005090477708.html) from Wellsold.
* [Bolts and servo horns](https://www.aliexpress.com/item/1005005232464912.html) from Wellsold.
* [Chassis to motors](https://www.aliexpress.com/item/1005005228713841.html) from Cool Play Hobby Toy Accessories.
* [Wheels to structural parts](https://www.aliexpress.com/item/1005005144149179.html) from Cool Play Hobby Toy Accessories.
* [Batteries](https://www.aliexpress.com/item/1005005049009279.html) from Cool Play Hobby Toy Accessories.
* [Motors, bearings and clips](https://www.aliexpress.com/item/1005004679687294.html) from JM Toy & Hobby store.
* [Bolts, nuts and clips](https://www.aliexpress.com/item/1005005531160906.html) from Have Fun RC Toy store.
* [More bolts etc.](https://www.aliexpress.com/i/4000097715173.html) from Have Fun RC Toy store.

In the end I bought most things from Wellsold and clips and bolts from Have Fun RC Toy store. In retrospect it would have cost much the same to buy a second car and use it for parts.

Other suppliers
---------------

Serious-RC are a UK based company that seem to sell primarily on eBay, they seem to have pretty much every MJX part going (plus cars and parts for MJX and many other brands).

* [Serious-RC on eBay](https://www.ebay.co.uk/str/seriousrc)
* [Serious-RC website](https://www.seriousrc.co.uk/)

The markup is noticeable compared with ordering from AliExpress but shipping times for the EU are _presumably_ lower as is _presumably_ the risk of getting fake parts.

Banggood also carry some MJX [162xx parts](https://uk.banggood.com/search/16208/0-0-0-1-4-60-0-price-0-0_p-1.html).

Mavros
------

For communication between the ROS world and a FC use [mavros](https://github.com/mavlink/mavros) - this consists of four packages, the main ones being [mavros](https://index.ros.org/p/mavros/github-mavlink-mavros/#humble-overview) (which pulls in mavros_msgs and libmavconn) and [mavros_extras](https://index.ros.org/p/mavros_extras/github-mavlink-mavros/#humble-overview) (which pulls in mavros and its dependency).

ArduPilot has a whole [ROS/ROS2 section](https://ardupilot.org/dev/docs/ros.html).

And the blog has a [Visual Navigation on the cheap](https://discuss.ardupilot.org/t/visual-navigation-on-the-cheap/91700) post that covers using a Kakute F4 FC (using its PWM1 to 4 pins to drive two [Pololu DRV8838 brushed motor drivers](https://www.pololu.com/product/2990) rather than a 4-in-1 ESC) to control a two-wheeled bot with a camera wired into a Pi for visual odometry (which involves ROS as described in the [ArduPilot VIO docs](https://ardupilot.org/dev/docs/ros-vio-tracking-camera.html) - the docs talk about cameras like the Realsense range but the blog uses a cheap ArduCam camera).

ArduPilot rovers with drone FCs
-------------------------------

The ArduPilot blog post mentioned above ([Visual Navigation on the cheap](https://discuss.ardupilot.org/t/visual-navigation-on-the-cheap/91700)) uses a Kakute F4 to control a two wheel rover.

That post is from 2022. The same developer also did a [ArduRover with the Pololu Romi](https://discuss.ardupilot.org/t/ardurover-with-the-pololu-romi/41991/1) blog post back in 2019.

This describes a similar setup (tho' the motor drivers and frame are different) but simpler - it's just the basic rover without any companion computer.

### ArduRover reference frames

The ArduPilot site has two RC cars as reference frames:

* The [Thunder Tiger Toyota Hilux](https://ardupilot.org/rover/docs/reference-frames-tt-toyotahilux.html)
* The [Traxxas Stampede 4WD truck](https://ardupilot.org/rover/docs/reference-frame-traxxas-stampede.html)

The Toyota Hilux page includes a link to its ArduPilot [`.param`](https://github.com/ArduPilot/ardupilot/blob/master/Tools/Frame_params/ThunderTiger-ToyotaHilux-Rover.param) file that's kept maitained in the main ArduPilot GitHub repo.

The Traxxas Stampede page shows how two of the servos of the Pixhawk are wired thru to the servo and the ESC (along with the rest of the wiring).

The Toyota Hilux also uses an ESP8266 for MAV telemetry but see below for the ESP32 alternative.

ESP32 MAV telemetry
-------------------

Traditionally, Holybro [SiK telemetry radios](https://holybro.com/products/sik-telemetry-radio-v3) have been used for a wireless connection between laptop and drone/rover.

But an interesting alternative (especially given the shorter distances typical when using a rover rather than a drone) is an ESP32.

See the ArduPilot documentation [here](https://ardupilot.org/rover/docs/common-esp32-telemetry.html) and the GitHub [DroneBridge/ESP32](https://github.com/DroneBridge/ESP32) project repo.

ESP32 boards:

* [WeAct ESP32-DOWD-V3](https://www.aliexpress.com/item/1005005645111663.html) - US$3
* [LILYGO TTGO T7](https://www.aliexpress.com/item/32846710180.html) - US$5.50

The above are proper ESP32s. Both WeAct and LILYGO also have S3 boards and other variants, e.g. here is [WeAct S3 board](https://www.aliexpress.com/item/1005005592730189.html) and a [LILYGO S3 board](https://www.aliexpress.com/item/1005004777561826.html).

However, if you use an S2 etc., you'll have to compile the firmware yourself, the DroneBridge/ESP32 only releases ready compiled firmware for the ESP32.

Adafruit have some nice tiny boards:

* [QT Py ESP32-S3](https://www.adafruit.com/product/5426) - US$12.50
* [TinyS3 ESP32-S3 with u.FL](https://www.adafruit.com/product/5747) - US$20

The TinyS3 is interesting not just because of its size but also because one could attach a u.FL antenna for improved range.

The SparkFun [Thing Plus - ESP32](https://www.sparkfun.com/products/20168) at $US25 seems hard to justify vs e.g. the WeAct board.

For a comparison of ESP32 MCUs, see this [table](https://gist.github.com/fabianoriccardi/cbb474c94a8659209e61e3194b20eb61) - the S2 and S3 are still Tensilica Xtensa 32 chips but the C3 and C6 are RISC-V.

Flight controller
-----------------

SpeedyBee [F405 V4](https://www.speedybee.com/speedybee-f405-v4-bls-55a-30x30-fc-esc-stack/).

Note: as shown above Betaflight and iNav support the V4, while ArduPilot only currently has support for the V3. The V3 is still available but according to reviews of the V4, it corrects several noticeable issues with the V3.

SpeedyBee [F405 V4](https://www.unmannedtechshop.co.uk/product/speedybee-f405-v4-flight-controller/) from Unmanned Tech.

ESC
---

The MJX ESC is 45A - it would be interesting to use a similar amp BLHeli_32 capable of bi-directional DSHOT and ESC telemetry.

**Important:** according to [OL's page](https://oscarliang.com/esc-telemetry-betaflight/), there's actually better RPM information included in the DSHOT protocol than in the ESC telemetry data - but better only in the sense that the DSHOT data is much more high frequency.

Holybro BLHeli_32 [Tekko32 F4 45A ESC](https://holybro.com/products/tekko32-f4-45a-esc)

[Tekko32 F4 45A ESC](https://www.3dxr.co.uk/multirotor-c3/multirotor-escs-c48/holybro-tekko32-f4-45a-esc-p4993) from 3DXR.

A similar 45A Lumenier model is the [Razor Pro F3 45A ESC](https://www.getfpv.com/electronics/electronic-speed-controllers-esc/single-esc/lumenier-razor-pro-f3-blheli-32-45a-2-6s-esc.html).

Note that the Holybro is an F4 and the Lumenier is a cheaper F3.

Transmitters and receivers
--------------------------

In the drone world, there's always a flight controller (FC) between the receiver (RX) and everything else.

So, the RX talks a digital protocol to the RC and doesn't have the multiple [PWM](https://oscarliang.com/rc-protocols/#PWM-Pulse-Width-Modulation) outputs that RC car RXs have.

On an RC car the RX's PWM outputs directly control the steering servo and the motor's ESC. There's no smart FC involved.

So, given that they seem much simpler, one might assume that RC car TXs and RXs would be much cheaper than those in the drone world.

But the opposite seems to be true.

In the drone world, the most popular RX protocol - [ExpressLRS](https://www.expresslrs.org/) - and the most popular TX firmware - [EdgeTX](https://edgetx.org/) - are open source and manufacturers compete to provide interoperable hardware.

In the RC car world, each manufacturer seems to have their own proprietart (and largely undocumented) protocols. If you want to switch to a TX from a different manufacturer then you'll also have to switch the RXs in all your cars to ones from that manufacturer.

In the drone world, the terms RX and TX are historical as the interaction is two way - however, it's still common in the RC car world that the communication is one-way and that e.g. the TX doesn't know that any RX is listening to it (it just sends signals out into the void and hopes something is listening). E.g. it's only in 2022 that FlySky introduced their ANT protocol where the communication between TX and RX is two way.

But despite things seeming much simpler, you seem to get much better value-for-money in the drone world, US$140 buys you a great [RadioMaster Boxer](https://www.radiomasterrc.com/products/boxer-radio-controller-m2) 16 channel TX while the same money buys an altogether more basic 3 channel [Futaba 3PV](https://futabausa.com/product/3pv/).

The comparison is a bit unfair as Futaba also produce vastly over priced products for the drone market - but no hobbyist actually buys them whereas in the RC car world, the Futaba 3PV seems to be a fairly typical model.

It seems only fairly recently that cheaper Chinese manufacturers have started making in-roads in this world, e.g.:

* [Flysky GT5](https://www.flysky-cn.com/gt5-canshu) (296g)
* [RadioLink RC6GS](https://www.radiolink.com/rc6gsv3) (319g)

RC Review's [Flysky GT5 vs. Radiolink RC6GS video](https://www.youtube.com/watch?v=8WxZb6vLdYI)

i-BUS/S.BUS capable GT5 compatible RXs:

* [X8B](https://www.flysky-cn.com/x8b-canshu) - 8 channels - pure digital.
* [X6B](https://www.flysky-cn.com/x6b-canshu) - 6 channels - digtal plus six PWM outputs.

While the GT5 only supports 6 channels, I'm inclined towards the X8B as it doesn't have the large PWM connector.

AFHDS 2A clearly does support reporting telemetry back to the transmitters, as is clear from the README for the [GitHub FlySkyRxFirmwareRssiMod repo](https://github.com/Cleric-K/FlySkyRxFirmwareRssiMod). It mods binary dumps of the original firmware to include RSSI in the information forwarded to the FC but makes clear RSSI is already communicated by default to the TX. However, I can't find anything that indicates that the GT5 can display this information (or is in anyway aware of the RX that its bound to).

Flysky aren't great at making the RX firmware available - however, they are available from the [GitHub FlySkyRxFirmware repo](https://github.com/povlhp/FlySkyRxFirmware) - most of the images have simply been extracted from RXs, including those for the X8B and X6B. I assume these images are the basis for the images that are modded by the FlySkyRxFirmwareRssiMod project.

TX and RX on AliExpress:

* [GT5 from RC Fun City store](https://www.aliexpress.com/item/1005005773630207.html) - US$58 plus US$11 shipping from EU wareshouse (or US$4.50 for shipping from China).
* [X8B from U-Angel-1988 store](https://www.aliexpress.com/item/32892188833.html) - US$17 plus US$2 shipping. Or from [RC Fun City store](https://www.aliexpress.com/item/4000169189998.html).

Note: Flysky also have the [G7P](https://www.flysky-cn.com/g7pdescription) (305g) with a nicer LCD and using their new ANT protocol that supports telemetry. However, so far they've only brought out one pure digital RX with S.BUX - the [SRM](https://www.flysky-cn.com/srmspecifications). And it looks quite bulky - altough the weight, at about 305g, is about the same. 

RC Review's [Flysky G7P review](https://www.youtube.com/watch?v=otPYzx7fU7I).

G7P on AliExpress:

* [Hundred Percent store](https://www.aliexpress.com/item/1005004371293939.html)
* [RC HobbyFly store](https://www.aliexpress.com/item/1005005210741036.html)
* [Dragon Model store](https://www.aliexpress.com/item/1005004018517454.html)

RadioMaster are actually about to launch an EdgeTX based TX (that can work with any existing ExpressLRS RX) for RC cars - the [MT12](https://www.radiomasterrc.com/products/mt12-surface-radio-controller) (480g).

Painless360 [RadioMaster MT12 review](https://www.youtube.com/watch?v=9k5FQxx34E0).

Remember: the screen and two-way comms isn't that big a deal if you're looking at all the data and more anyway via goggles.

My alternative choice to the Flysky GT5 would be the [RadioLink RC6GS v3](https://www.radiolink.com/rc6gsv3).

The big plus vs the GT5 is that it has telemetry, i.e. the TX can display the RSSI and battery voltage reported back from the RX.

They have a reasonable number of pure digital (i.e. no PWM outputs) 8-channel RXs with S.BUS:

* [R8XM](https://www.radiolink.com/r8xm) - with telemetry support (just connect the batteries balance lead directly to the RX).
* [R8FM](https://www.radiolink.com/r8fm) - smaller, no telemetry.
* [R8SM](https://www.radiolink.com/r8sm) - even smaller, no telemetry.

I like the substantial looking switches on the RC6GS, but in head-to-head videos like RC Review's [Flysky GT5 vs. Radiolink RC6GS video](https://www.youtube.com/watch?v=8WxZb6vLdYI), it looks rather bulky compared to the GT5 and the build quality seems to be slightly lower. But RC Review's is also very positive about it in his newer [RC6GS v3 video](https://www.youtube.com/watch?v=NYXfHBnTHkc).

On AliExpress:

* [RC6GS v3 at Hundred Percent store](https://www.aliexpress.com/item/4000615916643.html) - no RX version is about US$57 (plus US$6 shipping).
* [RC6GS v3 at BYRC store](https://www.aliexpress.com/item/1005002728220551.html) - no RX version is about US$50 (plus US$16 shipping).

### Multiprotocol modules

If you've got a drone/winged TX running EdgeTX then it can probably take a protocol module.

There's an open source project that's called [MULTI-Module](https://www.multi-module.org/) that supports about [70 protocols](https://www.multi-module.org/basics/supported-protocols) on 4in1 modules (so called becasue 4 different RF chips are needed to cover the range of technologies used by those protocols).

The Flysky [AFHDS 2A](https://www.multi-module.org/using-the-module/protocol-details/flysky-afhds2a) protocol and the [RadioLink](https://www.multi-module.org/using-the-module/protocol-details/radiolink) protocol of the RXs mentioned above are supported.

Various companies produce 4in1 modules, e.g. [RadioMaster](https://www.radiomasterrc.com/products/rm-4in1-module) and [iRangeX](https://www.banggood.com/IRangeX-IRX4-Plus-2_4G-CC2500-NRF24L01-A7105-CYRF6936-4-IN-1-Multiprotocol-ARM-TX-Module-With-Case-p-1225080.html).

### Spektrum DX5C

If you're interested to see the cheapest TX, with at least 5 channels, from one of the traditional RC manufacturers, it's probably the [Spektrum DX5C](https://www.spektrumrc.com/product/dx5c-smart-5-channel-dsmr-transmitter-with-sr6100at-receiver/SPM5120.html) - costing a mere US$220.

RC reviews and guides
---------------------

In googling for non-video reviews and guids, I kept on finding what I wanted on [QuadifyRC](https://www.quadifyrc.com/). The site has lots of in-depth reviews and lots of guides (like [this one](https://www.quadifyrc.com/rccarreviews/124019-budget-setup-and-tuning-guide-2021-get-the-most-out-of-your-car) to setting up and tuning your budget RC car).

---

4-lane MIPI / USB-3 / 8GB SBCs:

* [Orange Pi 5](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-5-32GB.html)

High-performance SBCs
---------------------

The Nvidia Nano DevKit used to be the obvious choice for situations where you needed an AI focused SBC. However, they've become hard to source (but you can still get them from [Waveshare](https://www.waveshare.com/product/ai/boards-kits/jetson-nano.htm)) and they're quite old now. I found this [comparison of the Nano with the Google Coral](https://www.raccoons.be/resources/insights/performance-comparison-:-coral-edge-tpu-vs-jetson-nano) very interesting - and the two main factor holding the Coral back (lack of USB 3.0 support on the Raspberry Pi) has now been addressed in the Raspberry Pi 5.

Note: in addition to the Nano, you can also get Nvidia TX2, Xavier and Orin boards but these are far more expensive.

Up until now, Raspberry Pi has used USB 2.0 and 2-lane MIPI. The first affects its ability to get the most out of hardware like the [Google Coral USB accelerator](https://coral.ai/products/accelerator) for ML inferencing and the second limits its ability to use the high-quality but competitively priced cameras that have become common for digital FPV like the [DJI O3 camera module](https://www.getfpv.com/fpv/cameras/dji-o3-air-unit-camera-module.html).

The [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) addresses both these issues. Unfortunately, it's currently almost impossible to buy.

There are almost no similarly spec'd (USB-3 / 4-lane MIPI / 8GB memory) SBCs out there at a similar price point.

The few that exist all seem to be based around the RK3588 - actually two variants the RK3588 and the RK3588S (which is identical to the RK3588 from a performance perspective but supports fewer peripherals, e.g. only one 4-lane MIPI camera - see [here](https://wiki.radxa.com/Rock5/RK3588_vs_RK3588S) for more details).

The most interesting looks to be the [Orange Pi 5](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-5-32GB.html) (which is available with up to a maximum of 32GB vs the 8GB of the Raspberry Pi 5).

As well as a maximum of 32GB (vs the 8GB of the Raspberry Pi 5) it seems to have several other advantages:

* The RK3588S is more powerful than the BCM2711 (see [here](https://www.cpubenchmark.net/compare/4297vs4906/BCM2711-vs-Rockchip-RK3588)).
* It features the camera connectors standard with digital FPV cameras rather than the Raspberry Pi-style [connector](https://www.raspberrypi.com/documentation/computers/raspberry-pi-5.html#mipi-csidsi-connectors).
* It has a PCIe M.2 SSD connector (whereas the Raspberry Pi 5 requires an additional hat to make its PCIe connector useable for SSDs). **Important:** there's a variant of the Orange Pi 5 called the 5B that has built-in WiFi but the down-side is it has no SSD connector.

Important: there are many different SSD connectors, the PCIe M.2 ones have a single notch to one side of the main connector, while SATA III ones have two notches, one to either side of the main connector. Then there's mSATA - this is an older standard that has a connector that looks identical to PCIe M.2 but usually has two holes at the other end of the board (for securing it in place) rather than the single semi-circle seen on M.2 SSDs. There are various lengths of SSD, the shortest type are 2230 (22x30mm), then there's 2242 (22x42mm) and the full-size ones are 2280 (22x80mm). The Orange Pi 5 board holes for securing 2230 or 2242 lengths.

Camera note:

* I'm not quite sure about the camera connector compatability - the connectors on the Orange Pi 5 look very like the connectors on the Raspberry Pi camera module board (as opposed to those on the Pi board itself). Previously, you're only option for using certain camera modules, with the Raspberry Pi,  was to buy a Raspberry Pi camera, detach its camera module (leaving just the board with its connector for the camera module and its outgoing connector to the Raspberry Pi) and then swap-in the new module, e.g. see the _How to use_ section for the [160&deg; IMX219 camera module](https://waveshare.com/imx219-d160.htm).
* The Orange Pi has three camera connectos, however the RK3588S supports one 4-lane camera and two 2-lane cameras so presumably, only one of the board's camera connectors is 4-lane capable (but I don't know which one - and perhaps none of the connectors is actually 4-lane capable).

One downside of the Orange Pi 5 vs the Raspberry Pi 5 is that there's [active cooler](https://www.raspberrypi.com/products/active-cooler/) for the  Raspberry Pi 5 that [clearly works](https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/). The spring-loaded push pins needed for the mechanical connection of a cooler aren't present on the Orange Pi 5 and Orange Pi don't see anything similar for the Orange Pi 5 (they do sell an [aluminium case](http://www.orangepi.org/html/hardWare/cases/details/Orange-Pi-Shell.html) where the case is supposed to act as a large heatsink). So, you have to resort to third-party solutions for an active cooler.

AliExpress is great for things that look good but may not actually do anything useful, e.g. this [large heatsink with fan](https://www.aliexpress.com/i/1005005116029772.html) (also avaiable [here](https://www.aliexpress.com/item/1005005115515888.html) and [here](https://www.aliexpress.com/item/1005005117005722.html)) specifically for the Orange Pi 5 looks great but (according to this [video](https://www.youtube.com/watch?v=BYM0jS9CHzM)) does almost nothing. The only branded item that reviews seem to show definitely works, is the rather over-the-top looking [EP-0167](https://wiki.52pi.com/index.php?title=EP-0167) from 52pi (AKA GeeekPi). They also sell a less OTT looking fan and heatsink combination (marketed as being for the the 5 Plus but should work with anything) - the [F-0021](https://wiki.52pi.com/index.php?title=F-0021).

Links:

* [Orange Pi 5 product page](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-5-32GB.html).
* AliExpress - [Orange Pi 5](https://www.aliexpress.com/item/1005004941850323.) - CHF80.
* AliExpress - [Orange Pi 5 aluminum case](https://www.aliexpress.com/item/1005005551883118.html) - CHF12.
* AliExpress - [52pi - heatsink and fan for Orange Pi 5 Plus](https://www.aliexpress.com/item/1005005670303855.html) - CHF8
* AliExpress - [52pi - radiator and fan for Orange Pi 5](https://www.aliexpress.com/item/1005005476149321.html) - CHF13

Note: shipping costs for some items on the 52pi AliExpress store are oddly high - the GeeekPi store has the [radiator/fan](https://www.aliexpress.com/item/1005005471772657.html) and [heatsink/fan](https://www.aliexpress.com/item/1005005676059693.html) at more normal shipping prices.

SSDs:

* 256GB mid-size 2242 [Transcend M.2 MTE400S](https://www.digitec.ch/de/s1/product/transcend-ssd-256gb-transcend-m2-mte400s-m2-2242-pcie-gen3-x4-nvme-256-gb-m2-ssd-23716353)
* 256GB short 2230 [Transcend M.2 MTE300S](https://www.digitec.ch/de/s1/product/transcend-ssd-256gb-transcend-m2-mte300s-m2-2230-pcie-gen3-x4-nvme-256-gb-m2-ssd-24136264)

The longer 2242 has marginally better write performance under certain circumstances but otherwise the two are identical performance wise.

**Important:** initially, it was rather invovled getting the Orange Pi 5 to boot from an SSD but now it should work out of the box on both Armbian (using `armbian-config`) and Orange Pi's own Ubuntu image which includes their `orangepi-config` (the source for which can be found [here](https://github.com/orangepi-xunlong/orangepi-build)). All the Orange Pi 5 supported OS images can be found [here](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/service-and-support/Orange-pi-5.html).

RememberThisTech has a [nice video](https://www.youtube.com/watch?v=1Tg9Czlhpy8) on getting the SSD going with the Orange Pi (in particular at 4m 10s he points out you should **update the bootloader and firmware**). See also, James A. Chamber's [blog post](https://jamesachambers.com/orange-pi-5-ssd-boot-guide/) on doing this as well.

Linux:

* [Orange Pi OSes](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/service-and-support/Orange-pi-5.html).
* [Armbian for Orange Pi 5](https://www.armbian.com/orangepi-5/).

Note: there's also the Orange Pi 5 Plus that has a RK3588 (so could support to 4-lane MIPI cameras) and has two PCIe M.2 connectors (so, could take both a WiFi6 modules and an SSD). However, it's about twice the weight of the non-Plus and has a whole load of connectors (e.g. 2 HDMI out and one HDMI in) that are irrelevant for a headless robotics setup. Unlike the non-Plus, the Plus does have the holes needed for the style of active cooler that the Raspberry Pi 5 supports and Orange Pi sell a suitable [cooler accessory](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Cooling-Fan.html).

Various other brands also produce RK3588 based boards, two of the better known are Banana Pi and FriendlyElec. However, their boards are pricier and more like the Orange Pi 5 Plus:

* [Banana Pi BPI-W3](https://wiki.banana-pi.org/Banana_Pi_BPI-W3) (available for US$160 [here](https://www.aliexpress.com/item/1005005492412383.html) on AliExpress).
* [FriendlyElec NanoPC-T6](https://www.friendlyelec.com/index.php?route=product/product&product_id=292) (the 8GB variant is US$120).

Other fan options:

* Shenzhen Green Technology [2 or 3-pin 5V fan with 40x40x12mm heatsink](https://www.aliexpress.com/i/32405641385.html).
* Shenzhen Green Technology [2-pin 5V fan with 28x23x8mm heatsink](https://www.aliexpress.com/item/4000297043992.html).
* Aokin [primary heatsink with two fans plus LAN and RAM heatsinks](https://www.aliexpress.com/item/33030333140.html).
* DIYzone [heatsink with fan plus LAN and USB controller heatsinks](https://www.aliexpress.com/item/4000279401589.html).
* Reichelt same [heatsink and fan combo](https://www.reichelt.com/ch/de/raspberry-pi-luefter-kuehlkoerper-25x25x13mm-dupon-rpi-fan-25x25-p291502.html) as DIYzone.
* Reichelt make your own with a [43x43x16mm heatsink](https://www.reichelt.com/ch/en/heat-sink-for-pga-43-x-43-x-16-5-mm-v-ick-pga43x43-p100979.html), [40x40mm fan](https://www.reichelt.com/ch/en/axial-fan-40x40x10mm-5v-12m-h-23dba-sun-ee40100s2-1-p260551.html) and [thermal pad](https://www.reichelt.com/ch/en/minus-pad-8-120-x-20-x-0-5-mm-tg-mp8-120-05-1-p156508.html) (they don't have 40x40mm pads so, you'll need to cut up this 120x20mm pad) (you'll still need to screw the fan down onto the heatsink).

Given that 52pi seem to make models that are known to work, I'm inclined to buy their fan/heatsink combo over the no name alternatives (and it's cheaper than making your own using branded components from Reichelt).

However, the heatsink with 3-pin 5V fan from Shenzhen Green Technology is interesting as all the other fans are always on whereas, _I presume_ the third pin is for PWM control (as shown [here](https://www.raspberrypi.com/products/raspberry-pi-4-case-fan/) with the Pi 4 case fan). The Raspberry Pi 5 active cooler also has PWM control.

---

WiFi dongle
-----------

There are no end of no-name dongles, but the highest spec branded dongle, I could find, is the tp-link [Archer T3U](https://www.tp-link.com/us/home-networking/usb-adapter/archer-t3u/) - it supports USB 3.0, AC1300, 2.4/5GHz, MU-MIMO (tho' I wonder if my WiFi AP isn't modern enough to get the most/anything out of e.g. MU-MIMO or the speed of AC1300).

[Archer T3U](https://www.digitec.ch/de/s1/product/tp-link-archer-t3u-mini-usb-30-netzwerkadapter-10857405) at Digitec.

Voltage and current sensors
---------------------------

It'd be nice to know when the voltage of the battery was droping toward 3.xV. I think **BLHeli_32 ESC will output both voltage and current information** (see OL's [BLHeli_32 telmetry page](https://oscarliang.com/esc-telemetry-betaflight/)) so, sensors like the following are _probably_ unnecessary for battery. _But_ a current sensor might be interesting for tracking the draw of the Pi and all associated electronics.

Maybe, for the battery, it's simpler just use a module like these (though you're also getting a regulator that's not needed - unless the total FC setup consumes less than 3A):

* [PM02 V3](https://holybro.com/collections/power-modules-pdbs/products/pm02-v3-12s-power-module) analog power module - provides current and voltage information (and 5.V/3A for an FC)
* [PM02D](https://holybro.com/collections/power-modules-pdbs/products/pm02d-power-module) digital power module - provides current and voltage information (and 5.V/3A for an FC)

It'd be interesting to know what chips these are using, it might well be the same as one of the Adafruit power modules below.

Power (voltage and current) sensors:

* [Adafruit INA228](https://www.adafruit.com/product/5832)
* [Adafruit INA260](https://www.adafruit.com/product/4226)

The INA228 _seems_ to be the newer (and, according to TI, more precise) of the two - but was out-of-stack at time of writing and has yet to have a tutorial (tho' it looks very similar to the INA260).

Adafruit do have a [MAX17048 LiPo / Li-ion fuel gauge and battery monitor](https://www.adafruit.com/product/5580) but it's only suitable for 1S.

They have current sensors:

* [Adafruit INA169](https://www.adafruit.com/product/1164) - analog 5A max.
* [Adafruit INA219](https://www.adafruit.com/product/904) - digital 3.2A max.

Pololu have various analog current sensors, e.g. the [ACS711EX breakout](https://www.pololu.com/product/2452) that can handle up to 15A (they have more expensive models for lower ampages, e.g. the [ACS724](https://www.pololu.com/product/4041) which can only handle 5A but an error of +/-1.5% (vs 5% for the ACS711EX).

Batteries
---------

The highest mAh 2S batteries are 5500mAh - they simply don't seem to come biger than that.

Gensace produce three identically priced 5500mAh 7.4V 2S1P 60C variants:

* [139x48x24mm 248g](https://www.gensace.de/gens-ace-5500mah-7-4v-2s1p-60c-car-lipo-battery-pack-hardcase-24-with-t-plug.html)
* [138x47x25mm 272g](https://www.gensace.de/gens-ace-5500mah-2s-7-4v-60c-hardcase-rc-10-car-lipo-battery-pack-with-t-plug.html) - same but with removable leads.
* [140x47x25mm 318g](https://www.gensace.de/gens-ace-5500mah-2s-7-6v-60c-hardcase-rc-20-car-lipo-battery-pack-with-t-plug.html)

So, the only difference seems to be slight variations in dimensions, the last one is odd - why a heavier variation when one of the others is the same price with all dimensions the same or slightly smaller.

Of course, there are also G-Tech variants.

Note: technically, you can get more that 5500mah but the next highest capacity batteries cost more than twice as much (and don't come with Deans connectors):

* [7600mAh 2S XT60 connector - 387g](https://www.gensace.de/gens-ace-7600mah-7-4v-60c-2s2p-lipo-battery-pc-material-case-with-xt60-plug.html)
* [8200mAh S2 female bullet connectors - 301g](https://www.gensace.de/gens-ace-redline-series-8200mah-7-6v-130c-2s1p-hardcase-58-hv-lipo-battery.html)

At 3S, you can get 80% more "power" (if my math is correct) in the _reasonable_ price range but only with an EC5 or a (giant) XT90 connector:

* [6500mAh 3S with EC5](https://www.gensace.de/gens-ace-6500mah-11-1v-60c-3s1p-lipo-battery-pack-with-ec5-bashing-series-2292.html)
* [6500mAh 3S with XT90](https://www.gensace.de/gens-ace-6500mah-11-1v-60c-3s1p-lipo-battery-pack-with-xt90-bashing-series-2339.html)

Above [8000mAh 3S with EC5](https://www.gensace.de/gens-ace-8000mah-11-1v-100c-3s1p-lipo-battery-pack-with-ec5-bashing-series.html) prices start to rocket.

Tracks
------

The HK based Robocar Store sells tracks as roll-out mats - they're quite expensive.

They sell them in various sizes, denoted as 100%, 80%, 60% and 40%. The 100% are meant for 1/10 scale cars.

For 1/16 you should really use the 60% but even the 40% mat would be very large - at 3x4.5m - in my apartment.

The [DIYRobocars standard track](https://www.robocarstore.com/collections/tracks/products/diyrobocars-standard-track) is US$200 for the 40% variant - you can see how it looks in the videos on the linked page.

Note: [DIYRobocars](https://www.diyrobocars.com/) is a hobbyist autonomous cars community that organizes races in the Bay area and is strongly linked with Donkey Car.

You can find DIYRobocars description of the track [here](https://www.diyrobocars.com/110th-scale-race-rules/) and a higher-res image of it [here](https://www.diyrobocars.com/wp-content/uploads/2019/07/Untitled.png) (that also shows the location of the cones that mark various parts of the track).

But in this DIYRobocars [blog post](https://www.diyrobocars.com/2019/08/12/adventures-with-the-nvidia-jetbot-and-jetracer/), you can see tracks laid down nicely with just tape.

### AWS DeepRacer tracks

The standard DeepRacer templates can be found [here](https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-track-examples.html) (even the basic loop track is 3.5x4.5m) along with instructions on how to lay them out with tape.

The tracks and barriers used to available from Amazon (for the amazing price of US$900 for a basic track and US$1,700 for a set of barriers).

Robocar has them available at more reasonable prices:

* [Basic track](https://www.robocarstore.com/products/aws-deepracer-standard-track) - 5x7.5m - US$440.
* Same track but as [heavy duty carpet variant](https://www.robocarstore.com/products/aws-deepracer-standard-track-carpet-version) - US$2,300.
* [Barriers](https://www.robocarstore.com/collections/tracks/products/fence-with-cover-for-aws-track) - 20 pieces - US$45.

But to be fair, their [docs](https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-build-your-track-materials-and-tools.html) suggest instead using [Tarco asphalt saturated organic felt](https://www.tarcoroofing.com/products/roofapp/shingles/mechanically-attached/asphalt-saturated-organic-felt) (the variant called _30# ASTM Specification Felt_). (which comes in 1x2m roles for around US$45).

I tried searching for track on AliExpress but didn't have much luck - all I found was this [track](https://www.aliexpress.com/item/1005001495620929.html) from BlueRaven for US$30.

### Protective mats

An alternative track surface are the interlocking mats found in places like gyms:

* [Gorilla Sports protective mat set](https://www.galaxus.ch/en/s3/product/gorilla-sports-protective-mat-set-120-cm-floor-guards-9315746) - 8 mats with total area 1.2x2.4m for CHF60.
* [Gonser floor mat set](https://www.gonser.ch/bodenmatte-61-x-61-x-1-2-cm-schwarz-20-er-set/a-10684/) - 20 mats with total area 2.4x3m for CHF120.

AWS DeepRacer
-------------

The DeepRacer [https://aws.amazon.com/deepracer/getting-started/] getting started guide is an interesting intro to Amazon's take on the field.

And it's interesting to see the dual-camera layout and how the lidar is mounted in the [blog post](https://aws.amazon.com/blogs/machine-learning/aws-deepracer-evo-and-sensor-kit-now-available-for-purchase/) introducing the DeepRacer Evo (one assumes the plastic of the shell is transparent to the lidar).

The [product page](https://aws.amazon.com/deepracer/) for the DeepRacer (original and Evo) describes the chassis as that of a "18th scale 4WD with monster truck" and from the [spare parts page](https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-vehicle-chassis-parts.html), it's clear the chassis comes from the [Wltoys A979](https://www.wl-toys.com/Wltoys-A979-rc-car-rc-racing-car-Parts-Wltoys-A979-High-speed-118-Full-scale-rc-racing-car-Max-Speed-50km-h-Shockproof-10053.html). This is one of Wltoys oldest models (it came out first in 2014).

Traxas
------

Interesting Traxxas models:

* [Traxxas brushless 4WD 1/10 Rustler VXL](https://traxxas.com/products/landing/rustler-4x4-vxl/)
* [Traxxas brushless AWD 1/10 chassis](https://traxxas.com/products/models/electric/4-tec-2-vxl-chassis)
* [Traxxas brushless 4WD 1/16 E-Revo VXL](https://traxxas.com/products/models/electric/erevo-vxl-116-tsm)
* [Traxxas brushed 4WD 1/16 Slash](https://traxxas.com/products/models/electric/70054-8-slash-116)

The shocks on the 1/16 models look very strange - if you look closely the shafts where you'd expect shocks are actually connected to springs (and, one assumes, oil-filled shocks) mounted in the body.

Tamiya
------

Note: all of the models below are 4WD. Tamiya builds look to be non-trivial, e.g. see this build log for the [TXT-1](http://www.technicopedia.com/RC/TXT-1/txt1.html).

The Tamiya TT-02 is a classic Tamiya chassis with various more modern variants:

* [TT-02R race chassis](https://www.tamiyausa.com/shop/110-4wd-shaft-drive-road-tt/rc-tt-02r-chassis-kit-2/) RRP US$218
* [TT-02 type S sports chassis](https://www.tamiyausa.com/shop/110-4wd-shaft-drive-road-tt/rc-tt-02-type-s-chassis-kit/) RRP US$282
* [TT-02 type SRX chassis](https://www.tamiyausa.com/shop/110-4wd-shaft-drive-road-tt/rc-tt-02-type-srx-chassis-kit/) (an upgrade of the type S) RRP US$359
* [TT-02BR chassis](https://www.tamiyausa.com/shop/-road-buggies/rc-tt-02br-chassis-kit/) RRP US$359

Note: the type S comes with a brushed motor but no servo, the other two include neither motor nor servo. For a run-thru of Tamiya 540 motors see [Blasted RC's overview](https://www.blasted-rc.com/blogs/getting-started-in-rc/whats-the-difference-between-tamiya-540-motors). They list the BLM-02S as the most popular of the brushless variants and costs about CHF90 and comes in 10.5T to 21.5T variants (where T is turns and can be roughly related to Kv).

From Digitec:

* [TT-02 type S](https://www.galaxus.ch/de/s5/product/tamiya-tt-02-type-s-chassis-kit-rc-auto-12012030) CHF 149
* [TT-02R](https://www.digitec.ch/de/s1/product/tamiya-tt-02r-chassis-kit-rc-auto-5809462) CHF 177
* [TT-02 type SRX](https://www.digitec.ch/de/s1/product/tamiya-tourenwagen-tt-02-type-srx-chassis-kit-rc-auto-23899203) CHF 279
* [TT-02BR](https://www.digitec.ch/de/s1/product/tamiya-tt-02br-kit-rc-auto-23899141) CHF 309

The TT-02B doesn't seem to be available as a plain chassis but you can get various very cheap TT-02B models (with body and brushed motor but no servo), e.g.:

* [Neo Scorcher](https://www.digitec.ch/de/s1/product/tamiya-neo-scorcher-kit-rc-auto-20329353) CHF 113
* [Plasma Edge II](https://www.galaxus.ch/de/s5/product/tamiya-plasma-edge-ii-kit-rc-auto-20985860) CHF 119

Other interesting models:

* [1/12 Toyota Land Cruiser](https://www.tamiyausa.com/shop/110-trucks/rc-toyota-land-cruiser-40-pup-3/) (CHF 179 at [Brack](https://www.brack.ch/tamiya-monster-truck-toyota-land-cruiser-40-pick-up-bausatz-1311824)
* 

Banggood
--------

* MJX Hyper Go [16208/16209](https://www.banggood.com/MJX-16208-16209-HYPER-GO-1-or-16-Brushless-High-Speed-RC-Car-Vechile-Models-45km-or-h-p-1967165.html)
* MJX Hyper Go [16207](https://www.banggood.com/MJX-16207-HYPER-GO-1-or-16-Brushless-High-Speed-RC-Car-Vechile-Models-45km-or-h-p-1967172.html)
* MJX Hyper Go [16210](https://www.banggood.com/MJX-16210-1-or-16-Brushless-High-Speed-RC-Car-Vehicle-Models-45km-or-h-p-1967083.html)
* MJX Hyper Go [14210](https://www.banggood.com/MJX-14210-HYPER-GO-1-or-14-Brushless-High-Speed-RC-Car-Vechile-Models-55km-or-h-p-1991233.html)
* HBX [16889a Pro](https://www.banggood.com/HBX-16889A-Pro-1-or-16-2_4G-4WD-Brushless-High-Speed-RC-Car-Vehicle-Models-Full-Propotional-p-1876495.html)
* Eachine [Flyhal FC600](https://www.banggood.com/EACHINE-Flyhal-FC600-Two-Batteries-RTR-1-or-16-2_4G-4WD-45km-or-h-Brushless-Fast-RC-Cars-Trucks-Vehicles-with-Oil-Filled-Shock-Absorber-p-1890171.html)
* Wltoys [124008](https://www.banggood.com/Wltoys-124008-RTR-1-or-12-2_4G-4WD-3S-Brushless-RC-Car-60km-or-h-Off-Road-Climbing-High-Speed-Truck-Full-Proportional-Vehicles-Models-Toys-p-1986964.html)

According to [QuadifyRC](https://www.quadifyrc.com/rccarreviews/hbx-16889a-pro-review-i-think-this-is-the-best-small-basher-ive-ever-had) the Flyhal FC600 is the same chassis as the 16889a Pro with a different body and wheels.

Rlaarlo 1/12 [AM-X12](https://rlaarlo.com/products/rlaarlo-amx12) - not from Banggood, Rlaarlo seem to specialize in selling direct. Rather pricier than any of the other models.

YouTube channels
----------------

Coming from the drone world where the crash-and-repair cycle means the bigger channels are more about build and setup, the RC car world seems a bit different with ready-to-run (RTR) being far more normal.

As such the channels, I've found most useful for _cheap_ RC cars are quite different to the ones I'd follow in the drone world.

My choice of best channels for _cheap_ RC cars:

* [beyondRC](https://www.youtube.com/@beyondRC/videos), e.g. [Top 10 CHEAP RC Cars of 2023](https://www.youtube.com/watch?v=bl0TjC6x5f0) and [Top 5 CHEAP RC CARS for CHRISTMAS 2023!](https://www.youtube.com/watch?v=HxwGfyqv41U).
* [Derby City RC](https://www.youtube.com/@DerbyCityRC/videos), e.g. [10 BEST RC cars UNDER $150](https://www.youtube.com/watch?v=LnMqcFo1_0s).
* [Tomley RC](https://www.youtube.com/@TomleyRC/videos), e.g. [The TOP $99 RC Cars of 2023](https://www.youtube.com/watch?v=kJLdkCQm8TE).

There's also [Kevin Talbot](https://www.youtube.com/@KevinTalbotTV/videos) - in terms of subscribers, he's way ahead of the others but he only occassionally looks at cheaper models (and he's rather loud and shouty).

Toe-in
------

The toe of the back wheels is generally fixed, while the toe of the front wheels can be changed by adjusting the turnbuckle links of the front wheel assembly.

See AMain Hobbies page [Understanding RC Wheel Adjustment: Camber, Caster, and Toe](https://www.amainhobbies.com/understanding-rc-wheel-adjustment-camber-caster-and-toe/cp1132) for when and why you would want a toe-in toe-neutral or toe-out configutation.

[Turnbuckle wrench](https://www.aliexpress.com/item/32760668491.html) from U-Angel-1988 AliExpress store  - US$1.60 plus $0.60 shipping.

Misc
----

[Luxonis OAD-D S2](https://shop.luxonis.com/collections/oak-cameras-1/products/oak-d-s2)

[Self-driving car on a shoestring project](https://towardsdatascience.com/deeppicar-part-1-102e03c83f2c) - uses a Pi and a Google Coral - doesn't use ROS or Donkey Car - build using TensorFlow.

### Waveshre JetRacer

Their Jetson Nano models:

* [JetRacer Pro](https://www.waveshare.com/product/ai/robots/mobile-robots/jetracer-pro-ai-kit.htm)
* [JetRacer Pro with lidar](https://www.waveshare.com/product/ai/robots/mobile-robots/jetracer-ros-ai-kit.htm)
* [JetBot Pro with lidar](https://www.waveshare.com/product/ai/robots/mobile-robots/jetbot-ros-ai-kit.htm) - two wheeled variant.

They also have guides for using their robots/cars with [Donkey Car](https://www.waveshare.com/wiki/DonkeyCar_for_Jetson_Nano-Calibrate_DonkeyCar), [autonomous driving](https://www.waveshare.com/wiki/JetRacer_AI_Kit#interactive-regression), [ROS](https://www.waveshare.com/wiki/JetBot_AI_Kit:_ROS) (unfortunately, ROS 1) and more.
