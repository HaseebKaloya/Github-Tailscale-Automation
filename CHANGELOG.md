# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
