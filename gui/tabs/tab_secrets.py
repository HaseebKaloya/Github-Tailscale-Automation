"""
Secrets Tab for Github&Tailscale-Automation
Author: Haseeb Kaloya

Secrets management for repositories
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QFileDialog, QMessageBox, QButtonGroup, QListWidget,
    QListWidgetItem, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pathlib import Path

from utils.helpers import read_lines_from_file
from utils.logger import get_logger
from core.constants import FILTER_TEXT
from gui.responsive_widgets import ResponsiveContainer, OptimalFormLayout
from gui.styles import GROUPBOX_STYLE, INPUT_STYLE, BUTTON_PRIMARY, RADIO_STYLE, BUTTON_SUCCESS

class TabSecrets(QWidget):
    """Secrets tab widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.logger = get_logger()
        
        # Store custom repository secrets
        self.repository_secrets = []  # List of {name, source, value, file_path}
        
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
        
        # Shared Secrets Section
        self.create_shared_secrets_section(content_layout)
        
        # Repository Secrets Section
        self.create_repository_secrets_section(content_layout)
        
        # Spacer
        content_layout.addStretch()
    
    def create_shared_secrets_section(self, parent_layout):
        """Create shared secrets section"""
        group_box = QGroupBox("Shared Secrets (Same for All Repositories)")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(18)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Info label
        info = QLabel("Add secrets that will be the same across all repositories (e.g., API keys, tokens)")
        info.setWordWrap(True)
        info.setStyleSheet("""
            color: #0078D4;
            font-size: 10pt;
            padding: 10px;
            background-color: transparent;
            border-left: 3px solid #0078D4;
            border-radius: 4px;
        """)
        layout.addWidget(info)
        
        # File path
        self.txt_secrets_file = QLineEdit()
        self.txt_secrets_file.setPlaceholderText("Select file with KEY=VALUE pairs...")
        self.txt_secrets_file.setReadOnly(True)
        self.txt_secrets_file.setStyleSheet(INPUT_STYLE)
        self.txt_secrets_file.setMinimumHeight(40)
        
        btn_browse = QPushButton("Browse...")
        btn_browse.setFixedSize(120, 40)
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.setStyleSheet(BUTTON_PRIMARY)
        btn_browse.clicked.connect(self.browse_secrets_file)
        
        path_row = OptimalFormLayout.create_field_row(
            "File:",
            self.txt_secrets_file,
            btn_browse,
            label_width=80
        )
        layout.addLayout(path_row)
        
        # Status label
        self.lbl_secrets_status = QLabel("")
        self.lbl_secrets_status.setAlignment(Qt.AlignCenter)
        self.lbl_secrets_status.setStyleSheet("""
            QLabel {
                color: #00B050;
                font-weight: bold;
                padding: 8px;
                background-color: transparent;
                border-radius: 4px;
                font-size: 10pt;
            }
        """)
        layout.addWidget(self.lbl_secrets_status)
        
        # Format example
        example = QLabel("Format: KEY=VALUE (one per line)\nExample:\nGITHUB_TOKEN=ghp_xxxxx\nAPI_KEY=abc123")
        example.setStyleSheet("""
            color: #666666;
            font-family: Consolas;
            font-size: 9pt;
            padding: 10px;
            background-color: transparent;
            border-radius: 4px;
        """)
        layout.addWidget(example)
        
        parent_layout.addWidget(group_box)
    
    def create_repository_secrets_section(self, parent_layout):
        """Create repository secrets section with custom names"""
        group_box = QGroupBox("Repository Secrets (Per-Repository with Custom Names)")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(18)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Info label
        info = QLabel("Add custom secrets for each repository. Each repository gets its own unique Tailscale key!")
        info.setWordWrap(True)
        info.setStyleSheet("""
            color: #0078D4;
            font-size: 10pt;
            padding: 10px;
            background-color: transparent;
            border-left: 3px solid #0078D4;
            border-radius: 4px;
        """)
        layout.addWidget(info)
        
        # Input form for adding secrets
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(12)
        
        # Secret Name input
        name_label = QLabel("Secret Name:")
        name_label.setStyleSheet("font-weight: bold; font-size: 10pt; color: #333; background-color: transparent;")
        form_layout.addWidget(name_label)
        
        self.txt_secret_name = QLineEdit()
        self.txt_secret_name.setPlaceholderText("e.g., TAILSCALE_KEY, TS_AUTH, MY_CUSTOM_SECRET")
        self.txt_secret_name.setStyleSheet(INPUT_STYLE)
        self.txt_secret_name.setMinimumHeight(40)
        form_layout.addWidget(self.txt_secret_name)
        
        # Value source
        source_label = QLabel("Secret Value Source:")
        source_label.setStyleSheet("font-weight: bold; font-size: 10pt; color: #333; margin-top: 8px; background-color: transparent;")
        form_layout.addWidget(source_label)
        
        # Radio button group for value source
        self.secret_source_group = QButtonGroup()
        
        # Option 1: Tailscale auto-generate (per-repo)
        self.radio_use_tailscale = QRadioButton("Use Tailscale Auth Key (unique per repository)")
        self.radio_use_tailscale.setChecked(True)
        self.radio_use_tailscale.setStyleSheet(RADIO_STYLE + " font-size: 10pt; padding: 5px;")
        self.radio_use_tailscale.toggled.connect(self.on_secret_source_changed)
        self.secret_source_group.addButton(self.radio_use_tailscale)
        form_layout.addWidget(self.radio_use_tailscale)
        
        # Option 2: Custom value (same for all)
        custom_value_layout = QHBoxLayout()
        self.radio_custom_value = QRadioButton("Use Custom Value:")
        self.radio_custom_value.setStyleSheet(RADIO_STYLE + " font-size: 10pt; padding: 5px;")
        self.radio_custom_value.toggled.connect(self.on_secret_source_changed)
        self.secret_source_group.addButton(self.radio_custom_value)
        custom_value_layout.addWidget(self.radio_custom_value)
        
        self.txt_custom_value = QLineEdit()
        self.txt_custom_value.setPlaceholderText("Enter value (same for all repositories)...")
        self.txt_custom_value.setEnabled(False)
        self.txt_custom_value.setStyleSheet(INPUT_STYLE)
        self.txt_custom_value.setMinimumHeight(35)
        custom_value_layout.addWidget(self.txt_custom_value)
        form_layout.addLayout(custom_value_layout)
        
        # Option 3: Import from file (per-repo)
        file_layout = QHBoxLayout()
        self.radio_import_values = QRadioButton("Import from File:")
        self.radio_import_values.setStyleSheet(RADIO_STYLE + " font-size: 10pt; padding: 5px;")
        self.radio_import_values.toggled.connect(self.on_secret_source_changed)
        self.secret_source_group.addButton(self.radio_import_values)
        file_layout.addWidget(self.radio_import_values)
        
        self.txt_values_file = QLineEdit()
        self.txt_values_file.setPlaceholderText("Select file (one value per line)...")
        self.txt_values_file.setEnabled(False)
        self.txt_values_file.setReadOnly(True)
        self.txt_values_file.setStyleSheet(INPUT_STYLE)
        self.txt_values_file.setMinimumHeight(35)
        file_layout.addWidget(self.txt_values_file)
        
        self.btn_browse_values = QPushButton("Browse")
        self.btn_browse_values.setFixedSize(100, 35)
        self.btn_browse_values.setEnabled(False)
        self.btn_browse_values.setCursor(Qt.PointingHandCursor)
        self.btn_browse_values.setStyleSheet(BUTTON_PRIMARY)
        self.btn_browse_values.clicked.connect(self.browse_values_file)
        file_layout.addWidget(self.btn_browse_values)
        form_layout.addLayout(file_layout)
        
        # Add Secret button
        btn_add_secret = QPushButton("Add Secret")
        btn_add_secret.setFixedHeight(40)
        btn_add_secret.setCursor(Qt.PointingHandCursor)
        btn_add_secret.setStyleSheet(BUTTON_SUCCESS)
        btn_add_secret.clicked.connect(self.add_repository_secret)
        form_layout.addWidget(btn_add_secret)
        
        layout.addWidget(form_frame)
        
        # List of added secrets
        list_label = QLabel("Added Repository Secrets:")
        list_label.setStyleSheet("font-weight: bold; font-size: 10pt; color: #333; margin-top: 10px; background-color: transparent;")
        layout.addWidget(list_label)
        
        self.list_secrets = QListWidget()
        self.list_secrets.setStyleSheet("""
            QListWidget {
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
                padding: 5px;
                font-size: 10pt;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #F0F0F0;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #F0F8FF;
            }
            QListWidget::item:selected {
                background-color: #E3F2FD;
                color: #0078D4;
            }
        """)
        self.list_secrets.setMinimumHeight(150)
        self.list_secrets.setMaximumHeight(250)
        layout.addWidget(self.list_secrets)
        
        # Remove button
        btn_remove_secret = QPushButton("Remove Selected Secret")
        btn_remove_secret.setFixedHeight(35)
        btn_remove_secret.setCursor(Qt.PointingHandCursor)
        btn_remove_secret.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 10pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
            QPushButton:pressed {
                background-color: #B91C1C;
            }
        """)
        btn_remove_secret.clicked.connect(self.remove_repository_secret)
        layout.addWidget(btn_remove_secret)
        
        # Example
        example = QLabel(
            "Example: Add secret named 'MY_TAILSCALE_KEY' using Tailscale Auth Key.\n"
            "    Result: 20 repos -> 20 unique keys, each added as 'MY_TAILSCALE_KEY'"
        )
        example.setStyleSheet("""
            color: #666666;
            font-size: 9pt;
            padding: 10px;
            background-color: transparent;
            border-radius: 4px;
            border-left: 3px solid #10B981;
        """)
        layout.addWidget(example)
        
        parent_layout.addWidget(group_box)
    
    
    def on_secret_source_changed(self):
        """Handle repository secret source option change"""
        use_custom = self.radio_custom_value.isChecked()
        use_import = self.radio_import_values.isChecked()
        
        self.txt_custom_value.setEnabled(use_custom)
        self.txt_values_file.setEnabled(use_import)
        self.btn_browse_values.setEnabled(use_import)
    
    def validate_secret_name(self, name):
        """Validate secret name (uppercase, numbers, underscores only)"""
        if not name:
            return False, "Secret name cannot be empty"
        
        # Check format (only uppercase letters, numbers, underscores)
        import re
        if not re.match(r'^[A-Z0-9_]+$', name):
            return False, "Secret name must contain only uppercase letters, numbers, and underscores"
        
        # Check for duplicates
        for secret in self.repository_secrets:
            if secret['name'].upper() == name.upper():
                return False, f"Secret '{name}' already exists"
        
        return True, ""
    
    def add_repository_secret(self):
        """Add a repository secret to the list"""
        # Get and validate secret name
        secret_name = self.txt_secret_name.text().strip().upper()
        
        is_valid, error_msg = self.validate_secret_name(secret_name)
        if not is_valid:
            QMessageBox.warning(self, "Invalid Secret Name", error_msg)
            return
        
        # Determine source
        if self.radio_use_tailscale.isChecked():
            source = 'tailscale_auto'
            value = ''
            file_path = ''
            display_source = "Tailscale (unique per repo)"
        elif self.radio_custom_value.isChecked():
            source = 'custom_value'
            value = self.txt_custom_value.text().strip()
            file_path = ''
            
            if not value:
                QMessageBox.warning(self, "Empty Value", "Please enter a custom value")
                return
            
            display_source = f"Custom: {value[:20]}..." if len(value) > 20 else f"Custom: {value}"
        else:  # Import from file
            source = 'import_file'
            value = ''
            file_path = self.txt_values_file.text().strip()
            
            if not file_path:
                QMessageBox.warning(self, "No File Selected", "Please select a file to import values from")
                return
            
            if not Path(file_path).exists():
                QMessageBox.warning(self, "File Not Found", f"The file does not exist:\n{file_path}")
                return
            
            display_source = f"File: {Path(file_path).name}"
        
        # Add to list
        secret_data = {
            'name': secret_name,
            'source': source,
            'value': value,
            'file_path': file_path
        }
        self.repository_secrets.append(secret_data)
        
        # Add to list widget
        list_item = QListWidgetItem(f"{secret_name} -> {display_source}")
        list_item.setData(Qt.UserRole, secret_data)
        self.list_secrets.addItem(list_item)
        
        # Clear inputs
        self.txt_secret_name.clear()
        self.txt_custom_value.clear()
        self.txt_values_file.clear()
        self.radio_use_tailscale.setChecked(True)
        
        self.logger.info(f"Added repository secret: {secret_name} (source: {source})")
        
        # Show success message
        QMessageBox.information(
            self,
            "Secret Added",
            f"✅ Secret '{secret_name}' added successfully!\n\n"
            f"This secret will be added to each repository you create."
        )
    
    def remove_repository_secret(self):
        """Remove selected repository secret from the list"""
        current_item = self.list_secrets.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a secret to remove")
            return
        
        # Get secret data
        secret_data = current_item.data(Qt.UserRole)
        secret_name = secret_data['name']
        
        # Confirm removal
        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove the secret '{secret_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Remove from list
            row = self.list_secrets.row(current_item)
            self.list_secrets.takeItem(row)
            
            # Remove from data
            self.repository_secrets = [s for s in self.repository_secrets if s['name'] != secret_name]
            
            self.logger.info(f"Removed repository secret: {secret_name}")
    
    def browse_values_file(self):
        """Browse for values file (per-repository values)"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Values File (one value per line)",
            "",
            FILTER_TEXT
        )
        
        if filename:
            try:
                # Count values
                values = read_lines_from_file(filename)
                
                if values:
                    self.txt_values_file.setText(filename)
                    self.logger.info(f"Values file loaded: {filename} ({len(values)} values)")
                    
                    QMessageBox.information(
                        self,
                        "File Loaded",
                        f"✓ Found {len(values)} values in file.\n\n"
                        f"Make sure you have at least as many values as repositories!"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Empty File",
                        "The selected file is empty."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to read file:\n{str(e)}"
                )
                self.logger.error(f"Error reading values file: {e}")
    
    def browse_secrets_file(self):
        """Browse for shared secrets file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Shared Secrets File",
            "",
            FILTER_TEXT
        )
        
        if filename:
            try:
                # Count secrets
                lines = read_lines_from_file(filename)
                secrets = [l for l in lines if '=' in l]
                
                if secrets:
                    self.txt_secrets_file.setText(filename)
                    self.lbl_secrets_status.setText(f"✓ Found {len(secrets)} secrets in file")
                    self.lbl_secrets_status.setStyleSheet("color: #00B050;")
                    self.logger.info(f"Secrets file loaded: {filename} ({len(secrets)} secrets)")
                else:
                    QMessageBox.warning(
                        self,
                        "Invalid File",
                        "No valid KEY=VALUE pairs found in file."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to read file:\n{str(e)}"
                )
                self.logger.error(f"Error reading secrets file: {e}")
    
    def get_config(self):
        """Get configuration from this tab"""
        return {
            'shared_secrets_file': self.txt_secrets_file.text().strip(),
            'repository_secrets': self.repository_secrets.copy()
        }
    
    def set_config(self, config):
        """Set configuration to this tab"""
        self.txt_secrets_file.setText(config.get('shared_secrets_file', ''))
        
        # Restore repository secrets
        self.repository_secrets = config.get('repository_secrets', []).copy() if config.get('repository_secrets') else []
        
        # BACKWARD COMPATIBILITY: Auto-migrate old Tailscale config to new system
        # If old config had auto_generate_tailscale=True and no repository_secrets, create default
        if config.get('auto_generate_tailscale') and not self.repository_secrets:
            default_secret = {
                'name': 'TAILSCALE_AUTH_KEY',
                'source': 'tailscale_auto',
                'value': '',
                'file_path': ''
            }
            self.repository_secrets.append(default_secret)
            self.logger.info("Auto-migrated old Tailscale config to new repository secrets format")
        
        # If old config had tailscale_keys_file and no repository_secrets, create default
        elif config.get('tailscale_keys_file') and not self.repository_secrets:
            default_secret = {
                'name': 'TAILSCALE_AUTH_KEY',
                'source': 'import_file',
                'value': '',
                'file_path': config['tailscale_keys_file']
            }
            self.repository_secrets.append(default_secret)
            self.logger.info("Auto-migrated old Tailscale file config to new repository secrets format")
        
        # Display all repository secrets
        self.list_secrets.clear()
        
        for secret in self.repository_secrets:
            # Determine display source
            if secret['source'] == 'tailscale_auto':
                display_source = "✨ Tailscale (unique per repo)"
            elif secret['source'] == 'custom_value':
                value_preview = secret['value'][:20] + "..." if len(secret['value']) > 20 else secret['value']
                display_source = f"📝 Custom: {value_preview}"
            else:  # import_file
                file_name = Path(secret['file_path']).name if secret['file_path'] else "Unknown"
                display_source = f"📂 File: {file_name}"
            
            # Add to list widget
            list_item = QListWidgetItem(f"🔐 {secret['name']}  →  {display_source}")
            list_item.setData(Qt.UserRole, secret)
            self.list_secrets.addItem(list_item)
