cmake_minimum_required(VERSION 3.16)
project(franka_hardware)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

option(CHECK_TIDY "Adds clang-tidy tests" OFF)

find_package(ament_cmake REQUIRED)
find_package(Franka 0.13.2 REQUIRED)
find_package(fmt REQUIRED)
find_package(franka_msgs REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)

add_library(franka_hardware SHARED
        src/franka_action_server.cpp
        src/franka_hardware_interface.cpp
        src/robot.cpp
        src/franka_param_service_server.cpp
        src/franka_executor.cpp
)

target_include_directories(franka_hardware PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>)

target_link_libraries(franka_hardware
        PUBLIC
            Franka::Franka
            franka_msgs::franka_msgs
            hardware_interface::hardware_interface
            rclcpp::rclcpp
            rclcpp_action::rclcpp_action
            rclcpp_lifecycle::rclcpp_lifecycle
        PRIVATE
            fmt::fmt
            pluginlib::pluginlib)

pluginlib_export_plugin_description_file(hardware_interface franka_hardware.xml)


install(TARGETS franka_hardware
        EXPORT export_${PROJECT_NAME}
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin)
install(
        DIRECTORY include/
        DESTINATION include
)

if(BUILD_TESTING)
    find_package(ament_cmake_clang_format REQUIRED)
    find_package(ament_cmake_copyright REQUIRED)
    find_package(ament_cmake_cppcheck REQUIRED)
    find_package(ament_cmake_flake8 REQUIRED)
    find_package(ament_cmake_lint_cmake REQUIRED)
    find_package(ament_cmake_pep257 REQUIRED)
    find_package(ament_cmake_xmllint REQUIRED)

    set(CPP_DIRECTORIES src include)
    ament_clang_format(CONFIG_FILE ../.clang-format ${CPP_DIRECTORIES})
    ament_copyright(${CPP_DIRECTORIES} package.xml)
    ament_cppcheck(${CPP_DIRECTORIES})
    ament_lint_cmake(CMakeLists.txt)
    ament_flake8()
    ament_pep257()
    ament_xmllint()

    add_subdirectory(test)

    if(CHECK_TIDY)
        find_package(ament_cmake_clang_tidy REQUIRED)
        set(ament_cmake_clang_tidy_CONFIG_FILE ../.clang-tidy)
        ament_clang_tidy(${CMAKE_BINARY_DIR})
    endif()
endif()

ament_export_targets(export_${PROJECT_NAME} HAS_LIBRARY_TARGET)
ament_export_dependencies(
        Franka
        franka_msgs
        hardware_interface
        rclcpp
        rclcpp_action
        rclcpp_lifecycle)
ament_package()
