cmake_minimum_required(VERSION 3.28)
project(demo_nav2_lab)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(perception_utils_ros2 REQUIRED)
find_package(concert_description REQUIRED)
find_package(concert_mapping REQUIRED)
find_package(concert_navigation REQUIRED)

install(
  DIRECTORY mesh 
            maps
            launch
  DESTINATION share/${PROJECT_NAME}
)


ament_package()
