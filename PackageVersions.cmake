# PackageVersions CMake Module
# 
# This module provides functions to load and use package versions from versions.json
# 
# Usage:
#   include(PackageVersions.cmake)
#   load_package_versions("${CMAKE_CURRENT_SOURCE_DIR}/PackageVersions/versions.json")
#   get_package_version("googletest" GTEST_VERSION)
#   message(STATUS "GoogleTest version: ${GTEST_VERSION}")

# Find Python3 for parsing JSON
find_package(Python3 COMPONENTS Interpreter QUIET)

# Global variable to store the path to versions.json
set(PACKAGE_VERSIONS_FILE "" CACHE INTERNAL "Path to versions.json file")

# Load package versions from JSON file
function(load_package_versions json_file)
    if(NOT EXISTS "${json_file}")
        message(FATAL_ERROR "Package versions file not found: ${json_file}")
    endif()
    
    set(PACKAGE_VERSIONS_FILE "${json_file}" CACHE INTERNAL "Path to versions.json file")
    message(STATUS "Loaded package versions from: ${json_file}")
endfunction()

# Get a specific package version
function(get_package_version package_name output_var)
    if("${PACKAGE_VERSIONS_FILE}" STREQUAL "")
        message(FATAL_ERROR "Package versions not loaded. Call load_package_versions() first.")
    endif()
    
    if(NOT Python3_Interpreter_FOUND)
        message(FATAL_ERROR "Python3 is required to parse versions.json but was not found.")
    endif()
    
    # Get the directory containing this module to find get_version.py
    get_filename_component(MODULE_DIR "${PACKAGE_VERSIONS_FILE}" DIRECTORY)
    
    execute_process(
        COMMAND ${Python3_EXECUTABLE} "${MODULE_DIR}/get_version.py" get "${package_name}" --field version
        OUTPUT_VARIABLE VERSION_OUTPUT
        ERROR_VARIABLE VERSION_ERROR
        RESULT_VARIABLE VERSION_RESULT
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    
    if(NOT VERSION_RESULT EQUAL 0)
        message(FATAL_ERROR "Failed to get version for package '${package_name}': ${VERSION_ERROR}")
    endif()
    
    set(${output_var} "${VERSION_OUTPUT}" PARENT_SCOPE)
endfunction()

# Get a specific package field (version, repository, etc.)
function(get_package_field package_name field_name output_var)
    if("${PACKAGE_VERSIONS_FILE}" STREQUAL "")
        message(FATAL_ERROR "Package versions not loaded. Call load_package_versions() first.")
    endif()
    
    if(NOT Python3_Interpreter_FOUND)
        message(FATAL_ERROR "Python3 is required to parse versions.json but was not found.")
    endif()
    
    # Get the directory containing this module to find get_version.py
    get_filename_component(MODULE_DIR "${PACKAGE_VERSIONS_FILE}" DIRECTORY)
    
    execute_process(
        COMMAND ${Python3_EXECUTABLE} "${MODULE_DIR}/get_version.py" get "${package_name}" --field "${field_name}"
        OUTPUT_VARIABLE FIELD_OUTPUT
        ERROR_VARIABLE FIELD_ERROR
        RESULT_VARIABLE FIELD_RESULT
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    
    if(NOT FIELD_RESULT EQUAL 0)
        message(FATAL_ERROR "Failed to get ${field_name} for package '${package_name}': ${FIELD_ERROR}")
    endif()
    
    set(${output_var} "${FIELD_OUTPUT}" PARENT_SCOPE)
endfunction()

# Example usage macro for common pattern
macro(fetch_external_package package_name)
    get_package_version(${package_name} PKG_VERSION)
    get_package_field(${package_name} repository PKG_REPO)
    
    message(STATUS "Fetching ${package_name} ${PKG_VERSION} from ${PKG_REPO}")
    
    # Note: You still need to call FetchContent_Declare and FetchContent_MakeAvailable
    # This macro just provides the version and repository info
endmacro()
