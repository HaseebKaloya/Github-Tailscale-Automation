# Developer Guide

This guide is intended for developers who want to contribute to **Github&Tailscale-Automation** or understand its internal architecture.

## Architecture Overview

The application follows a modular **Model-View-Controller (MVC)** inspired architecture, built with **Python 3.10+** and **PyQt5**.

### Directory Structure

```
Github-Tailscale-Automation/
├── api/                  # External API Wrappers
│   ├── github_api.py     # PyGithub wrapper
│   └── tailscale_api.py  # Tailscale HTTP API wrapper
├── core/                 # Business Logic & Controllers
│   ├── config_manager.py # Settings management
│   ├── diagnostics.py    # System health checks
│   └── main_window.py    # Main GUI Controller
├── gui/                  # Presentation Layer
│   ├── tabs/             # Individual tab widgets
│   ├── widgets/          # Reusable UI components
│   └── styles.py         # CSS-like QSS styling
├── utils/                # Utilities
│   ├── logger.py         # Thread-safe logging
│   └── recovery.py       # State persistence
└── main.py               # Application Entry Point
```

---

## Core Components

### 1. The API Layer (`api/`)
We use dedicated wrapper classes to abstract external dependencies.
*   **`GitHubAPI`**: Handles authentication, repository creation, file uploads, and secret encryption (using `PyNaCl`).
*   **`TailscaleAPI`**: Handles direct HTTP requests to the Tailscale control plane for key generation.

### 2. The GUI Layer (`gui/`)
*   **Responsive Design**: We use a custom `ResponsiveContainer` class that adjusts layouts based on window width.
*   **Styling**: All styles are defined in `gui/styles.py` to ensure consistency. We use a Dark Mode palette by default.
*   **Thread Safety**: Long-running operations (like bulk repo creation) must be run in background threads (`QThread`) to keep the UI responsive. *Note: Currently, some operations are synchronous; moving them to `QThread` is a planned improvement.*

### 3. State Management (`core/config_manager.py`)
Configuration is stored in a JSON file. The `ConfigManager` class handles loading, validating, and saving these settings.
*   **Security**: Sensitive tokens are stored in plain text in the JSON file in this version. *Future work: Integrate system keyring.*

### 4. Diagnostics & Recovery
*   **`SystemDiagnostics`**: Runs a suite of checks (socket connections, file permissions) to ensure the environment is healthy.
*   **`RecoveryManager`**: Saves the state of bulk operations. If the app crashes, it creates a `session_X.json` file in `recovery/` that tracks which repositories were successfully created and which failed.

---

## Extending the Application

### Adding a New Tab
1.  Create a new file in `gui/tabs/`, e.g., `tab_analytics.py`.
2.  Define a class inheriting from `QWidget`.
3.  Implement `init_ui()` method.
4.  Register the tab in `core/main_window.py` inside the `init_all_pages` method and add a button to the `Sidebar`.

### Adding a New API Feature
1.  Open the relevant file in `api/`.
2.  Add a method to the class (e.g., `delete_repository` in `GitHubAPI`).
3.  Ensure proper error handling using `try-except` blocks.
4.  Log all actions using `self.logger`.

---

## Development Environment

### Setup
```bash
# Clone
git clone <repo-url>

# Virtual Env
python -m venv venv
source venv/bin/activate

# Install
pip install -r requirements.txt
```

### Testing
Run the test suite (if available) or manual diagnostics:
```bash
python main.py --check
```

---

## Coding Standards
*   **Style**: Follow PEP 8.
*   **Docstrings**: All classes and methods must have docstrings.
*   **Type Hints**: Use Python type hinting (`typing` module) for function arguments and return values.
*   **Logging**: Never use `print()`; use `logger.info()` or `logger.error()`.
