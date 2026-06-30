# Command execution to bring up concert demo

To maintain division, the CONCERT on board sub-network has ROS_DOMAIN_ID 100, whereas PILOT has ID 77. This is because the automatic discovery did't work.

## Preliminaries
- Turn on the robot pushing the two buttons, firstly press (not hold) the button closer to the middle of the robot, and then the other. At this point CONCERT should start turning on (white light on).

- When ready to start everything, press the dead man button (emergency) and the green light on the robot should turn on.

### Embedded PC - XBOT2 and Ecat
In the Embedded PC (ip 10.24.10.100, you can access via the command ssh_embedded) you have to launch on 3 separate terminal:
'''bash
# Turn on Ecat master
repl -f /home/user/data/forest_ws/src/concert_config/ecat/ecat_config.yaml
'''

'''bash
# Turn on XBot2 Core
xbot2-core --hw ec_imp -C /home/user/data/forest_ws/src/concert_config/ModularBot.yaml
'''

'''bash
# Turn on connection for Xbot2 on the tablet
# Make sure to connect on ip 10.24.10.1000 and port 8080
xbot2_gui_server
'''

### Control - Back lidar and Imu
On the Control PC (ip 10.24.10.102) open two terminals and run the following commands to bring up IMU (Vectornav) and back VLP lidar

ros2 launch vectornav vectornav.launch.py
ros2 launch concert_config velodyne-VLP16_back.launch.py


## Vision
ros2 launch concert_config velodyne-VLP16_front.launch.py
zenoh_dds2_bridge

## Pilot
zenoh_dds2_bridge <ip pilot>

## SLAM
On **Vision** mkae sure to be on branch master of concert_localization and branch test_alelovato of concert_navigation
ros2 launch concert_localization rtabmap.launch.py

## LOCALIZATION
On **Vision** mkae sure to be on branch master of concert_localization
ros2 launch concert_localization localization.launch.py map_file:=/path/to/map

> Note: Usually, if you are using rtabmap.launch.py to collect the PCD file, you'll find the .pcd file under current_dir/maps

## NAVIGATION
On **Vision** mkae sure to be on branch test_alelovato of concert_navigation
ros2 launch concert_localization navigation.launch.py map_file:=/path/to/map.yaml

> Note: To convert the PCD into Nav2 maps, you can use 'ros2 launch pcd_to_nav2_map.launch.py map_file:=/path_to_pcd_file' and will save a folder with the .pgm and .yaml of the converted maps. You can use params to set the height.