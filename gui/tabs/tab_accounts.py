"""
Accounts Tab for Github&Tailscale-Automation
Author: Haseeb Kaloya

GitHub and Tailscale credentials configuration
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
import os

from api.github_api import GitHubAPI
from api.tailscale_api import TailscaleAPI
from utils.validators import validate_github_token, validate_tailscale_key
from utils.logger import get_logger
from gui.responsive_widgets import ResponsiveContainer, OptimalFormLayout
from gui.styles import GROUPBOX_STYLE, INPUT_STYLE, BUTTON_PRIMARY, BUTTON_SUCCESS

class TabAccounts(QWidget):
    """Accounts tab widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.logger = get_logger()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        # Create responsive container
        container = ResponsiveContainer(self, max_width=1100)
        
        # Set container as main widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        
        # Get content layout from container
        content_layout = container.get_layout()
        
        # GitHub Section
        self.create_github_section(content_layout)
        
        # Tailscale Section
        self.create_tailscale_section(content_layout)
        
        # Spacer
        content_layout.addStretch()
    
    def create_github_section(self, parent_layout):
        """Create GitHub credentials section"""
        group_box = QGroupBox("GitHub Credentials")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(18)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Username
        self.txt_github_username = QLineEdit()
        self.txt_github_username.setPlaceholderText("Enter GitHub username")
        self.txt_github_username.setStyleSheet(INPUT_STYLE)
        self.txt_github_username.setMinimumHeight(40)
        username_row = OptimalFormLayout.create_field_row(
            "Username:",
            self.txt_github_username
        )
        layout.addLayout(username_row)
        
        # Token
        self.txt_github_token = QLineEdit()
        self.txt_github_token.setPlaceholderText("Enter GitHub personal access token (ghp_...)")
        self.txt_github_token.setEchoMode(QLineEdit.Password)
        self.txt_github_token.setStyleSheet(INPUT_STYLE)
        self.txt_github_token.setMinimumHeight(40)
        
        self.btn_show_github = QPushButton("Show")
        self.btn_show_github.setFixedSize(100, 40)
        self.btn_show_github.setCursor(Qt.PointingHandCursor)
        self.btn_show_github.setStyleSheet(BUTTON_PRIMARY)
        self.btn_show_github.setIcon(QIcon("resources/icons/eye.svg"))
        self.btn_show_github.setIconSize(QSize(20, 20))
        self.btn_show_github.clicked.connect(self.toggle_github_token)
        
        token_row = OptimalFormLayout.create_field_row(
            "Token:",
            self.txt_github_token,
            self.btn_show_github
        )
        layout.addLayout(token_row)
        
        # Test button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_test_github = QPushButton("Test Connection")
        self.btn_test_github.setFixedSize(180, 45)
        self.btn_test_github.setCursor(Qt.PointingHandCursor)
        self.btn_test_github.setStyleSheet(BUTTON_SUCCESS)
        self.btn_test_github.setIcon(QIcon("resources/icons/check.svg"))
        self.btn_test_github.setIconSize(QSize(20, 20))
        self.btn_test_github.clicked.connect(self.test_github_connection)
        btn_layout.addWidget(self.btn_test_github)
        layout.addLayout(btn_layout)
        
        # Status label
        self.lbl_github_status = QLabel("")
        self.lbl_github_status.setAlignment(Qt.AlignCenter)
        self.lbl_github_status.setMinimumHeight(30)
        self.lbl_github_status.setStyleSheet("""
            QLabel {
                padding: 8px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 10pt;
            }
        """)
        layout.addWidget(self.lbl_github_status)
        
        parent_layout.addWidget(group_box)
    
    def create_tailscale_section(self, parent_layout):
        """Create Tailscale credentials section"""
        group_box = QGroupBox("Tailscale Credentials")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(18)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # API Key
        self.txt_tailscale_api = QLineEdit()
        self.txt_tailscale_api.setPlaceholderText("Enter Tailscale API key (tskey-api-...)")
        self.txt_tailscale_api.setEchoMode(QLineEdit.Password)
        self.txt_tailscale_api.setStyleSheet(INPUT_STYLE)
        self.txt_tailscale_api.setMinimumHeight(40)
        
        self.btn_show_tailscale = QPushButton("Show")
        self.btn_show_tailscale.setFixedSize(100, 40)
        self.btn_show_tailscale.setCursor(Qt.PointingHandCursor)
        self.btn_show_tailscale.setStyleSheet(BUTTON_PRIMARY)
        self.btn_show_tailscale.setIcon(QIcon("resources/icons/eye.svg"))
        self.btn_show_tailscale.setIconSize(QSize(20, 20))
        self.btn_show_tailscale.clicked.connect(self.toggle_tailscale_key)
        
        api_row = OptimalFormLayout.create_field_row(
            "API Key:",
            self.txt_tailscale_api,
            self.btn_show_tailscale
        )
        layout.addLayout(api_row)
        
        # Network
        self.txt_tailscale_network = QLineEdit()
        self.txt_tailscale_network.setPlaceholderText("Enter Tailscale network name (e.g., example.com)")
        self.txt_tailscale_network.setStyleSheet(INPUT_STYLE)
        self.txt_tailscale_network.setMinimumHeight(40)
        network_row = OptimalFormLayout.create_field_row(
            "Tailnet:",
            self.txt_tailscale_network
        )
        layout.addLayout(network_row)
        
        # Test button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_test_tailscale = QPushButton("Test Connection")
        self.btn_test_tailscale.setFixedSize(180, 45)
        self.btn_test_tailscale.setCursor(Qt.PointingHandCursor)
        self.btn_test_tailscale.setStyleSheet(BUTTON_SUCCESS)
        self.btn_test_tailscale.setIcon(QIcon("resources/icons/check.svg"))
        self.btn_test_tailscale.setIconSize(QSize(20, 20))
        self.btn_test_tailscale.clicked.connect(self.test_tailscale_connection)
        btn_layout.addWidget(self.btn_test_tailscale)
        layout.addLayout(btn_layout)
        
        # Status label
        self.lbl_tailscale_status = QLabel("")
        self.lbl_tailscale_status.setAlignment(Qt.AlignCenter)
        self.lbl_tailscale_status.setMinimumHeight(30)
        self.lbl_tailscale_status.setWordWrap(True)
        self.lbl_tailscale_status.setStyleSheet("""
            QLabel {
                padding: 8px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 10pt;
            }
        """)
        layout.addWidget(self.lbl_tailscale_status)
        
        parent_layout.addWidget(group_box)
    
    def toggle_github_token(self):
        """Toggle GitHub token visibility"""
        if self.txt_github_token.echoMode() == QLineEdit.Password:
            self.txt_github_token.setEchoMode(QLineEdit.Normal)
            self.btn_show_github.setText("Hide")
            self.btn_show_github.setIcon(QIcon("resources/icons/eye_off.svg"))
        else:
            self.txt_github_token.setEchoMode(QLineEdit.Password)
            self.btn_show_github.setText("Show")
            self.btn_show_github.setIcon(QIcon("resources/icons/eye.svg"))
    
    def toggle_tailscale_key(self):
        """Toggle Tailscale key visibility"""
        if self.txt_tailscale_api.echoMode() == QLineEdit.Password:
            self.txt_tailscale_api.setEchoMode(QLineEdit.Normal)
            self.btn_show_tailscale.setText("Hide")
            self.btn_show_tailscale.setIcon(QIcon("resources/icons/eye_off.svg"))
        else:
            self.txt_tailscale_api.setEchoMode(QLineEdit.Password)
            self.btn_show_tailscale.setText("Show")
            self.btn_show_tailscale.setIcon(QIcon("resources/icons/eye.svg"))
    
    def test_github_connection(self):
        """Test GitHub API connection"""
        try:
            username = self.txt_github_username.text().strip()
            token = self.txt_github_token.text().strip()
            
            if not username or not token:
                self.lbl_github_status.setStyleSheet("color: #C00000;")
                self.lbl_github_status.setText("⚠ Please enter both username and token")
                return
            
            # Validate token format
            is_valid, error_msg = validate_github_token(token)
            if not is_valid:
                self.lbl_github_status.setStyleSheet("color: #C00000;")
                self.lbl_github_status.setText(f"⚠ {error_msg}")
                return
            
            # Test connection
            self.lbl_github_status.setStyleSheet("color: #666666;")
            self.lbl_github_status.setText("⏳ Testing connection...")
            self.btn_test_github.setEnabled(False)
            
            # Create API instance and test
            github_api = GitHubAPI(token, username)
            success, message = github_api.test_connection()
            
            if success:
                self.lbl_github_status.setStyleSheet("color: #00B050;")
                self.lbl_github_status.setText(f"✓ {message}")
                self.logger.info("GitHub connection test successful")
            else:
                self.lbl_github_status.setStyleSheet("color: #C00000;")
                self.lbl_github_status.setText(f"✗ {message}")
                self.logger.error(f"GitHub connection test failed: {message}")
            
        except Exception as e:
            self.lbl_github_status.setStyleSheet("color: #C00000;")
            self.lbl_github_status.setText(f"✗ Error: {str(e)}")
            self.logger.error(f"GitHub connection test error: {e}")
        finally:
            self.btn_test_github.setEnabled(True)
    
    def test_tailscale_connection(self):
        """Test Tailscale API connection"""
        try:
            api_key = self.txt_tailscale_api.text().strip()
            network = self.txt_tailscale_network.text().strip()
            
            if not api_key or not network:
                self.lbl_tailscale_status.setStyleSheet("color: #C00000;")
                self.lbl_tailscale_status.setText("⚠ Please enter both API key and network name")
                return
            
            # Validate key format
            is_valid, error_msg = validate_tailscale_key(api_key)
            if not is_valid:
                self.lbl_tailscale_status.setStyleSheet("color: #C00000;")
                self.lbl_tailscale_status.setText(f"⚠ {error_msg}")
                return
            
            # Test connection
            self.lbl_tailscale_status.setStyleSheet("color: #666666;")
            self.lbl_tailscale_status.setText("⏳ Testing connection...")
            self.btn_test_tailscale.setEnabled(False)
            
            # Create API instance and test
            tailscale_api = TailscaleAPI(api_key, network)
            success, message = tailscale_api.test_connection()
            
            if success:
                self.lbl_tailscale_status.setStyleSheet("color: #00B050;")
                self.lbl_tailscale_status.setText(f"✓ {message}")
                self.logger.info("Tailscale connection test successful")
            else:
                self.lbl_tailscale_status.setStyleSheet("color: #C00000;")
                self.lbl_tailscale_status.setText(f"✗ {message}")
                self.logger.error(f"Tailscale connection test failed: {message}")
            
        except Exception as e:
            self.lbl_tailscale_status.setStyleSheet("color: #C00000;")
            self.lbl_tailscale_status.setText(f"✗ Error: {str(e)}")
            self.logger.error(f"Tailscale connection test error: {e}")
        finally:
            self.btn_test_tailscale.setEnabled(True)
    
    def get_config(self):
        """Get configuration from this tab"""
        return {
            'github_username': self.txt_github_username.text().strip(),
            'github_token': self.txt_github_token.text().strip(),
            'tailscale_api': self.txt_tailscale_api.text().strip(),
            'tailscale_network': self.txt_tailscale_network.text().strip()
        }
    
    def set_config(self, config):
        """Set configuration to this tab"""
        self.txt_github_username.setText(config.get('github_username', ''))
        self.txt_github_token.setText(config.get('github_token', ''))
        self.txt_tailscale_api.setText(config.get('tailscale_api', ''))
        self.txt_tailscale_network.setText(config.get('tailscale_network', ''))
