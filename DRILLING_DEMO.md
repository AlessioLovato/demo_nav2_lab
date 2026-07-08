# Drilling Demo (ROS1)

This guide covers the **ROS1** side of the demo: bringing control up from the XBot2 GUI, bridging it into ROS2, and running the drilling operation. It's meant to be interleaved with the **ROS2** navigation pipeline in [`README.md`](README.md), in this order:

1. **Control Bringup** — bring up control from the XBot2 GUI on the tablet.
2. **ROS1 Bridge Bringup** — bridge the robot description (and other topics) from ROS1 to ROS2 over `ros1_bridge`.
3. **Navigation Startup** — back to [`README.md`](README.md) to bring up SLAM, localization, and navigation.
4. **Demo** — navigate autonomously to the drilling point and drill.

---

## 1. Control Bringup

**Why first:** `control_bringup` brings up the LiDARs in ROS1 as part of its startup checks, even though they aren't otherwise used here — so this step has to run *before* the rest of the navigation pipeline.

1. On the tablet, open the XBot2 GUI and connect it to `10.24.10.102`.
2. Run the **`ecat`** plugin, then the **`control_bringup`** plugin.
3. Wait for both to complete successfully.
4. Once bringup has succeeded, turn off the LiDARs plugin — it's no longer needed.

---

## 2. ROS1 Bridge Bringup

All of the following commands run **inside the `concert_ros_bridge` docker container**, on the **Controller PC** — enter the PC directly, via `ssh_docker` if on the pilot, or `ssh concert@10.24.10.102` otherwise.

You'll need **3 separate terminals**: two to republish XBot2 params as ROS1 topics, and one to run the actual ROS1 ↔ ROS2 bridge.

### 2.1 Terminal 1 — Param republish

First, start the container:

```bash
docker start concert_ros_bridge
```

Then attach a new terminal to it:

```bash
# Attach to the container
docker exec -it concert_ros_bridge /bin/bash
```

Now republish the robot description param as a topic — the ROS2 side needs it as a topic, not a param:

```bash
# Source the ROS1 ws
cd concert_ros_bridge_ws
source ros1_ws/install_isolated/setup.bash
# Convert param to topic for ROS2 - base estimation requires a ROS2 topic
rostopic pub /xbotcore/robot_description std_msgs/String "data: $(rosparam get /xbotcore/robot_description)"
```

### 2.2 Terminal 2 — Param republish

Same as above, but for the semantic description:

```bash
# Attach to the container
docker exec -it concert_ros_bridge /bin/bash
```

```bash
# Source the ROS1 ws
cd concert_ros_bridge_ws
source ros1_ws/install_isolated/setup.bash
# Convert param to topic for ROS2 - base estimation requires a ROS2 topic
rostopic pub /xbotcore/robot_description_semantic std_msgs/String "data: $(rosparam get /xbotcore/robot_description_semantic)"
```

### 2.3 Terminal 3 — Launch the `ros1_bridge`

```bash
# Attach to the container
docker exec -it concert_ros_bridge /bin/bash
```

```bash
# Export DOMAIN ID to match the subnet
export ROS_DOMAIN_ID=100 # DOMAIN ID of CONCERT subnet
export ROS_LOCALHOST_ONLY=0
# Source the ROS2 ws
cd concert_ros_bridge_ws
source ros2_ws/install/setup.bash
# Load param and run the bridge
rosparam load config/ros_bridge_config.yaml
ros2 run ros1_bridge parameter_bridge
```

At this point the bridge is online, and the republished topics should be visible from any ROS2 terminal in the CONCERT subnet.

---

## 3. Navigation Startup

Go back to [`README.md`](README.md) to bring up localization and navigation.

---

## 4. Demo

With the drilling plugin and navigation both up, start the demo: send the robot to autonomously navigate to the drilling point, and once it arrives, start drilling on the wall.