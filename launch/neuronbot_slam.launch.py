import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    # Get the package directories.
    neuronbot_gazebo_dir = get_package_share_directory('neuronbot2_gazebo')
    slam_asgmt_dir = get_package_share_directory('ros2_slam_multimap')

    # Create the launch configuration variables.
    gui = LaunchConfiguration('gui')
    world_pkg = LaunchConfiguration('world_pkg')
    world_file = LaunchConfiguration('world_file')

    # Declare the launch arguments.
    declare_gui_cmd = DeclareLaunchArgument(
        'gui', 
        default_value='true',
        description='Flag to enable or disable the Gazebo 3D window.'
    )
    
    declare_world_pkg_cmd = DeclareLaunchArgument(
        'world_pkg', 
        default_value='turtlebot3_gazebo',
        description='The ROS 2 package where the map is located.'
    )
    
    declare_world_file_cmd = DeclareLaunchArgument(
        'world_file', 
        default_value='turtlebot3_house.world',
        description='The exact name of the .world file.'
    )
    
    # Dynamically build the path to the world file using substitutions.
    world_path = PathJoinSubstitution([
        FindPackageShare(world_pkg),
        'worlds',
        world_file
    ])

    
    # Include the Gazebo simulation launch file.
    include_gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(neuronbot_gazebo_dir, 'launch', 'neuronbot2_world.launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'world': world_path,
            'gui': gui
        }.items()
    )
    
    # Start the SLAM Toolbox node.
    slam_params_file = os.path.join(slam_asgmt_dir, 'config', 'neuronbot_params.yaml')
    
    start_slam_toolbox_cmd = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            slam_params_file,
            {'use_sim_time': True}
        ]
    )

    # Start RViz2 for visualization.
    start_rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    # Create and populate the launch description.
    ld = LaunchDescription()

    # Add the launch arguments.
    ld.add_action(declare_gui_cmd)
    ld.add_action(declare_world_pkg_cmd)
    ld.add_action(declare_world_file_cmd)

    # Add the nodes and includes.
    ld.add_action(include_gazebo_cmd)
    ld.add_action(start_slam_toolbox_cmd)
    ld.add_action(start_rviz_cmd)

    return ld
