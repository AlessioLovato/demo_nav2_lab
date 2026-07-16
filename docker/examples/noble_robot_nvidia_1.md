# Vision Host: Standard Docker

This document describes the configuration of the following container:

```text
noble-robot-nvidia-1
```

The container runs on the Vision host and provides:

* NVIDIA GPU access
* Intel RealSense support
* ROS 2 Jazzy
* XBot2
* Localization
* Navigation
* Defect-detection components

## Temporary `xbot.cloud` workaround

> [!IMPORTANT]
> As of July 2026, the `xbot.cloud` domain is not resolving anymore.
>
> This causes `sudo apt update` to fail when accessing the XBot2 package repository.

Inside the container, add the following temporary hostname mapping:

```bash
echo "54.73.207.169 xbot.cloud" | sudo tee -a /etc/hosts
```

Verify the mapping:

```bash
getent hosts xbot.cloud
```

Expected output:

```text
54.73.207.169 xbot.cloud
```

Then retry:

```bash
sudo apt update
```

This workaround should be incorporated into the next container image or removed once the domain becomes available again.

## Updating XBot2

At the time of writing, the installed XBot2 package may need to be removed before installing the latest nightly version because APT compares package versions lexicographically.

Run:

```bash
sudo apt update

sudo apt purge -y xbot2_desktop_full
sudo apt autoremove -y

sudo apt install -y xbot2_desktop_full
```

The currently available packages can be inspected at:

```text
http://54.73.207.169/xbot2-nightly/ubuntu/noble/
```

Compare the available package versions with the versions installed in the container:

```bash
apt policy xbot2_desktop_full
```

### Update the multidof recipes:

```bash
cd /home/user/xbot2_ws/recipes/multidof_recipes

git fetch
git checkout alelovato_recipes
git pull
```

> [!NOTE]
> The `alelovato_recipes` branch is temporary. Switch back to the `ros2` branch when the required changes have been merged.

### Update `xbot2_gui_server`:

```bash
cd /home/user/xbot2_ws/src/xbot2_gui_server
git pull
```

This includes the latest fix for an issue that prevented `xbot2_gui_server` from starting correctly.

## Shell customization

### Enable Forest autocompletion

Add the Forest completion command to `~/.bashrc` only if it is not already present:

```bash
grep -qxF 'eval "$(register-python-argcomplete forest)"' ~/.bashrc || \
echo 'eval "$(register-python-argcomplete forest)"' >> ~/.bashrc
```

### Configure the ROS domain

The CONCERT onboard subnet uses ROS domain ID `100`.

```bash
grep -qxF 'export ROS_DOMAIN_ID=100' ~/.bashrc || \
echo 'export ROS_DOMAIN_ID=100' >> ~/.bashrc
```

Reload the shell configuration:

```bash
source ~/.bashrc
```

Verify the result:

```bash
echo "$ROS_DOMAIN_ID"
```

Expected output:

```text
100
```

## Installing additional dependencies

> [!IMPORTANT]
> Installing the latest version of MoveIt2 requires geometric_shapes to be version 2.3.4. Since we use the same dependency, to complain with MoveIt2 we have to update it before building other packages.

Install the additional ROS package:

```bash
sudo apt install -y \
    ros-jazzy-geometric-shapes \
    ros-jazzy-random-numbers 
```

The RTAB-Map packages should normally be installed later through the Forest recipes. If they are missing, install them manually:

```bash
sudo apt install -y \
    ros-jazzy-rtabmap-odom \
    ros-jazzy-rtabmap-slam
```

## Building the workspace

Move to the workspace:

```bash
cd /home/user/xbot2_ws
```

Build the required Forest projects:

```bash
forest grow concert_description -j10
forest grow concert_localization -j10
forest grow concert_navigation -j10
forest grow concert_config -j10
forest grow hdl_localization -j10
forest grow centauro_cartesio -j10
forest grow cartesio_collision_support -j10
```

## Gazebo simulation configuration

Gazebo must be able to locate models and resources installed in the workspace.

Add the following line to `~/.bashrc`:

```bash
grep -qxF 'export GZ_SIM_RESOURCE_PATH=/home/user/xbot2_ws/install/share:$GZ_SIM_RESOURCE_PATH' ~/.bashrc || \
echo 'export GZ_SIM_RESOURCE_PATH=/home/user/xbot2_ws/install/share:$GZ_SIM_RESOURCE_PATH' >> ~/.bashrc
```

Reload the shell:

```bash
source ~/.bashrc
```

Verify the variable:

```bash
echo "$GZ_SIM_RESOURCE_PATH"
```

## Intel RealSense installation

The following procedure was valid on July 16, 2026.

The upstream installation instructions are maintained in the `librealsense` repository:

```text
https://github.com/realsenseai/librealsense/blob/master/doc/distribution_linux.md
```

### Install the RealSense SDK

> [!CAUTION]
> **Before installation disconnect the RealSense device.**

Create the APT keyring directory:

```bash
# Ensure the directory exists
sudo mkdir -p /etc/apt/keyrings

# Download and dearmor
curl -sSf https://librealsense.realsenseai.com/Debian/librealsenseai.asc | \
gpg --dearmor | sudo tee /etc/apt/keyrings/librealsenseai.gpg > /dev/null
```

Install HTTPS support for APT:

```bash
sudo apt-get install -y apt-transport-https
```

Add the RealSense repository:

```bash
echo "deb [signed-by=/etc/apt/keyrings/librealsenseai.gpg] https://librealsense.realsenseai.com/Debian/apt-repo `lsb_release -cs` main" | \
sudo tee /etc/apt/sources.list.d/librealsense.list
sudo apt-get update
```

Install the RealSense packages:

```bash
sudo apt-get install -y \
    librealsense2-dkms \
    librealsense2-utils
```

After installation:

1. Reconnect the device.
2. Verify that it is detected using

```bash
rs-enumerate-devices
```

The command should display information about the connected camera.

## Installing the ROS 2 RealSense driver

Install the ROS 2 packages:

```bash
sudo apt install -y \
    ros-jazzy-realsense2-camera \
    ros-jazzy-diagnostic-updater
```

Launch the camera driver:

```bash
ros2 launch realsense2_camera rs_launch.py
```

Verify that the node is running.

## Device access troubleshooting

When the camera is visible on the host but not inside the container, verify that the required devices are exposed through `compose.yaml`.

For example:

```yaml
services:
  robot-nvidia:
    volumes:
      - /dev:/dev
```

Then recreate the container:

```bash
docker compose -p defection up -d --force-recreate robot-nvidia
```

Also verify device permissions inside the container:

```bash
ls -l /dev/video*
lsusb
```

Depending on the configuration, the container may need access to groups such as:

```text
video
plugdev
```
