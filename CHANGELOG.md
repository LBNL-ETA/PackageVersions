# Changelog

All notable changes to package versions will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.0.0] - 2026-02-05

### Added
- Initial release of centralized package version management
- `versions.json` with current versions for all THERM and WINDOW dependencies
- `validate.py` script to validate JSON structure
- `get_version.py` script to query package versions
- `PackageVersions.cmake` module for CMake integration
- Comprehensive README with usage examples
- Example CMakeLists.txt demonstrating integration

### Package Versions
- GoogleTest: v1.14.0
- Eigen: 5.0.1
- Windows-CalcEngine: Version_1.0.66
- KeffCavity: Version_1.0.31
- HygroThermFEM: Version_1.0.51
- CMake minimum: 3.12
- C++ Standard: C++20

## Guidelines for Updating

When updating package versions:

1. Update the version in `versions.json`
2. Update the `lastUpdated` field in `versions.json`
3. Add an entry to this CHANGELOG under `[Unreleased]`
4. When releasing, move entries from `[Unreleased]` to a new version section
5. Use semantic versioning for this repository's tags (if applicable)

### Entry Format

```markdown
### Changed
- Package-Name: old_version -> new_version (reason for update)
```

Example:
```markdown
### Changed
- GoogleTest: v1.14.0 -> v1.15.0 (security update)
- Eigen: 5.0.1 -> 5.0.2 (bug fixes)
```
