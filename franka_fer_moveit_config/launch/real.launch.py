"""Launchfile for the real robot. Does not start Rviz by default."""

from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_rsp_launch, generate_move_group_launch, generate_moveit_rviz_launch, generate_spawn_controllers_launch
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.conditions import IfCondition

# TODO: This is a temporary fix until moveit_configs_utils.launches.generate_spawn_controllers_launch provides a method
# To do an --switch-asap or the controller is written in a way that does not require it
# When replaced it will be imported with generate_spawn_controllers_launch
def PATCH_generate_spawn_controllers_launch(moveit_config):
    controller_names = moveit_config.trajectory_execution.get(
        "moveit_simple_controller_manager", {}
    ).get("controller_names", [])
    ld = LaunchDescription()
    for controller in controller_names + ["joint_state_broadcaster"]:
        ld.add_action(
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[controller, '--switch-asap'],
                output="screen",
            )
        )
    return ld
def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("fer", package_name="franka_fer_moveit_config").
        robot_description(mappings={"hand" : "true",
                                    "use_fake_hardware" : "false",
                                    "fake_sensor_commands" : "false",
                                    "ros2_control" : "true",
                                    "robot_ip" : LaunchConfiguration("robot_ip")}).to_moveit_configs()
    )
    return LaunchDescription(generate_rsp_launch(moveit_config).entities
    + generate_move_group_launch(moveit_config).entities
    + PATCH_generate_spawn_controllers_launch(moveit_config).entities
    + [DeclareLaunchArgument("robot_ip", description="URL or ip address for the robot."),
       DeclareLaunchArgument("use_rviz", default_value="False", description="To use rviz, set to true."),
       IncludeLaunchDescription(PathJoinSubstitution([FindPackageShare('franka_fer_moveit_config'), 'launch', 'moveit_rviz.launch.py']),
                                condition=IfCondition(LaunchConfiguration('use_rviz'))),
      # We need to start the gripper separately because it is not implemented as a ROS 2 controller, but rather is a separate node
        IncludeLaunchDescription(PathJoinSubstitution([FindPackageShare('franka_gripper'), 'launch', 'gripper.launch.py']),
                                 launch_arguments={
                                     'arm_id' : 'fer',
                                     'robot_ip': LaunchConfiguration("robot_ip"),
                                     'use_fake_hardware' : 'false'}.items()),
    Node(package="controller_manager",
         executable="ros2_control_node",
         parameters=[PathJoinSubstitution([FindPackageShare('franka_fer_moveit_config'),'config','fer_real_controllers.yaml'])],
         remappings=[("/controller_manager/robot_description", "/robot_description")],),
    Node(package='joint_state_publisher',
         executable='joint_state_publisher',
         parameters=[{'source_list': ['joint_state_broadcaster/joint_states', 'fer_gripper/joint_states'], 'rate': 1000}])
    ])

