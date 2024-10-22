cmake_minimum_required(VERSION 3.10)
project(BlobMasses)

add_executable(v2 v2.cpp)

set(OPENCV_INCLUDE_DIR /opt/homebrew/Cellar/opencv/4.9.0_7/include/opencv4)
set(OPENCV_LIB_DIR /opt/homebrew/Cellar/opencv/4.9.0_7/lib/)

message(STATUS "OpenCV library path: ${OPENCV_LIB_DIR}")

# set include directory
target_include_directories(v2 PUBLIC "${OPENCV_INCLUDE_DIR}")

# set library directory
target_link_directories(v2 PUBLIC "${OPENCV_LIB_DIR}")

# link specific object files we need
# target_link_libraries(write_text opencv_imgcodecs opencv_core opencv_imgproc)
target_link_libraries(v2 opencv_core opencv_imgproc opencv_highgui opencv_imgcodecs)

set(CMAKE_CXX_FLAGS "-Wall -std=c++11")