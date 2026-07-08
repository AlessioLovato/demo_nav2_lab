# Command Execution for Concert Demo

To keep the systems separated, the **CONCERT onboard sub-network** uses `ROS_DOMAIN_ID=100`, while **PILOT** uses `ROS_DOMAIN_ID=77`.

This setup is required because automatic discovery range do not work reliably.

> [!NOTE]
> **Full demo order:** this README covers the **ROS2** navigation pipeline. The demo can also have a **ROS1** drilling part, documented separately in [`DRILLING_DEMO.md`](DRILLING_DEMO.md). See [below](#9-optional-drilling--switch-back-to-ros1) for exactly when to switch over — in short, control bringup (ROS1) must run *before* the rest of this navigation pipeline, and the actual drilling only happens once the robot has arrived at its target via navigation.

---

## 1. Preliminaries

1. Turn on the robot by pressing the two power buttons:

   * First, press the button closer to the middle of the robot.
   * Then, press the second button.

   Do **not** hold the buttons.

2. CONCERT should start powering on. A **white light** should turn on.

3. When you are ready to start the full system:

   * Press the dead-man / emergency button.
   * The **green light** on the robot should turn on.

---

## 2. Embedded PC — XBot2 and EtherCAT

On the **Embedded PC** (appears as `mio-concert` in the terminal):

* IP address: `10.24.10.100`
* Access command: `ssh_embedded` (from pilot)

Open **three separate terminals** and  after having turned on CONCERT, wait 5 seconds before running these commands:

### Terminal 1 — Start EtherCAT Master

```bash
repl -f /home/user/data/forest_ws/src/concert_config/ecat/ecat_config.yaml
```

You should see that the master tries to connect to at least 20 slaves.

### Terminal 2 — Start XBot2 Core

When the previous script has arrived at the output "_started looping_", then wait a few seconds and run

```bash
xbot2-core --hw ec_imp -C /home/user/data/forest_ws/src/concert_config/ModularBot.yaml
```
You should hear the brakes th
### Terminal 3 — Start XBot2 GUI Server

This enables the XBot2 connection from the tablet.

```bash
xbot2_gui_server
```

On the tablet, connect to:

```text
IP:   10.24.10.100
Port: 8080
```

---

## 3. Control PC — Back LiDAR and IMU

On the **Control PC**:

* IP address: `10.24.10.102`
* Access command: `ssh_control` (from pilot)

Open **two separate terminals** and run the following commands to bring up the IMU and rear VLP LiDAR.


### Terminal 1 — Start IMU / VectorNav

```bash
ros2 launch vectornav vectornav.launch.py
```

### Terminal 2 — Start Rear Velodyne VLP-16 LiDAR

```bash
ros2 launch concert_config velodyne-VLP16_back.launch.py
```

---

## 4. Vision PC

On the **Vision PC**:

* IP address: `10.24.10.101`
* Access command: `ssh_control` (from pilot)

Open **two separate terminals** and launch the front VLP LiDAR and the Zenoh DDS bridge.


### Terminal 1 — Front Velodyne VLP-16 LiDAR

```bash
ros2 launch concert_config velodyne-VLP16_front.launch.py
```

### Terminal 2 — Zenoh DDS Bridge

```bash
zenoh-bridge-ros2dds
```

---

## 5. Pilot

On **PILOT** (IP address: `10.24.10.77`), start the Zenoh DDS bridge and point it to the Vision IP.

```bash
zenoh-bridge-ros2dds -e tcp/10.24.10.101:7447
```

Then load whatever visual interface you need.

---

## 6. SLAM

On **Vision**, make sure the repositories are on the following branches:

| Repository             | Branch           |
| ---------------------- | ---------------- |
| `concert_localization` | `master`         |

Then run:

```bash
ros2 launch concert_localization rtabmap.launch.py
```

---

## 7. Localization

On **Vision**, make sure `concert_localization` is on branch `master`.
**For this part a PCD map is required. Seen note below.**

Then run:

```bash
ros2 launch concert_localization hdl_localization.launch.py map_file:=/path/to/map.pcd
```

> **Note:**
> If you are using `rtabmap.launch.py` to collect the PCD file launched from `forest_ws` folder, the generated `.pcd` file is usually saved under:
>
> ```text
> /home/user/data/forest_ws/maps
> ```

---

## 8. Navigation

On **Vision**, make sure `concert_navigation` is on branch `test_alelovato`.<br>
**For this part a Nav2 style map is required. Seen note below.**

Then run:

```bash
ros2 launch concert_navigation navigation.launch.py map_file:=/path/to/map.yaml
```

> **Note:**
> To convert a PCD file into Nav2 maps, use:
>
> ```bash
> ros2 launch pcd_to_nav2_map.launch.py map_file:=/path_to_pcd_file
> ```
>
> This will generate a folder containing the converted `.pgm` and `.yaml` map files.
>
> You can also use launch parameters to configure the map height.

---

## 9. **[OPTIONAL]** Drilling — Switch back to ROS1

Once the robot has arrived at the drilling point via the navigation pipeline above, go back to **[`DRILLING_DEMO.md`](DRILLING_DEMO.md)** and run the drilling operation from ROS1, using the `ros1_bridge` to reach the CONCERT ROS2 topics.
