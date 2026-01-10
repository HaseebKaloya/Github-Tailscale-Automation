"""
Completion Dialog for Github&Tailscale-Automation
Author: Haseeb Kaloya

Shows results after repository creation
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.helpers import format_duration

class CompletionDialog(QDialog):
    """Completion results dialog"""
    
    def __init__(self, success, message, results, parent=None):
        """
        Initialize completion dialog
        
        Args:
            success: Whether operation succeeded
            message: Summary message
            results: Results dictionary with statistics
            parent: Parent widget
        """
        super().__init__(parent)
        self.success = success
        self.message = message
        self.results = results
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Operation Complete")
        self.setModal(True)
        self.setFixedSize(600, 500)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Icon and title
        self.create_header(layout)
        
        # Summary
        self.create_summary(layout)
        
        # Details
        self.create_details(layout)
        
        # Buttons
        self.create_buttons(layout)
    
    def create_header(self, parent_layout):
        """Create header section"""
        header_layout = QHBoxLayout()
        
        # Icon
        icon_label = QLabel("✓" if self.success else "✗")
        icon_label.setFont(QFont("Segoe UI", 48))
        icon_label.setStyleSheet(f"color: {'#00B050' if self.success else '#C00000'};")
        icon_label.setFixedWidth(80)
        icon_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(icon_label)
        
        # Title and message
        text_layout = QVBoxLayout()
        
        title = QLabel("Success!" if self.success else "Operation Failed")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet(f"color: {'#00B050' if self.success else '#C00000'};")
        text_layout.addWidget(title)
        
        msg = QLabel(self.message)
        msg.setFont(QFont("Segoe UI", 10))
        msg.setWordWrap(True)
        text_layout.addWidget(msg)
        
        header_layout.addLayout(text_layout)
        parent_layout.addLayout(header_layout)
        
        # Separator
        separator = QLabel()
        separator.setFixedHeight(2)
        separator.setStyleSheet(f"background-color: {'#00B050' if self.success else '#C00000'};")
        parent_layout.addWidget(separator)
    
    def create_summary(self, parent_layout):
        """Create summary section"""
        group = QGroupBox(" Summary ")
        group.setFont(QFont("Segoe UI", 9, QFont.Bold))
        
        layout = QVBoxLayout(group)
        layout.setSpacing(10)
        
        # Statistics
        created_count = len(self.results.get('created_repos', []))
        keys_count = self.results.get('generated_keys', 0)
        errors_count = len(self.results.get('errors', []))
        elapsed = self.results.get('elapsed_time', 0)
        
        stats_text = f"""
<b>Repositories Created:</b> {created_count}<br>
<b>Tailscale Keys Generated:</b> {keys_count}<br>
<b>Errors:</b> {errors_count}<br>
<b>Time Elapsed:</b> {format_duration(elapsed)}
        """
        
        stats_label = QLabel(stats_text)
        stats_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(stats_label)
        
        parent_layout.addWidget(group)
    
    def create_details(self, parent_layout):
        """Create details section"""
        group = QGroupBox(" Details ")
        group.setFont(QFont("Segoe UI", 9, QFont.Bold))
        
        layout = QVBoxLayout(group)
        
        # Details text
        details_text = QTextEdit()
        details_text.setReadOnly(True)
        details_text.setFont(QFont("Consolas", 9))
        details_text.setStyleSheet("""
            QTextEdit {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }
        """)
        
        # Build details
        details = ""
        
        # Created repositories
        created_repos = self.results.get('created_repos', [])
        if created_repos:
            details += "✓ Created Repositories:\n"
            for repo in created_repos:
                details += f"  • {repo}\n"
            details += "\n"
        
        # Errors
        errors = self.results.get('errors', [])
        if errors:
            details += "✗ Errors:\n"
            for error in errors:
                details += f"  • {error}\n"
            details += "\n"
        
        # Additional info
        if self.results.get('generated_keys', 0) > 0:
            details += f"ℹ Tailscale keys saved to backup file\n"
        
        details_text.setText(details.strip())
        layout.addWidget(details_text)
        
        parent_layout.addWidget(group)
    
    def create_buttons(self, parent_layout):
        """Create button section"""
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        # View Logs button
        btn_logs = QPushButton("View Logs")
        btn_logs.setFixedWidth(120)
        btn_logs.clicked.connect(self.open_logs)
        btn_layout.addWidget(btn_logs)
        
        # OK button
        btn_ok = QPushButton("OK")
        btn_ok.setFixedWidth(120)
        btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        btn_ok.clicked.connect(self.accept)
        btn_layout.addWidget(btn_ok)
        
        parent_layout.addLayout(btn_layout)
    
    def open_logs(self):
        """Open logs folder"""
        import subprocess
        import platform
        from pathlib import Path
        
        try:
            logs_path = Path("logs")
            if not logs_path.exists():
                logs_path.mkdir(exist_ok=True)
            
            # Open in file explorer
            if platform.system() == 'Windows':
                subprocess.Popen(['explorer', str(logs_path)])
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', str(logs_path)])
            else:  # Linux
                subprocess.Popen(['xdg-open', str(logs_path)])
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to open logs folder:\n{str(e)}"
            )
