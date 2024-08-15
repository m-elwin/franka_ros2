#  Copyright (c) 2024 Franka Robotics GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# This file is an adapted version of
# https://github.com/ros-planning/moveit_resources/blob/ca3f7930c630581b5504f3b22c40b4f82ee6369d/panda_moveit_config/launch/demo.launch.py

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    Shutdown
)
from launch.conditions import UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution
)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare, ExecutableInPackage

import yaml

def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, 'r') as file:
            return yaml.safe_load(file)
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None

def generate_launch_description():


    # Planning Functionality
    ompl_planning_pipeline_config = {
        'ompl': {
            'planning_plugins': ['ompl_interface/OMPLPlanner'],
            'request_adapters': ['default_planning_request_adapters/ResolveConstraintFrames',
                                'default_planning_request_adapters/ValidateWorkspaceBounds',
                                'default_planning_request_adapters/CheckStartStateBounds',
                                'default_planning_request_adapters/CheckStartStateCollision'],
            'response_adapters': ['default_planning_response_adapters/AddTimeOptimalParameterization',
                                  'default_planning_response_adapters/ValidateSolution',
                                  'default_planning_response_adapters/DisplayMotionPath'],
            'start_state_max_bounds_error': 0.1,
        }
    }
    ompl_planning_yaml = load_yaml(
        'franka_fer_moveit_config', 'config/ompl_planning.yaml'
    )
    ompl_planning_pipeline_config['ompl'].update(ompl_planning_yaml)

#    # Trajectory Execution Functionality
#    moveit_simple_controllers_yaml = load_yaml(
#        'franka_fer_moveit_config', 'config/fer_controllers.yaml'
#    )
#    moveit_controllers = {
#        'moveit_simple_controller_manager': moveit_simple_controllers_yaml,
#        'moveit_controller_manager': 'moveit_simple_controller_manager'
#                                     '/MoveItSimpleControllerManager',
#    }
#
#    trajectory_execution = {
#        'moveit_manage_controllers': True,
#        'trajectory_execution.allowed_execution_duration_scaling': 1.2,
#        'trajectory_execution.allowed_goal_duration_margin': 0.5,
#        'trajectory_execution.allowed_start_tolerance': 0.01,
#    }

#
#    # Start the actual move_group node/action server
#    run_move_group_node = Node(
#        package='moveit_ros_move_group',
#        executable='move_group',
#        output='screen',
#        parameters=[
#            robot_description,
#            robot_description_semantic,
#            kinematics_yaml,
#            ompl_planning_pipeline_config,
#            trajectory_execution,
#            moveit_controllers,
#            planning_scene_monitor_parameters,
#        ],
#    )

    # RViz
#    rviz_base = os.path.join(get_package_share_directory(
#        'franka_fer_moveit_config'), 'rviz')
#    rviz_full_config = os.path.join(rviz_base, 'moveit.rviz')

#    rviz_node = Node(
#        package='rviz2',
#        executable='rviz2',
#        name='rviz2',
#        output='log',
#        arguments=['-d', rviz_full_config],
#        parameters=[
#            robot_description,
#            robot_description_semantic,
#            ompl_planning_pipeline_config,
#            kinematics_yaml,
#        ],
#    )



    # Load controllers
#    load_controllers = []
#    for controller in ['fer_arm_controller', 'joint_state_broadcaster']:
#        load_controllers += [
#            ExecuteProcess(
#                cmd=['ros2 run controller_manager spawner {}'.format(
#                    controller)],
#                shell=True,
#                output='screen',
#            )
#        ]


#    franka_robot_state_broadcaster = Node(
#        package='controller_manager',
#        executable='spawner',
#        arguments=['franka_robot_state_broadcaster'],
#        output='screen',
#        condition=UnlessCondition(use_fake_hardware),
#    )


#    gripper_launch_file = IncludeLaunchDescription(
#        PythonLaunchDescriptionSource([PathJoinSubstitution(
#            [FindPackageShare('franka_gripper'), 'launch', 'gripper.launch.py'])]),
#        launch_arguments={'robot_ip': robot_ip,
#                          use_fake_hardware_parameter_name: use_fake_hardware}.items(),
#    )
    robot_description = ParameterValue(Command([ExecutableInPackage("xacro", "xacro"), " ",
                                                PathJoinSubstitution([FindPackageShare("franka_description"), "robots", "fer", "fer.urdf.xacro"]),
                                                ' hand:=true',
                                                ' robot_ip:=', LaunchConfiguration('robot_ip'),
                                                ' use_fake_hardware:=',LaunchConfiguration('use_fake_hardware'),
                                                ' fake_sensor_commands:=',LaunchConfiguration('fake_sensor_commands'),
                                                ' ros2_control:=true']),value_type=str)
    robot_description_semantic = ParameterValue(Command([ExecutableInPackage("xacro", "xacro"), ' ',
                                                        PathJoinSubstitution([FindPackageShare('franka_fer_moveit_config'),'srdf','fer_arm.srdf.xacro'])])
                                               , value_type=str)
    return LaunchDescription(
        [ DeclareLaunchArgument('robot_ip', description='Hostname or IP address of the robot.')
         ,DeclareLaunchArgument('use_fake_hardware', default_value='false',description='Use fake hardware')
         ,DeclareLaunchArgument('fake_sensor_commands', default_value='false', description='Fake sensor commands. Only valid when "use_fake_hardware" == true')
         ,DeclareLaunchArgument('db', default_value='False', description='Database flag')
#        rviz_node,
         ,Node(package='robot_state_publisher',
              executable='robot_state_publisher',
              name='robot_state_publisher',
              output='both',
              parameters=[{'robot_description': robot_description}]
            )
          ,Node(package='controller_manager',
                executable='ros2_control_node',
                parameters=[PathJoinSubstitution([FindPackageShare('franka_fer_moveit_config'), 'config', 'fer_ros_controllers.yaml'])],
                remappings=[('joint_states', 'franka/joint_states')],
                output='screen',
                on_exit=Shutdown(),
                )
          ,Node(package='joint_state_publisher',
                executable='joint_state_publisher',
                parameters=[{'source_list': ['franka/joint_states', 'fer_gripper/joint_states'], 'rate': 30}],
          )
          ,Node(package="moveit_ros_move_group",
                executable="move_group",
                output="screen",
                parameters=[
                    {'publish_robot_description_semantic': True,
                     'allow_trajectory_execution' : True,
                     'publish_planning_scene': True,
                     'publish_state_updates': True,
                     'publish_transforms_updates': True,
                     'monitor_dynamics': False,
                     'robot_description': robot_description,
                     'robot_description_semantic': robot_description_semantic,
                     },
                    load_yaml('franka_fer_moveit_config', 'config/kinematics.yaml'),
                    ompl_planning_pipeline_config,
                    {'default_planning_pipeline': 'ompl'},
                    {'planning_pipelines': ['ompl']}
                ]
          )
#         franka_robot_state_broadcaster,
#         gripper_launch_file
         ]
#        + load_controllers
    )
