# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-01-12

### Added
- **CI/CD**: GitHub Actions workflow to automatically build and release the application on new version tags.
- **Documentation**:
    - `USER_GUIDE.md` with detailed, step-by-step instructions and screenshots.
    - `PULL_REQUEST_TEMPLATE.md` to standardize community contributions.
    - `CODE_OF_CONDUCT.md` based on the Contributor Covenant.
- **Build**:
    - PyInstaller build configuration (`.spec` file) for creating a standalone Windows executable.

### Changed
- **Documentation**:
    - `README.md`:
        - Added a Table of Contents for improved navigation.
        - Added badges for stars, forks, and open issues.
        - Made "Screenshots" and "Project Structure" sections collapsible for a cleaner layout.
    - `CONTRIBUTING.md`: Updated to reference the new `CODE_OF_CONDUCT.md`.
    - `SECURITY.md`: Enhanced with specific details on data handling and encryption.

## [1.0.0] - 2026-01-10

### Added
- **GUI**: Modern PyQt5 interface with responsive widgets and dark mode support.
- **GitHub Automation**:
    - Bulk repository creation with configurable settings (Issues, Wiki, Projects).
    - Automated file uploads to repositories.
    - GitHub Secrets management using `PyNaCl` encryption.
    - Workflow dispatch triggers.
- **Tailscale Integration**:
    - Automated auth key generation.
    - Support for reusable, ephemeral, and pre-authorized keys.
    - Tag management for keys.
- **System**:
    - Comprehensive system diagnostics and dependency checking.
    - Robust logging system with rotation.
    - Configuration management with validation.

### Security
- Implemented secure handling of API tokens and keys.
- Added dependency validation on startup.

### Documentation
- Initial release of comprehensive documentation.
