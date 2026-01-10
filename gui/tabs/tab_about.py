"""
About Tab for Github&Tailscale-Automation
Author: Haseeb Kaloya

Professional about page with clean, modern styling
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QDesktopServices
from PyQt5.QtCore import QUrl

from core.constants import (
    APP_NAME, APP_VERSION, AUTHOR_NAME, 
    AUTHOR_EMAIL, AUTHOR_CONTACT
)
from gui.responsive_widgets import ResponsiveContainer
from gui.styles import GROUPBOX_STYLE, BUTTON_PRIMARY

class TabAbout(QWidget):
    """About tab widget with clean, professional design"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        container = ResponsiveContainer(self, max_width=1100)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        
        layout = container.get_layout()
        layout.setSpacing(20)
        
        # Header section
        header_label = QLabel(f"{APP_NAME}")
        header_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                color: #0078D4;
                background-color: transparent;
                padding: 20px;
            }
        """)
        layout.addWidget(header_label)
        
        # Version badge
        version_label = QLabel(f"Version {APP_VERSION}")
        version_label.setFont(QFont("Segoe UI", 11))
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("""
            QLabel {
                color: #0078D4;
                background-color: transparent;
                border: 2px solid #0078D4;
                border-radius: 15px;
                padding: 8px 20px;
            }
        """)
        layout.addWidget(version_label)
        
        # Description
        desc_group = QGroupBox("Professional GitHub & Tailscale Automation")
        desc_group.setFont(QFont("Segoe UI", 12, QFont.Bold))
        desc_group.setStyleSheet(GROUPBOX_STYLE)
        desc_layout = QVBoxLayout(desc_group)
        desc_layout.setSpacing(15)
        
        desc_text = QLabel(
            "Transform your workflow with automated repository creation, "
            "file uploads, secret management, and workflow execution. "
            "Built with precision for developers who value their time."
        )
        desc_text.setWordWrap(True)
        desc_text.setFont(QFont("Segoe UI", 10))
        desc_text.setStyleSheet("color: #333; line-height: 1.6; background-color: transparent; padding: 10px;")
        desc_layout.addWidget(desc_text)
        
        layout.addWidget(desc_group)
        
        # Features
        features_group = QGroupBox("Key Features")
        features_group.setFont(QFont("Segoe UI", 12, QFont.Bold))
        features_group.setStyleSheet(GROUPBOX_STYLE)
        features_layout = QVBoxLayout(features_group)
        features_layout.setSpacing(10)
        
        features = [
            ("Smart Repository Creation", "Generate multiple repos with intelligent naming"),
            ("Automated File Uploads", "Upload workflows, projects, and .gitignore files"),
            ("Secret Management", "Auto-generate or import Tailscale keys securely"),
            ("Workflow Automation", "Start GitHub Actions with one click"),
        ]
        
        for title, desc in features:
            feature_widget = self.create_feature_card(title, desc)
            features_layout.addWidget(feature_widget)
        
        layout.addWidget(features_group)
        
        # Developer info
        dev_group = QGroupBox("Developer Information")
        dev_group.setFont(QFont("Segoe UI", 12, QFont.Bold))
        dev_group.setStyleSheet(GROUPBOX_STYLE)
        dev_layout = QVBoxLayout(dev_group)
        dev_layout.setSpacing(10)
        
        dev_name = QLabel(f"<b>Developer:</b> {AUTHOR_NAME}")
        dev_name.setStyleSheet("font-size: 10pt; background-color: transparent; padding: 5px;")
        dev_layout.addWidget(dev_name)
        
        dev_email = QLabel(f"<b>Email:</b> {AUTHOR_EMAIL}")
        dev_email.setStyleSheet("font-size: 10pt; background-color: transparent; padding: 5px;")
        dev_layout.addWidget(dev_email)
        
        dev_phone = QLabel(f"<b>Phone:</b> {AUTHOR_CONTACT}")
        dev_phone.setStyleSheet("font-size: 10pt; background-color: transparent; padding: 5px;")
        dev_layout.addWidget(dev_phone)
        
        # GitHub button
        github_btn = QPushButton("Visit GitHub Profile")
        github_btn.setFixedHeight(40)
        github_btn.setStyleSheet(BUTTON_PRIMARY)
        github_btn.setCursor(Qt.PointingHandCursor)
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl("https://github.com/HaseebKaloya")
        ))
        dev_layout.addWidget(github_btn)
        
        layout.addWidget(dev_group)
        
        # Custom services
        services_group = QGroupBox("Need Custom Automation?")
        services_group.setFont(QFont("Segoe UI", 12, QFont.Bold))
        services_group.setStyleSheet(GROUPBOX_STYLE)
        services_layout = QVBoxLayout(services_group)
        services_layout.setSpacing(15)
        
        services_text = QLabel(
            "Looking for custom automation solutions? I build tailored tools "
            "for GitHub workflows, CI/CD pipelines, API integrations, and more. "
            "Fast turnaround, clean code, ongoing support."
        )
        services_text.setWordWrap(True)
        services_text.setStyleSheet("font-size: 10pt; line-height: 1.6; background-color: transparent; padding: 10px;")
        services_layout.addWidget(services_text)
        
        contact_btn = QPushButton("Contact Me for Custom Development")
        contact_btn.setFixedHeight(45)
        contact_btn.setStyleSheet(BUTTON_PRIMARY)
        contact_btn.setCursor(Qt.PointingHandCursor)
        contact_btn.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl(f"mailto:{AUTHOR_EMAIL}")
        ))
        services_layout.addWidget(contact_btn)
        
        layout.addWidget(services_group)
        
        # Footer
        footer = QLabel("© 2026 Haseeb Kaloya. All rights reserved.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 9pt;
                background-color: transparent;
                padding: 20px;
            }
        """)
        layout.addWidget(footer)
        
        layout.addStretch()
    
    def create_feature_card(self, title, description):
        """Create a clean feature card"""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border-left: 3px solid #0078D4;
                padding-left: 15px;
            }
        """)
        card_layout = QVBoxLayout(widget)
        card_layout.setContentsMargins(15, 10, 10, 10)
        card_layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title_label.setStyleSheet("color: #0078D4; background-color: transparent;")
        card_layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 9))
        desc_label.setStyleSheet("color: #666; background-color: transparent;")
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)
        
        return widget
    
    def get_config(self):
        """Get configuration from this tab"""
        return {}
    
    def set_config(self, config):
        """Set configuration to this tab"""
        pass
