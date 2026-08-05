import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    # 1. Declarăm parametrul magic: use_sim_time (True = Gazebo, False =  Real)
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Folosesc timpul din simulare daca sunt in Gazebo'
    )

    # 2. Găsesc pachetul cu descrierea robotului (URDF-ul)
    turtlebot_desc_dir = get_package_share_directory('turtlebot_description')

    # 3. Lansarea pentru Simulare
    gazebo_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot_desc_dir, 'launch', 'sim.launch.py')
        ),
        condition=IfCondition(use_sim_time)
    )

    # 4. Lansarea pentru Hardware Real
    # (Aici pun micro_ros_agent, driverul de Lidar real, etc.)
    #     PythonLaunchDescriptionSource(
    #         os.path.join(turtlebot_desc_dir, 'launch', 'real_hardware.launch.py')
    #     ),
    #     condition=UnlessCondition(use_sim_time)
    # )

    # 5. trimit către ROS 2
    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(gazebo_sim_launch)
    


    return ld