### Defection docker - Vision host

>[!IMPORTANT]
> As of today, the domain xbot.cloud is no more available. For this reason, once accessed the docker, you must run
> *echo "54.73.207.169 xbot.cloud" | sudo tee -a /etc/hosts*
> This should be fixed on the next docker image release since produces an error with `sudo apt update`


## General update
```bash
# Update xbot2 - as of today to update you need to remove it before as apt do not check the date but lexically the version (trust me)
sudo apt update
sudo apt purge -y xbot2_desktop_full
sudo apt autoremove -y
sudo apt install -y xbot2_desktop_full ros-jazzy-geometric-shapes
cd /home/user/xbot2_ws/recipes/multidof_recipes
git fetch
git checkout alelovato_recipes # TODO: switch back at ros2
git pull
cd /home/user/xbot2_ws/src/xbot2_gui_server
git pull # Get to last commit to remove a bug that does not allow xbot2_gui_server to run
```
You can check from (http://54.73.207.169/xbot2-nightly/ubuntu/noble/)[http://54.73.207.169/xbot2-nightly/ubuntu/noble/] that the packages version match with the latest.

## Customization
```bash
# Re-enable forest autocompile
echo 'eval "$(register-python-argcomplete forest)"' >> ~/.bashrc
echo "export ROS_DOMAIN_ID=100" >> ~/.bashrc # CONCERT subnet domain id
source ~/.bashrc

# Install other stuff
# sudo apt install -y ros-jazzy-rtabmap-odom ros-jazzy-rtabmap-slam #Should be installed by recipe
sudo apt install -y ros-jazzy-random-numbers
cd /home/user/xbot2_ws
forest grow concert_description -j10
forest grow concert_localization -j10 #TBD: add depencency to hdl_localization(?)
forest grow concert_navigation -j10
forest grow concert_config -j10
forest grow hdl_localization -j10
forest grow centauro_cartesio -j10 # Error in dependency of libxbot2_interface (loads v1.1)
forest grow cartesio_collision_support -j10 # Error in dependency of libxbot2_interface (loads v1.1)
```

If you need to run the simulation, export this line to allow gazebo finding the models:
```bash
export GZ_SIM_RESOURCE_PATH=/home/user/xbot2_ws/install/share:$GZ_SIM_RESOURCE_PATH >> ~/.bashrc
source ~/.bashrc
```


## Realsense installation
Up to the 16/07/2026, the instruction to install the realsense SDK from (https://github.com/realsenseai/librealsense/blob/master/doc/distribution_linux.md)[https://github.com/realsenseai/librealsense/blob/master/doc/distribution_linux.md] are:

```bash
# Ensure the directory exists
sudo mkdir -p /etc/apt/keyrings

# Download and dearmor
curl -sSf https://librealsense.realsenseai.com/Debian/librealsenseai.asc | \
gpg --dearmor | sudo tee /etc/apt/keyrings/librealsenseai.gpg > /dev/null
sudo apt-get install apt-transport-https
echo "deb [signed-by=/etc/apt/keyrings/librealsenseai.gpg] https://librealsense.realsenseai.com/Debian/apt-repo `lsb_release -cs` main" | \
sudo tee /etc/apt/sources.list.d/librealsense.list
sudo apt-get update
sudo apt-get install -y librealsense2-dkms librealsense2-utils
```
now unplug the realsense device and re-plug it. Running the command
```bash
rs-enumerate-devices
```
you should see some information about the reaslense conneted appearing on screen.

### Installation of ROS2 driver
```bash
sudo apt install -y ros-jazzy-realsense2-camera ros-jazzy-diagnostic-updater
```
now running
```bash
ros2 launch realsense2_camera rs_launch.py
```
you should see the running node of the camera in ros2.
