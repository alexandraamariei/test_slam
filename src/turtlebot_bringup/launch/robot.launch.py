import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    # 1. Declarăm parametrul magic: use_sim_time (True = Gazebo, False = Hardware Real)
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Foloseste timpul din simulare daca esti in Gazebo'
    )

    # 2. Căutăm pachetul nostru de descriere (cel vechi, cu URDF-ul)
    turtlebot_desc_dir = get_package_share_directory('turtlebot_description')

    # 3. Definim ce se lansează DACA suntem in SIMULARE (use_sim_time = true)
    # Aici chemăm fișierul tău existent sim.launch.py
    gazebo_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot_desc_dir, 'launch', 'sim.launch.py')
        ),
        condition=IfCondition(use_sim_time)
    )

    # 4. Definim ce se lansează DACA suntem pe HARDWARE REAL (use_sim_time = false)
    # Deocamdată nu avem fișierele reale, așa că le lăsăm pregătite teoretic
    # (Aici vom pune micro_ros_agent, driverul de Lidar real, etc.)
    # real_hardware_launch = IncludeLaunchDescription(...) 

    # 5. Împachetăm totul și trimitem către ROS 2
    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(gazebo_sim_launch)
    
    # Când vom avea hardware-ul:
    # ld.add_action(real_hardware_launch)

    return ld