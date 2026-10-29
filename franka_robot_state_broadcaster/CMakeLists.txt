cmake_minimum_required(VERSION 3.16)
project(franka_robot_state_broadcaster)

if(NOT CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

option(CHECK_TIDY "Adds clang-tidy tests" OFF)

find_package(ament_cmake REQUIRED)
find_package(controller_interface REQUIRED)
find_package(franka_msgs REQUIRED)
find_package(franka_semantic_components REQUIRED)
find_package(generate_parameter_library REQUIRED)
find_package(pluginlib REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(rcpputils REQUIRED)
find_package(rcutils REQUIRED)
find_package(realtime_tools REQUIRED)
find_package(std_msgs REQUIRED)

generate_parameter_library(franka_robot_state_broadcaster_parameters
        src/franka_robot_state_broadcaster_parameters.yaml)

add_library(franka_robot_state_broadcaster SHARED
        src/franka_robot_state_broadcaster.cpp)

target_include_directories(franka_robot_state_broadcaster PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>)

target_link_libraries(franka_robot_state_broadcaster
        PUBLIC
            franka_robot_state_broadcaster_parameters
            controller_interface::controller_interface
            franka_msgs::franka_msgs
            franka_semantic_components::franka_semantic_components
            rclcpp_lifecycle::rclcpp_lifecycle
            realtime_tools::realtime_tools
        PRIVATE
            pluginlib::pluginlib
            rclcpp::rclcpp
            rcpputils::rcpputils
            rcutils::rcutils
            std_msgs::std_msgs)

pluginlib_export_plugin_description_file(controller_interface franka_robot_state_broadcaster.xml)


install(TARGETS franka_robot_state_broadcaster franka_robot_state_broadcaster_parameters
        EXPORT export_${PROJECT_NAME}
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin)
install(
        DIRECTORY include/
        DESTINATION include
)


if(BUILD_TESTING)
    find_package(ament_cmake_gmock REQUIRED)
    find_package(ament_cmake_clang_format REQUIRED)
    find_package(ament_cmake_copyright REQUIRED)
    find_package(ament_cmake_cppcheck REQUIRED)
    find_package(ament_cmake_flake8 REQUIRED)
    find_package(ament_cmake_lint_cmake REQUIRED)
    find_package(ament_cmake_pep257 REQUIRED)
    find_package(ament_cmake_xmllint REQUIRED)
    find_package(controller_manager REQUIRED)
    find_package(hardware_interface REQUIRED)
    find_package(ros2_control_test_assets REQUIRED)

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
        ament_clang_tidy(${CMAKE_BINARY_DIR})
    endif()

    add_rostest_with_parameters_gmock(${PROJECT_NAME}_test
        test/test_franka_robot_state_broadcaster.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/test/franka_robot_state_broadcaster_parameters.yaml)
    target_link_libraries(${PROJECT_NAME}_test
        ${PROJECT_NAME}
        controller_manager::controller_manager
        hardware_interface::hardware_interface
        ros2_control_test_assets::ros2_control_test_assets)

    ament_add_gmock(test_load_franka_robot_state_broadcaster test/test_load_franka_robot_state_broadcaster.cpp)
    target_link_libraries(test_load_franka_robot_state_broadcaster
        controller_manager::controller_manager
        hardware_interface::hardware_interface
        ros2_control_test_assets::ros2_control_test_assets)
endif()

ament_export_targets(export_${PROJECT_NAME} HAS_LIBRARY_TARGET)
ament_export_dependencies(
        controller_interface
        franka_msgs
        franka_semantic_components
        rclcpp_lifecycle
        realtime_tools)
ament_package()
