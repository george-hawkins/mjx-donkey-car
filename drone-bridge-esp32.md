DroneBridge ESP32
=================

I found that my Android Pixel phone could connect to the AP created by the DroneBridge device but couldn't load the device's website.

If I tried <http://dronebridge.local>, it failed with `DNS_PROBE_FINISHED_NXDOMAIN`.

If I tried <http://192.168.2.1>, the loading indicator (at the top of the page) never got beyond almost nothing.

Using my Macbook Air worked much better but the main logo and more importantly one or other of the required Javascript files would typically fail to load (I logged an issue about this [here](https://github.com/DroneBridge/ESP32/issues/53)).

![DroneBridge download failures](images/dronebridge-download-failures.png)

So, I just inlined the external `.css` and `.js` files into the `index.html` file and converted the logo into a data URI as follows.

First, clone the DroneBridge repo:

```
$ git clone git@github.com:DroneBridge/ESP32.git dronebridge-esp32
$ cd dronebridge-esp32
```

Create a data URI for the logo:

```
$ echo "data:image/png;base64,$(cat frontend/DroneBridgeLogo.png | base64 | tr -d '\r\n')"
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPoAAAAdCAYAAACDrXEHAAAACXBIWXMAAAV+AAAFfgE+AsMhAAAAGX...
```

Find the line `<img src="DroneBridgeLogo.png" alt="DB Logo">` in `index.html` and replace the filename `DroneBridgeLogo.png` with the URI generated above:

```
$ vim frontend/index.html
```

You should end up with something like `<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhE...ApUAAAAASUVORK5CYII=" alt="DB Logo">` where the URI bit is about 5,626 characters long.

And then also inline the `.js` and `.css` files (just inline their content between `<script> ... </script>` and `<style> ... </style>` tags respectively).

I didn't bother inlining `android-icon-192x192.png` and the various sized `favicon` PNGs.

Then determine the IDF version being used and store it as a shell variable:

```
$ grep -F -m 1 esp_idf_version .github/workflows/esp_idf.yml
esp_idf_version: v4.4
$ version=v4.4
```

Now, do a build. Normally, this is do-able without using Docker interactive mode but there's a bug in how the `IDF_VER` value is determined in the Docker image corresponding to the IDF version currently used by the DroneBridge project (it was fixed on Dec 1st, 2023 - see [#12636](https://github.com/espressif/esp-idf/pull/12636)):

```
$ docker run --rm -v $PWD:/project -w /project -u $UID -e HOME=/tmp -it espressif/idf:release-$version
...
> git config --global --add safe.directory /opt/esp/idf
> idf.py set-target esp32 build
> exit
```

Note: the `IDF_VER` thing isn't a big deal - it's just that the DroneBridge web UI displays the IDF version and without the `safe.directory` step it shows up as `HEAD-HASH-NOTFOUND`.

Once back out of Docker-land, the results of the build are in the `build` directory.

Unfortunately, it's not trivial (but not impossible) to upload the `.bin` files using Dockerized development environment. An easier solution is to use `pip` to install `esptool`:

```
$ python3 -m venv env
$ source env/bin/activate
$ pip install --upgrade pip
$ pip install esptool
```

Now, the `.bin` files can be uploaded to the development board. Connect the board via USB-C, determine which device it's using (in my case `/dev/ttyUSB0`), erase the flash and upload:

```
$ device=/dev/ttyUSB0
$ esptool.py -p $device erase_flash
$ esptool.py \
    -p $device \
    -b 460800 \
    --before default_reset \
    --after hard_reset \
    --chip esp32 \
    write_flash \
    --flash_mode dio \
    --flash_size detect \
    --flash_freq 40m \
    0x1000 build/bootloader/bootloader.bin \
    0x8000 build/partition_table/partition-table.bin \
    0x10000 build/db_esp32.bin \
    0x110000 build/www.bin
```

Note: there's no need to hold down the BOOT button on the board - everything is done automatically and the board is reset and restarts at the end of the process.

That's it - the board is ready - as noted, I could not successfully connect to it with my Google Pixel phone but could connect to it with my MacBook Air.

ESP32 S3
--------

Things _should_ be just as simple for an S3 board.

The build process is the same except the target is `esp32s3`:

```
$ docker run --rm -v $PWD:/project -w /project -u $UID -e HOME=/tmp -it espressif/idf:release-$version
...
> git config --global --add safe.directory /opt/esp/idf
> idf.py set-target esp32s3 build
> exit
```

At the end of the build process, it outputs the command needed to upload the result. It's almost the same as for the classic ESP32 except the that `chip` is `esp32s3`, `flash_freq` is `80m` and the address for `bootloader.bin` is `0x0`:

```
$ device=/dev/ttyUSB0
$ esptool.py -p $device erase_flash
$ esptool.py \
    -p $device \
    -b 460800 \
    --before default_reset \
    --after hard_reset \
    --chip esp32s3 \
    write_flash \
    --flash_mode dio \
    --flash_size detect \
    --flash_freq 80m \
    0x0 build/bootloader/bootloader.bin \
    0x8000 build/partition_table/partition-table.bin \
    0x10000 build/db_esp32.bin \
    0x110000 build/www.bin
```

However, after flashing, my MacBook Air and Google Pixel could see the AP the board created but couldn't connect to it (the Pixel tried a few times and then just returned to my main WiFi network and the MacBook Air just kept trying, failing and prompting for the password again).

Debugging
----------

For Linux, there's no issue with accessing serial devices from within the container, you just have to specify the device with the `--device` argument.

So, I could monitor what was going on:

```
$ docker run --rm -v $PWD:/project -w /project -u $UID -e HOME=/tmp --device=/dev/ttyACM0:/dev/ttyACM0 -it espressif/idf:release-$version
> git config --global --add safe.directory /opt/esp/idf
> idf.py monitor
Executing action: monitor
Serial port /dev/ttyACM0
Connecting....
Detecting chip type... ESP32-S3
...
I (664) DB_ESP32: AP started!
I (714) DB_ESP32: Partition size: total: 173441, used: 104165
I (714) DB_HTTP_REST: Starting HTTP Server
I (724) TCP_SERVER_SETUP: Opened TCP server on port 5760
I (724) DB_CONTROL: Opened UDP socket on port 14550
I (734) DB_CONTROL: Started control module
I (734) TCP_SERVER_SETUP: Opened TCP server on port 1603
I (744) COMM: Started communication module
```

But after this point, it didn't output anything additional.

Note: press ctrl-T ctrl-H for the monitor menu. To stop monitoring, you seem to have to _first_ unplug the board and _then_ press ctrl-T ctrl-X.

When using the classic ESP32, the following is output when my MacBook Air connects:

```
I (46552) wifi:new:<1,0>, old:<1,0>, ap:<1,0>, sta:<255,255>, prof:1
I (46552) wifi:station: ac:c9:06:15:13:11 join, AID=1, b, 20
I (46582) DB_ESP32: Client connected - station:ac:c9:06:15:13:11, AID=1
I (49512) esp_netif_lwip: DHCP server assigned IP to a station, IP is: 192.168.2.2
I (50542) esp_netif_lwip: DHCP server assigned IP to a station, IP is: 192.168.2.2
```

The preceeding output is nearly identical, the main noticeable difference is that the `used` value is higher for the classic ESP32:

```
I (902) DB_ESP32: Partition size: total: 173441, used: 162899
I (902) DB_HTTP_REST: Starting HTTP Server
I (902) TCP_SERVER_SETUP: Opened TCP server on port 5760
I (912) DB_CONTROL: Opened UDP socket on port 14550
I (912) DB_CONTROL: Started control module
I (922) TCP_SERVER_SETUP: Opened TCP server on port 1603
```

But this may be down to not using the "fat" `index.html` for the S3 (I wanted to eliminate it as part of the problem).
