"""
Path management utility for Github&Tailscale-Automation
Handles bundled resources for PyInstaller EXE conversion.
"""

import os
import sys
from pathlib import Path

def get_app_root() -> Path:
    """
    Get the absolute path to the application root.
    Handles both script execution and PyInstaller bundling.
    """
    if getattr(sys, 'frozen', False):
        # Running as a bundled EXE
        # Use the directory where the EXE is located for persistent data
        return Path(sys.executable).parent
    else:
        # Running as a normal Python script
        return Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_resource_path(relative_path: str) -> Path:
    """
    Get the absolute path to a resource.
    For PyInstaller, resources are extracted to a temporary folder (_MEIPASS).
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    else:
        base_path = get_app_root()
        
    return base_path / relative_path

# Standard App Paths
APP_ROOT = get_app_root()
LOGS_DIR = APP_ROOT / "logs"
CONFIGS_DIR = APP_ROOT / "configs"
RESOURCES_DIR = get_resource_path("resources")

def ensure_dirs():
    """Ensure all required directories exist."""
    LOGS_DIR.mkdir(exist_ok=True)
    CONFIGS_DIR.mkdir(exist_ok=True)
