# Quick Start Guide

This guide will help you quickly integrate PackageVersions into your THERM or WINDOW project.

## Option 1: Using as a Git Submodule (Recommended)

```bash
# Add PackageVersions as a submodule to your project
cd your-project
git submodule add https://github.com/LBNL-ETA/PackageVersions.git

# Update your CMakeLists.txt
cat >> CMakeLists.txt << 'EOF'

# Load PackageVersions
find_package(Python3 COMPONENTS Interpreter REQUIRED)

# Get GoogleTest version
execute_process(
    COMMAND ${Python3_EXECUTABLE} PackageVersions/get_version.py get googletest --field version
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    OUTPUT_VARIABLE GOOGLETEST_VERSION
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

execute_process(
    COMMAND ${Python3_EXECUTABLE} PackageVersions/get_version.py get googletest --field repository
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    OUTPUT_VARIABLE GOOGLETEST_REPO
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Use with FetchContent
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY ${GOOGLETEST_REPO}
    GIT_TAG ${GOOGLETEST_VERSION}
)
FetchContent_MakeAvailable(googletest)
EOF
```

## Option 2: Quick CLI Usage

```bash
# Clone the repository
git clone https://github.com/LBNL-ETA/PackageVersions.git
cd PackageVersions

# List all packages
python3 get_version.py list

# Get specific version
python3 get_version.py get googletest --field version

# Get repository URL
python3 get_version.py get Windows-CalcEngine --field repository

# List packages used by a specific project
python3 get_version.py list --used-by HygroThermFEM

# Validate the JSON file
python3 validate.py
```

## Option 3: Direct JSON Access

```bash
# Using jq to query versions.json
cat PackageVersions/versions.json | jq -r '.packages.testing.googletest.version'

# Get all internal packages
cat PackageVersions/versions.json | jq '.packages.internal'
```

## Common Use Cases

### 1. Update a Package Version

```bash
# Edit versions.json
vim PackageVersions/versions.json

# Update the version field
# Update the lastUpdated field

# Validate
python3 validate.py

# Commit
git add versions.json
git commit -m "Update googletest to v1.15.0"
```

### 2. Add a New Package

```json
{
  "packages": {
    "libraries": {
      "your-new-package": {
        "version": "1.0.0",
        "type": "git_tag",
        "repository": "https://github.com/example/package.git",
        "description": "Description of the package",
        "usedBy": ["YourProject"]
      }
    }
  }
}
```

### 3. Check What Packages a Project Uses

```bash
python3 get_version.py list --used-by Windows-CalcEngine
```

## Integration Examples

### CMake Example

See `examples/CMakeLists.txt` for a complete working example.

### Shell Script Example

```bash
#!/bin/bash
GTEST_VERSION=$(python3 PackageVersions/get_version.py get googletest --field version)
echo "Using GoogleTest version: $GTEST_VERSION"
```

### Python Script Example

```python
import json

with open('PackageVersions/versions.json', 'r') as f:
    versions = json.load(f)
    
gtest_version = versions['packages']['testing']['googletest']['version']
print(f"GoogleTest version: {gtest_version}")
```

## Next Steps

1. Read the full [README.md](README.md) for comprehensive documentation
2. Check [CHANGELOG.md](CHANGELOG.md) for version update guidelines
3. Explore [examples/](examples/) for integration patterns
4. Set up automated validation in your CI/CD pipeline

## Getting Help

- Check the [README.md](README.md) for detailed documentation
- Review existing package configurations in `versions.json`
- Look at the example in `examples/CMakeLists.txt`

## Best Practices

1. **Always validate** after editing versions.json: `python3 validate.py`
2. **Update lastUpdated** field when changing versions
3. **Document changes** in CHANGELOG.md
4. **Test your changes** in dependent projects before merging
5. **Use consistent version formats** (follow existing patterns)
