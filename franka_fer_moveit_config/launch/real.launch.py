"""Launchfile for the real robot. Does not start Rviz by default"""

from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # TODO: Need to override the xacro arguments before building the config.  this is done by
    # Calling .robot_description() and explicitly passing it mappings that make it use the real robot.
    # Might also take some work to get the controllers loaded properly (although I think changes in the URDF automatically do that once we
    # generate a URDF for the real robot.)
    # Need to also pass in robot_ip, possibly to the move_group node
    # Goal is to run demo mode on real robot,
    # But also provide a simple setup where we can load a moveit_py node instead of the default move_Group node.
    moveit_config = (
        MoveItConfigsBuilder("fer", package_name="franka_fer_moveit_config").
        robot_description(mapppings={"hand" : "true",
                                     "use_fake_hardware" : "false",
                                     "fake_sensor_commands" : "false",
                                     "ros2_control" : "true",
                                     "robot_ip" : LaunchConfiguration("robot_ip")}).to_moveit_configs()
        )
    description = generate_demo_launch(moveit_config)
    description.add_action(DeclareLaunchArgument("robot_ip", description="URL or ip address for the robot."))
    # We need to start the gripper separately because it is not implemented as a ROS 2 controller, but rather is a separate node
    description.add_action(IncludeLaunchDescription(PathJoinSubstitution([FindPackageShare('franka_gripper'), 'launch', 'gripper.launch.py']),
                                    launch_arguments={
                                        'arm_id' : 'fer',
                                        'robot_ip': LaunchConfiguration("robot_ip"),
                                        'use_fake_hardware' : 'false'}.items()))
    # We need a joint_state_publisher to unify the joint states from the gripper and the arm
    description.add_action(
        Node(package='joint_state_publisher',
             executable='joint_state_publisher',
             parameters=[{'source_list': ['joint_state_broadcaster/joint_states', 'fer_gripper/joint_states'], 'rate': 30}]))
    return description

