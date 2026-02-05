# Example CMakeLists.txt showing how to use PackageVersions
#
# This example demonstrates how to integrate the PackageVersions repository
# into your CMake project to ensure consistent dependency versions.

cmake_minimum_required(VERSION 3.12)
project(ExampleProject)

# Option 1: If PackageVersions is a subdirectory or submodule
# include(PackageVersions/PackageVersions.cmake)
# load_package_versions("${CMAKE_CURRENT_SOURCE_DIR}/PackageVersions/versions.json")

# Option 2: If you want to manually specify the path
# include(/path/to/PackageVersions/PackageVersions.cmake)
# load_package_versions("/path/to/PackageVersions/versions.json")

# Option 3: Direct Python script usage (without CMake module)
# This example shows how to get GoogleTest version directly

find_package(Python3 COMPONENTS Interpreter REQUIRED)

execute_process(
    COMMAND ${Python3_EXECUTABLE} get_version.py get googletest --field version
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    OUTPUT_VARIABLE GOOGLETEST_VERSION
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

execute_process(
    COMMAND ${Python3_EXECUTABLE} get_version.py get googletest --field repository
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    OUTPUT_VARIABLE GOOGLETEST_REPO
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

message(STATUS "GoogleTest Version: ${GOOGLETEST_VERSION}")
message(STATUS "GoogleTest Repository: ${GOOGLETEST_REPO}")

# Example: Using with FetchContent
include(FetchContent)

FetchContent_Declare(
    googletest
    GIT_REPOSITORY ${GOOGLETEST_REPO}
    GIT_TAG ${GOOGLETEST_VERSION}
)
FetchContent_MakeAvailable(googletest)

# Similarly for other packages:
execute_process(
    COMMAND ${Python3_EXECUTABLE} get_version.py get Windows-CalcEngine --field version
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    OUTPUT_VARIABLE WCE_VERSION
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

execute_process(
    COMMAND ${Python3_EXECUTABLE} get_version.py get Windows-CalcEngine --field repository
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    OUTPUT_VARIABLE WCE_REPO
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

message(STATUS "Windows-CalcEngine Version: ${WCE_VERSION}")

# FetchContent_Declare(
#     Windows-CalcEngine
#     GIT_REPOSITORY ${WCE_REPO}
#     GIT_TAG ${WCE_VERSION}
# )
# FetchContent_MakeAvailable(Windows-CalcEngine)
