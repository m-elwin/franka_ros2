""" Set parameters necessary to configure moveit and associated nodes
    to work with the franka panda robot

    Parameters Set:
    robot_description
    robot_description_semantic
    ompl parameters
    kinematics.yaml parameters
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import SetParameter, SetParametersFromFile
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    """Description will contain a SetParameter actions that set the appropriate parameters"""

    return LaunchDescription([
        DeclareLaunchArgument("robot_ip", description="IP Address of the Franka Robot"),
        DeclareLaunchArgument("use_fake_hardware", default_value="false",  description="Use fake hardware rather than the real robot"),
        DeclareLaunchArgument("fake_sensor_commands", default_value="false", description="Use fake sensor data, only valid if use_fake_hardware is true"),

        SetParameter(name="robot_description",
                     value=Command([FindExecutable(name="xacro"), " ",
                                   PathJoinSubstitution([FindPackageShare("franka_description"), "robots", "panda_arm.urdf.xacro"]),
                                   " hand:=true",
                                   " robot_ip:=", LaunchConfiguration("robot_ip"),
                                   " use_fake_hardware:=", LaunchConfiguration("use_fake_hardware"),
                                   " fake_sensor_commands:=", LaunchConfiguration("fake_sensor_commands")
                                    ]),
                     ),

        SetParameter(name="robot_description_semantic",
                     value=Command([FindExecutable(name="xacro"), " ",
                                   PathJoinSubstitution([FindPackageShare("franka_moveit_config"), "srdf", "panda_arm.srdf.xacro"]),
                                   " hand:=true"])
                     ),

        SetParametersFromFile(filename=PathJoinSubstitution([FindPackageShare("franka_moveit_config"), "config", "kinematics.yaml"])),

        SetParameter(name='move_group', value=
                     {
                         'planning_plugin': 'ompl_interface/OMPLPlanner',
                         'request_adapters': 'default_planner_request_adapters/AddTimeOptimalParameterization '
                                             'default_planner_request_adapters/ResolveConstraintFrames '
                                             'default_planner_request_adapters/FixWorkspaceBounds '
                                             'default_planner_request_adapters/FixStartStateBounds '
                                             'default_planner_request_adapters/FixStartStateCollision '
                                             'default_planner_request_adapters/FixStartStatePathConstraints',
                        'start_state_max_bounds_error': 0.1,
                     }),

        SetParametersFromFile(filename=PathJoinSubstitution([FindPackageShare("franka_moveit_config"), "config", "ompl_planning.yaml"]))

        ])
