# PackageVersions

A centralized repository for managing package versions across LBNL-ETA projects, specifically THERM and WINDOW.

## Purpose

This repository maintains the canonical version information for all external dependencies and internal packages used by THERM and WINDOW projects. By maintaining a single source of truth for package versions, we ensure:

- **Consistency**: All projects use the same versions of shared dependencies
- **Reproducibility**: Build environments can be reliably recreated
- **Maintainability**: Version updates can be coordinated across all projects
- **Visibility**: Clear documentation of dependency relationships

## Package Structure

The `versions.json` file contains all version information organized into categories:

- **testing**: Testing frameworks (GoogleTest)
- **libraries**: External C++ libraries (Eigen)
- **internal**: LBNL-ETA internal packages (Windows-CalcEngine, KeffCavity, HygroThermFEM)
- **build**: Build system requirements (CMake, C++ standard)

## Usage

### For THERM and WINDOW Projects

When setting up dependencies in your CMakeLists.txt, reference the versions from this repository:

#### Example: Fetching GoogleTest

```cmake
set(GoogleTest_Version "v1.14.0")  # From versions.json
FetchContent_Declare(
    GTestExternal
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG ${GoogleTest_Version}
)
```

#### Example: Fetching Windows-CalcEngine

```cmake
set(WindowsCalcEngine_Branch "Version_1.0.66")  # From versions.json
FetchContent_Declare(
    Windows-CalcEngine
    GIT_REPOSITORY https://github.com/LBNL-ETA/Windows-CalcEngine
    GIT_TAG ${WindowsCalcEngine_Branch}
)
```

### Querying Versions Programmatically

You can parse the `versions.json` file in your build scripts or CI/CD pipelines:

```bash
# Using jq to get GoogleTest version
cat versions.json | jq -r '.packages.testing.googletest.version'

# Get all packages used by a specific project
cat versions.json | jq '.packages[][] | select(.usedBy[] == "HygroThermFEM")'
```

## Updating Versions

When updating a package version:

1. Update the version in `versions.json`
2. Update the `lastUpdated` field
3. Commit the change with a clear message indicating what changed
4. Create tags if needed for tracking major dependency updates

## Current Dependencies

### Core Projects
- **Windows-CalcEngine** v1.0.66: Thermal and optical routines
- **KeffCavity** v1.0.31: Cavity effective conductance calculations  
- **HygroThermFEM** v1.0.51: Hygrothermal finite element modeling

### External Libraries
- **GoogleTest** v1.14.0: Testing framework
- **Eigen** 5.0.1: Linear algebra library

### Build Requirements
- **CMake** 3.12+ minimum (3.20+ recommended)
- **C++ Standard**: C++20

## Integration

To integrate this repository into your project:

1. Add this repository as a git submodule:
   ```bash
   git submodule add https://github.com/LBNL-ETA/PackageVersions.git
   ```

2. Or reference it in your CI/CD pipeline to fetch the latest versions

3. Parse `versions.json` in your build scripts to set version variables

## Contributing

When adding new packages or updating versions:

1. Ensure all fields are filled out (version, repository, description, usedBy)
2. Keep the JSON properly formatted and validated
3. Update this README if new categories or usage patterns are introduced
4. Test the changes with dependent projects before merging

## License

This repository follows the same license as the LBNL-ETA organization projects.