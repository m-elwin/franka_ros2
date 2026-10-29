cmake_minimum_required(VERSION 3.16)
project(integration_launch_testing)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY test
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
    find_package(ament_cmake_copyright REQUIRED)
    find_package(ament_cmake_flake8 REQUIRED)
    find_package(ament_cmake_lint_cmake REQUIRED)
    find_package(ament_cmake_pep257 REQUIRED)
    find_package(ament_cmake_xmllint REQUIRED)
    find_package(launch_testing_ament_cmake)

    ament_copyright(package.xml)
    ament_lint_cmake(CMakeLists.txt)
    ament_flake8()
    ament_pep257()
    ament_xmllint()
endif()

ament_package()