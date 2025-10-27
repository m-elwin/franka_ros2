# Northwestern MSR Fork Changes
This is a fork of franka_ros, designed to work with the original FER (formerly panda robots) on ROS 2 kilted.

1. It uses a [fork of libfranka](https://github.com/m-elwin/libfranka) that matches functionality in 
libfranka 0.13.3 but for the old Panda robot. 

2. It tries to track the latest franka_ros, but without needing to update libfranka beyond 0.13.3

3. Currently, franka_example_controllers and franka_semantic_components are up-to-date with v3.0.0 of franka_ros2,
with minimal modifications for working with ROS 2 kitled (due mainly to ROS 2 control API changes)

4. Other packages most recently branched from franka_ros2 0.15.1, but they still work. Maybe these will be upgraded later.

# ROS 2 integration for Franka Robotics research robots

[![CI](https://github.com/frankaemika/franka_ros2/actions/workflows/ci.yml/badge.svg)](https://github.com/frankaemika/franka_ros2/actions/workflows/ci.yml)

See the [Franka Control Interface (FCI) documentation][fci-docs] for more information.

## License

All packages of `franka_ros2` are licensed under the [Apache 2.0 license][apache-2.0].

[apache-2.0]: https://www.apache.org/licenses/LICENSE-2.0.html

[fci-docs]: https://frankaemika.github.io/docs
