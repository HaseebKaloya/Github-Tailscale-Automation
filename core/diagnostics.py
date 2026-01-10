
import sys
import os
import socket
import requests
import importlib.metadata
import platform
from datetime import datetime

class SystemDiagnostics:
    """
    Performs system health checks for the Github&Tailscale-Automation application.
    Checks:
    1. Network connectivity (General Internet, GitHub API, Tailscale API)
    2. File system permissions (Logs, Backups, Configs)
    3. Python Environment & Dependencies
    """

    def __init__(self):
        self.results = []
        self.all_passed = True

    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results.append(f"[{timestamp}] [{status}] {message}")
        if status == "ERROR":
            self.all_passed = False

    def check_network(self):
        """Check internet and API connectivity"""
        self.log("Testing Network Connectivity...", "INFO")
        
        # 1. General Internet
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            self.log("Internet connection: OK", "PASS")
        except OSError:
            self.log("Internet connection: FAILED", "ERROR")
            return

        # 2. GitHub API
        try:
            response = requests.get("https://api.github.com/zen", timeout=5)
            if response.status_code == 200:
                self.log("GitHub API connection: OK", "PASS")
            else:
                self.log(f"GitHub API returned status: {response.status_code}", "WARNING")
        except requests.RequestException as e:
            self.log(f"GitHub API connection failed: {str(e)}", "ERROR")

        # 3. Tailscale API
        try:
            # Just check if the domain is resolvable and reachable
            socket.create_connection(("api.tailscale.com", 443), timeout=5)
            self.log("Tailscale API reachable: OK", "PASS")
        except OSError:
            self.log("Tailscale API unreachable", "ERROR")

    def check_permissions(self):
        """Check file system permissions"""
        self.log("Testing File Permissions...", "INFO")
        
        cwd = os.getcwd()
        dirs_to_check = [
            cwd,
            os.path.join(cwd, "logs"),
            os.path.join(cwd, "backups"),
            os.path.join(cwd, "configs"),
            os.path.join(cwd, "resources")
        ]

        for directory in dirs_to_check:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                    self.log(f"Created missing directory: {directory}", "FIX")
                except OSError as e:
                    self.log(f"Failed to create directory {directory}: {e}", "ERROR")
                    continue
            
            # Check write permission
            if os.access(directory, os.W_OK):
                self.log(f"Write access to {os.path.basename(directory)}: OK", "PASS")
            else:
                self.log(f"Write access to {os.path.basename(directory)}: DENIED", "ERROR")

    def check_dependencies(self):
        """Check required python packages"""
        self.log("Checking Dependencies...", "INFO")
        
        required = {
            "PyQt5": "5.0.0",
            "PyGithub": "1.50",
            "requests": "2.0.0",
            "pynacl": "1.4.0",
            "python-dotenv": "0.10.0"
        }
        
        for package, min_version in required.items():
            try:
                version = importlib.metadata.version(package)
                self.log(f"Package '{package}' found (v{version})", "PASS")
            except importlib.metadata.PackageNotFoundError:
                self.log(f"Package '{package}' MISSING", "ERROR")

    def run_all(self):
        """Run all checks and return report"""
        self.log(f"Starting System Diagnostics on {platform.system()} {platform.release()}", "INFO")
        
        self.check_network()
        self.check_permissions()
        self.check_dependencies()
        
        status = "PASSED" if self.all_passed else "COMPLETED WITH ERRORS"
        self.log(f"Diagnostics {status}", "INFO")
        
        return "\n".join(self.results), self.all_passed

if __name__ == "__main__":
    diag = SystemDiagnostics()
    report, passed = diag.run_all()
    print(report)
    sys.exit(0 if passed else 1)
