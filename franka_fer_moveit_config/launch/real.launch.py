"""Launchfile for the real robot. Does not start Rviz by default"""

from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.conditions import IfCondition

def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("fer", package_name="franka_fer_moveit_config").
        robot_description(mappings={"hand" : "true",
                                     "use_fake_hardware" : "false",
                                     "fake_sensor_commands" : "false",
                                     "ros2_control" : "true",
                                     "robot_ip" : LaunchConfiguration("robot_ip")}).to_moveit_configs()
        )
    return LaunchDescription([
        DeclareLaunchArgument("robot_ip", description="URL or ip address for the robot."),
        DeclareLaunchArgument("use_rviz", default_value="false", description="Set to True to use Rviz"),
        # We need to start the gripper separately because it is not implemented as a ROS 2 controller, but rather is a separate node
        IncludeLaunchDescription(PathJoinSubstitution([FindPackageShare('franka_gripper'), 'launch', 'gripper.launch.py']),
                                 launch_arguments={
                                     'arm_id' : 'fer',
                                     'robot_ip': LaunchConfiguration("robot_ip"),
                                     'use_fake_hardware' : 'false'}.items()),
        IncludeLaunchDescription(PathJoinSubstitution([FindPackageShare('franka_fer_moveit_config'),'launch','rsp.launch.py'])),
        IncludeLaunchDescription(PathJoinSubstitution([FindPackageShare('franka_fer_moveit_config'),'launch','move_group.launch.py'])),
        IncludeLaunchDescription(PathJoinSubstitution([FindPackageShare('franka_fer_moveit_config'),'launch','moveit_rviz.launch.py']),
                                 condition=IfCondition(LaunchConfiguration('use_rviz'))),
        Node(package="controller_manager",
             executable="ros2_control_node",
             parameters=[PathJoinSubstitution([FindPackageShare('franka_fer_moveit_config'),'config','fer_real_controllers.yaml'])],
             remappings=[("/controller_manager/robot_description", "/robot_description")],),
        IncludeLaunchDescription(PathJoinSubstitution([FindPackageShare('franka_fer_moveit_config'),'launch','spawn_controllers.launch.py']))
        ])

    return description

