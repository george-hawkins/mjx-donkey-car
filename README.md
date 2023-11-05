
Parts:

Body clips: M001
Oil-filled shocks: 16500R
Steering Linkage: 16431
Wheel Assembly: 16300B
F/R Body Pillars: 16281
Bolts for body pillars: M2684

Tool for steering linkage

More standard name for steering linkage seems to be "turnbuckle links" - <https://www.amainhobbies.com/understanding-rc-wheel-adjustment-camber-caster-and-toe/cp1132>

Manual: https://www.hobbiesaustralia.com.au/assets/files/MJX-16208-16209-16210-manual.pdf

Weirdly the English MJX site doesn't have any manuals page hasn't been updates with anythong post 2017.

On their Chinese site, you can find manuals for the 16208 etc. but in Chinese: http://www.mjxrc.com/down_list/instruction.html

---

I was looking for some three-way splitter to split off power from the battery cabling to the Pi or Nano SBC to achieve something like the Holybro PMO2:

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

Raspberry Pi 5 power limiting - the Pi 5 will, by default, provide _less_ power via USB as it needs more itself.

If you "wish to drive high-power peripheral, [you need a] USB-C power adapter which supports a 5V, 5A (25W) operating mode. If the Raspberry Pi 5 firmware detects this supply, it increases the USB current limit to 1.6A, providing 5W of extra power for downstream USB devices".

So, if using a supply that doesn't have USB-C's ability to signal this ability, I _guess_ you have to use "the option to override the current limit".

---

Question: is using an SD card rather than an SSD or an eMMC module on a Pi be an issue - this video <https://www.youtube.com/watch?v=Bf7kSNWbcrU> mentions that the slowness of the SD card may be relevant.

---

This guy made an interesting start on a ROS based self-driving RC car: <https://www.youtube.com/watch?v=Bf7kSNWbcrU>

Unfortunately, he never got around to the later chapters.

He's using stuff from the MIT Racecar project: <https://mit-racecar.github.io/hardware/>

Including VESC - an open source ESC that can provide tachometer/odometry data - I wonder if [BLHeli_32](https://github.com/bitdump/BLHeli/tree/master/BLHeli_32%20ARM) can do something similar?

BLHeli_32 certainly provides RPM telemetry data which sounds similar.

---

I pre-ordered an 8GB Raspberry Pi 5 from <https://shop.pimoroni.com/>

And registered for a restock update from Reichelt.

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
* TX - <https://www.aliexpress.com/item/1005005773630207.html>
* RX - <https://www.aliexpress.com/item/4000169189998.html>
* Regulator - see Pololu above.

I suspect, you can work out if V4 Speedybee needs changes in ArduCopter relative to V3 by comparing Betaflight configs:

* <https://github.com/betaflight/unified-targets/blob/master/configs/default/SPBE-SPEEDYBEEF405V3.config>
* <https://github.com/betaflight/unified-targets/blob/master/configs/default/SPBE-SPEEDYBEEF405V4.config>

Actually, there seem to be lots of changes.

ArduCopter: <https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_HAL_ChibiOS/hwdef/speedybeef4v3>

See, also:

* <https://github.com/iNavFlight/inav/tree/master/src/main/target/SPEEDYBEEF405V3>
* <https://github.com/iNavFlight/inav/tree/master/src/main/target/SPEEDYBEEF405V4>

JB has a great video <https://www.youtube.com/watch?v=L-6r2iX1p6s> on servos with BF so maybe:

* Get things working with BF
* Then ArduCopter
* Then Articulated's ROS series
* Then Donkey Car

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

Note: Flysky also have the [G7P](https://www.flysky-cn.com/g7pdescription) (305g) using their new ANT protocol but ...

RC Review's [Flysky G7P review](https://www.youtube.com/watch?v=otPYzx7fU7I).

RadioMaster are actually about to launch an EdgeTX based TX (that can work with any existing ExpressLRS RX) for RC cars - the [MT12](https://www.radiomasterrc.com/products/mt12-surface-radio-controller) (480g).

Painless360 [RadioMaster MT12 review](https://www.youtube.com/watch?v=9k5FQxx34E0).

Remember: the screen and two-way comms isn't that big a deal if you're looking at all the data and more anyway via goggles.

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
