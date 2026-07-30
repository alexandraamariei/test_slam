import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_path = get_package_share_directory('turtlebot_description')
    xacro_file = os.path.join(pkg_path, 'urdf', 'robot.urdf.xacro') # sau .urdf
    
    # Transformăm xacro în xml dacă este cazul
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    # 1. Nodul obligatoriu care publică base_link și restul pieselor
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}]
    )
    # 3. Porniți Gazebo Harmonic
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # 4. Spawnați robotul în Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'turtlebot_burger',
                   '-z', '0.1'], # Îl lansăm puțin deasupra solului
        output='screen'
    )

  # 5. Puntea (Bridge) între ROS 2 și Gazebo
    bridge = Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
                # LINIA NOUĂ CARE REZOLVĂ ERORILE CU ROȘU PENTRU ROȚI:
                '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model'
            ],
            output='screen'
        )
    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        spawn_entity,
        bridge
    ])