cmake_minimum_required(VERSION 3.0.0)
project(progetto_lampioni VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
enable_testing()

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
message(STATUS "OpenCV_LIBS: ${OpenCV_LIBS}")

add_executable(progetto_lampioni main.cpp)

target_link_libraries(progetto_lampioni ${OpenCV_LIBS})


set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
