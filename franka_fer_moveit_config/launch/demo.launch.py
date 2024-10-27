from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription

def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("fer", package_name="franka_fer_moveit_config").to_moveit_configs()
    description = generate_demo_launch(moveit_config)
    description.add_action(IncludeLaunchDescription(PathJoinSubstitution([FindPackageShare('franka_gripper'), 'launch', 'gripper.launch.py']),
                                    launch_arguments={
                                        'arm_id' : 'fer',
                                        'robot_ip': 'None',
                                        'use_fake_hardware' : 'true'}.items()))
    return description

