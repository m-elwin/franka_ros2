cmake_minimum_required(VERSION 3.16)
project(franka_semantic_components)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

option(CHECK_TIDY "Adds clang-tidy tests" OFF)

find_package(ament_cmake REQUIRED)
find_package(Franka 0.13.0 REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(franka_hardware REQUIRED)
find_package(franka_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(controller_interface REQUIRED)
find_package(rclcpp REQUIRED)
find_package(urdf REQUIRED)

add_library(franka_semantic_components SHARED
  src/franka_robot_state.cpp
  src/franka_robot_model.cpp
  src/franka_cartesian_velocity_interface.cpp
  src/franka_cartesian_pose_interface.cpp
  src/franka_semantic_component_interface.cpp
  src/translation_utils.cpp)

target_include_directories(franka_semantic_components PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)

target_link_libraries(franka_semantic_components
  PUBLIC
    Franka::Franka
    Eigen3::Eigen
    franka_hardware::franka_hardware
    franka_msgs::franka_msgs
    geometry_msgs::geometry_msgs
    sensor_msgs::sensor_msgs
    hardware_interface::hardware_interface
    controller_interface::controller_interface
    urdf::urdf
  PRIVATE
    std_msgs::std_msgs
    rclcpp::rclcpp)

install(TARGETS franka_semantic_components
  EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)

if(BUILD_TESTING)
  find_package(ament_cmake_clang_format REQUIRED)
  find_package(ament_cmake_copyright REQUIRED)
  find_package(ament_cmake_cppcheck REQUIRED)
  find_package(ament_cmake_flake8 REQUIRED)
  find_package(ament_cmake_lint_cmake REQUIRED)
  find_package(ament_cmake_pep257 REQUIRED)
  find_package(ament_cmake_xmllint REQUIRED)
  find_package(ament_cmake_gmock REQUIRED)

  set(CPP_DIRECTORIES src include)
  ament_clang_format(CONFIG_FILE ../.clang-format ${CPP_DIRECTORIES})
  ament_copyright(${CPP_DIRECTORIES} package.xml)
  ament_cppcheck(${CPP_DIRECTORIES})
  ament_lint_cmake(CMakeLists.txt)
  ament_flake8()
  ament_pep257()
  ament_xmllint()
  if(CHECK_TIDY)
    find_package(ament_cmake_clang_tidy REQUIRED)
    set(ament_cmake_clang_tidy_CONFIG_FILE ../.clang-tidy)
    ament_clang_tidy(${CMAKE_BINARY_DIR} --jobs 6)
  endif()

  ament_add_gmock(test_franka_robot_state test/franka_robot_state_test.cpp)
  target_link_libraries(test_franka_robot_state franka_semantic_components)

  ament_add_gmock(test_franka_robot_model test/franka_robot_model_test.cpp)
  target_link_libraries(test_franka_robot_model franka_semantic_components)

  ament_add_gmock(franka_semantic_component_interface_test
    test/franka_semantic_interface_test.cpp)
  target_link_libraries(franka_semantic_component_interface_test franka_semantic_components)

  ament_add_gmock(franka_cartesian_velocity_interface_test
    test/franka_cartesian_velocity_interface_test.cpp)
  target_link_libraries(franka_cartesian_velocity_interface_test franka_semantic_components)

  ament_add_gmock(franka_cartesian_pose_interface_test
    test/franka_cartesian_pose_interface_test.cpp)
  target_link_libraries(franka_cartesian_pose_interface_test franka_semantic_components)

  install(FILES test/robot_description_test.txt
          DESTINATION share/${PROJECT_NAME})
endif()

ament_export_targets(export_${PROJECT_NAME} HAS_LIBRARY_TARGET)
ament_export_dependencies(
  Franka
  Eigen3
  franka_hardware
  franka_msgs
  geometry_msgs
  sensor_msgs
  hardware_interface
  controller_interface
  urdf)
ament_package()
