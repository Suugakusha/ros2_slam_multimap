
# ROS2 Humble 2D SLAM Multimap Integration

## Overview
This repository contains a ROS2 Humble setup for a 2D SLAM application. It integrates the NeuronBot2 mobile robot, equipped with a 2D LiDAR, into the Gazebo simulation environment to generate a specified 2D map using `slam_toolbox`. It supports multiple explorable maps: TurtleBot3 House (default), NeuronBot2 Mememan and Phoenix maps. I built this on Ubuntu 22.04 LTS, the recommended version for ROS2 Humble.

## Setup Instructions
0. [Have or install ROS2 Humble on your system](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html), and install standard build tools 
`sudo apt install python3-colcon-common-extensions python3-vcstool python3-rosdep`.

1. Create a ROS2 workspace, clone the repository above, and source your terminal:
   `mkdir -p ~/[dir name]/src`
   `cd ~/[dir name]/src`
   `git clone https://github.com/Suugakusha/ros2_slam_multimap.git`
   `source /opt/ros/humble/setup.bash`
   
2. Import external repositories in your workspace repository.
`cd ~/[dir name]`
`vcs import src < src/ros2_slam_multimap/ros2.repos`

4. Install all necessary ROS2 dependencies for the cloned packages: 
   (You can skip `sudo rosdep init` if you've already done it before).
   `sudo rosdep init` 
   `rosdep update`
   `rosdep install --from-paths src --ignore-src -r -y`
   
5. The NeuronBot2 launch file doesn't handle dynamic world loading well so replace it with a patched version provided in the `patch/` folder:
`cp src/ros2_slam_multimap/patch/neuronbot2_world.launch.py src/neuronbot2/neuronbot2_gazebo/launch/neuronbot2_world.launch.py`

6. Build the workspace using `colcon build --symlink-install`.

7. Source your workspace with `source install/setup.bash`.

## Launching the Simulation
To launch the robot, the Gazebo environment, and the SLAM node simultaneously, run:

- **Default TurtleBot3 House:**
  `ros2 launch ros2_slam_multimap neuronbot_slam.launch.py`

- **Specify a Custom Map:**
  `ros2 launch ros2_slam_multimap neuronbot_slam.launch.py world_pkg:=[package name] world_file:=[world name]`

- **Included NeuronBot2 Maps:**
  NeuronBot2 provides 2 basic maps (`mememan_world` and `phenix_world`). To load them:
  `ros2 launch ros2_slam_multimap neuronbot_slam.launch.py world_pkg:=neuronbot2_gazebo world_file:=mememan_world.model` 
  `ros2 launch ros2_slam_multimap neuronbot_slam.launch.py world_pkg:=neuronbot2_gazebo world_file:=phenix_world.model`

**If you're running a Virtual Machine:**
Running in a VM with limited VRAM, Gazebo may freeze while loading high detail maps. It's better to run Gazebo in headless mode (no 3D Gazebo GUI, just RViz):
`ros2 launch rros2_slam_multimap neuronbot_slam.launch.py gui:=false`

