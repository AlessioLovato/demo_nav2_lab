# Command Execution for Concert Demo

To keep the systems separated, the **CONCERT onboard sub-network** uses `ROS_DOMAIN_ID=100`, while **PILOT** uses `ROS_DOMAIN_ID=77`.

This setup is required because automatic discovery did not work reliably.

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

On the **Embedded PC**:

* IP address: `10.24.10.100`
* Access command: `ssh_embedded`

Open **three separate terminals** and run the following commands.

### Terminal 1 — Start EtherCAT Master

```bash
repl -f /home/user/data/forest_ws/src/concert_config/ecat/ecat_config.yaml
```

### Terminal 2 — Start XBot2 Core

```bash
xbot2-core --hw ec_imp -C /home/user/data/forest_ws/src/concert_config/ModularBot.yaml
```

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

On the **Vision PC**, launch the front VLP LiDAR and the Zenoh DDS bridge.

### Front Velodyne VLP-16 LiDAR

```bash
ros2 launch concert_config velodyne-VLP16_front.launch.py
```

### Zenoh DDS Bridge

```bash
zenoh_dds2_bridge
```

---

## 5. Pilot

On **PILOT**, start the Zenoh DDS bridge and point it to the Pilot IP.

```bash
zenoh_dds2_bridge <ip_pilot>
```

---

## 6. SLAM

On **Vision**, make sure the repositories are on the following branches:

| Repository             | Branch           |
| ---------------------- | ---------------- |
| `concert_localization` | `master`         |
| `concert_navigation`   | `test_alelovato` |

Then run:

```bash
ros2 launch concert_localization rtabmap.launch.py
```

---

## 7. Localization

On **Vision**, make sure `concert_localization` is on branch `master`.

Then run:

```bash
ros2 launch concert_localization localization.launch.py map_file:=/path/to/map
```

> **Note:**
> If you are using `rtabmap.launch.py` to collect the PCD file, the generated `.pcd` file is usually saved under:
>
> ```text
> current_dir/maps
> ```

---

## 8. Navigation

On **Vision**, make sure `concert_navigation` is on branch `test_alelovato`.

Then run:

```bash
ros2 launch concert_localization navigation.launch.py map_file:=/path/to/map.yaml
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
