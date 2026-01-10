#!/usr/bin/env python3
"""
Github&Tailscale-Automation - Professional Edition
Author: Haseeb Kaloya
Email: haseebkaloya@gmail.com
Contact: +92-3294163702

Complete GitHub & Tailscale Automation Platform
Bulk Repositories | Automated Keys | Actions | Secrets | More
"""

import sys
import os
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from core.main_window import MainWindow
from utils.logger import setup_logger
from utils.paths import RESOURCES_DIR, LOGS_DIR, ensure_dirs
from utils.icon_utils import get_cropped_icon
from core.diagnostics import SystemDiagnostics

def check_dependencies_robust():
    """Check dependencies using importlib.metadata"""
    diag = SystemDiagnostics()
    diag.check_dependencies()
    return diag.all_passed

def main():
    """Main application entry point"""
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="Github&Tailscale-Automation")
    parser.add_argument("--check", action="store_true", help="Run system diagnostics and exit")
    args = parser.parse_args()

    # Setup logging
    logger = setup_logger()
    
    if args.check:
        print("Running System Diagnostics...")
        diag = SystemDiagnostics()
        report, passed = diag.run_all()
        print(report)
        sys.exit(0 if passed else 1)

    logger.info("Starting Github&Tailscale-Automation...")
    logger.info("Developed by: Haseeb Kaloya")
    
    # Check dependencies
    if not check_dependencies_robust():
        logger.warning("Some dependencies might be missing or broken. Running anyway, but errors may occur.")
    
    # Create Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName("Github&Tailscale-Automation")
    app.setOrganizationName("Haseeb Kaloya")
    
    # Ensure persistent directories exist
    ensure_dirs()

    # Set Application Icon (Taskbar and Window Title Bars)
    # Using the optimized favicon for UI visibility
    app_icon = get_cropped_icon(RESOURCES_DIR / "app_favicon.png")
    if not app_icon.isNull():
        app.setWindowIcon(app_icon)
    else:
        logger.warning("Failed to load or crop application icon")

    # Enable high DPI scaling
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    try:
        # Create and show main window
        window = MainWindow()
        window.show()
        
        logger.info("Application started successfully")
        return app.exec_()
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
