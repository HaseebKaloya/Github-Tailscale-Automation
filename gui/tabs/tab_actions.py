"""
Actions Tab for Github&Tailscale-Automation
Author: Haseeb Kaloya

Workflow actions and automation options
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QCheckBox, QSpinBox, QLineEdit, QComboBox
)
from PyQt5.QtGui import QFont

from utils.logger import get_logger
from gui.responsive_widgets import ResponsiveContainer
from gui.styles import GROUPBOX_STYLE, CHECKBOX_STYLE

class TabActions(QWidget):
    """Actions tab widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.logger = get_logger()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        # Create responsive container
        container = ResponsiveContainer(self, max_width=950)
        
        # Set container as main widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        
        # Get content layout from container
        content_layout = container.get_layout()
        
        # Workflow & Actions Options
        self.create_workflow_section(content_layout)
        
        # Repository Settings
        self.create_repository_settings_section(content_layout)
        
        # Branch Protection
        self.create_branch_protection_section(content_layout)
        
        # GitHub Pages
        self.create_github_pages_section(content_layout)
        
        # Backup & Logging Options
        self.create_backup_section(content_layout)
        
        # Spacer
        content_layout.addStretch()
    
    def create_workflow_section(self, parent_layout):
        """Create enhanced workflow options section"""
        group_box = QGroupBox("Workflow & Actions")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Start workflows checkbox
        self.chk_start_workflows = QCheckBox("Start GitHub Actions workflows after creation")
        self.chk_start_workflows.setChecked(True)
        self.chk_start_workflows.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px;")
        layout.addWidget(self.chk_start_workflows)
        
        # Wait for completion checkbox
        self.chk_wait_workflow = QCheckBox("Wait for workflow completion")
        self.chk_wait_workflow.setChecked(False)
        self.chk_wait_workflow.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px;")
        layout.addWidget(self.chk_wait_workflow)
        
        # Retry on failure checkbox
        self.chk_retry_workflow = QCheckBox("Retry failed workflows")
        self.chk_retry_workflow.setChecked(False)
        self.chk_retry_workflow.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px;")
        layout.addWidget(self.chk_retry_workflow)
        
        # Workflow timeout
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("Workflow Timeout:")
        timeout_label.setStyleSheet("font-size: 10pt; color: #333; font-weight: bold; background-color: transparent;")
        timeout_layout.addWidget(timeout_label)
        
        self.spin_workflow_timeout = QSpinBox()
        self.spin_workflow_timeout.setMinimum(5)
        self.spin_workflow_timeout.setMaximum(60)
        self.spin_workflow_timeout.setValue(30)
        self.spin_workflow_timeout.setSuffix(" minutes")
        self.spin_workflow_timeout.setStyleSheet("""
            QSpinBox {
                padding: 5px 10px;
                font-size: 10pt;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
            }
            QSpinBox:focus {
                border-color: #0078D4;
            }
        """)
        timeout_layout.addWidget(self.spin_workflow_timeout)
        timeout_layout.addStretch()
        layout.addLayout(timeout_layout)
        
        # Info label
        info = QLabel("Workflows will be triggered immediately after repository creation. Timeout applies if waiting for completion.")
        info.setWordWrap(True)
        info.setStyleSheet("""
            color: #0078D4;
            font-size: 9pt;
            padding: 10px;
            background-color: transparent;
            border-left: 3px solid #0078D4;
            border-radius: 4px;
        """)
        layout.addWidget(info)
        
        parent_layout.addWidget(group_box)
    
    def create_repository_settings_section(self, parent_layout):
        """Create repository settings section"""
        group_box = QGroupBox("Repository Settings")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Enable Issues
        self.chk_enable_issues = QCheckBox("Enable Issues")
        self.chk_enable_issues.setChecked(True)
        self.chk_enable_issues.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px;")
        layout.addWidget(self.chk_enable_issues)
        
        # Enable Wiki
        self.chk_enable_wiki = QCheckBox("Enable Wiki")
        self.chk_enable_wiki.setChecked(False)
        self.chk_enable_wiki.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px;")
        layout.addWidget(self.chk_enable_wiki)
        
        # Enable Projects
        self.chk_enable_projects = QCheckBox("Enable Projects")
        self.chk_enable_projects.setChecked(False)
        self.chk_enable_projects.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px;")
        layout.addWidget(self.chk_enable_projects)
        
        # Repository Topics
        topics_layout = QHBoxLayout()
        topics_label = QLabel("Topics:")
        topics_label.setStyleSheet("font-size: 10pt; color: #333; font-weight: bold; background-color: transparent;")
        topics_layout.addWidget(topics_label)
        
        self.txt_repo_topics = QLineEdit()
        self.txt_repo_topics.setPlaceholderText("e.g., python, automation, github (comma-separated)")
        self.txt_repo_topics.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                font-size: 10pt;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #0078D4;
            }
        """)
        topics_layout.addWidget(self.txt_repo_topics)
        layout.addLayout(topics_layout)
        
        # Info label
        info = QLabel("Configure repository features. Topics help others discover your repositories.")
        info.setWordWrap(True)
        info.setStyleSheet("""
            color: #00B050;
            font-size: 9pt;
            padding: 10px;
            background-color: transparent;
            border-left: 3px solid #00B050;
            border-radius: 4px;
        """)
        layout.addWidget(info)
        
        parent_layout.addWidget(group_box)
    
    def create_branch_protection_section(self, parent_layout):
        """Create branch protection section"""
        group_box = QGroupBox("Branch Protection")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Protect main branch
        self.chk_protect_main = QCheckBox("Protect main branch")
        self.chk_protect_main.setChecked(False)
        self.chk_protect_main.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px;")
        layout.addWidget(self.chk_protect_main)
        
        # Require PR reviews
        self.chk_require_reviews = QCheckBox("Require pull request reviews before merging")
        self.chk_require_reviews.setChecked(False)
        self.chk_require_reviews.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px; margin-left: 30px;")
        layout.addWidget(self.chk_require_reviews)
        
        # Require status checks
        self.chk_require_checks = QCheckBox("Require status checks to pass before merging")
        self.chk_require_checks.setChecked(False)
        self.chk_require_checks.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px; margin-left: 30px;")
        layout.addWidget(self.chk_require_checks)
        
        # Restrict pushes
        self.chk_restrict_push = QCheckBox("Restrict who can push to main branch")
        self.chk_restrict_push.setChecked(False)
        self.chk_restrict_push.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px; margin-left: 30px;")
        layout.addWidget(self.chk_restrict_push)
        
        # Info label
        info = QLabel("Branch protection rules help maintain code quality and prevent accidental changes.")
        info.setWordWrap(True)
        info.setStyleSheet("""
            color: #FF6B35;
            font-size: 9pt;
            padding: 10px;
            background-color: transparent;
            border-left: 3px solid #FF6B35;
            border-radius: 4px;
        """)
        layout.addWidget(info)
        
        parent_layout.addWidget(group_box)
    
    def create_github_pages_section(self, parent_layout):
        """Create GitHub Pages section"""
        group_box = QGroupBox("GitHub Pages")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Enable GitHub Pages
        self.chk_enable_pages = QCheckBox("Enable GitHub Pages")
        self.chk_enable_pages.setChecked(False)
        self.chk_enable_pages.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px;")
        layout.addWidget(self.chk_enable_pages)
        
        # Pages source
        source_layout = QHBoxLayout()
        source_label = QLabel("Source:")
        source_label.setStyleSheet("font-size: 10pt; color: #333; font-weight: bold; margin-left: 30px; background-color: transparent;")
        source_layout.addWidget(source_label)
        
        self.combo_pages_source = QComboBox()
        self.combo_pages_source.addItems(["main branch /root", "main branch /docs", "gh-pages branch"])
        self.combo_pages_source.setStyleSheet("""
            QComboBox {
                padding: 5px 10px;
                font-size: 10pt;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #0078D4;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
        """)
        source_layout.addWidget(self.combo_pages_source)
        source_layout.addStretch()
        layout.addLayout(source_layout)
        
        # Info label
        info = QLabel("GitHub Pages allows you to host websites directly from your repository.")
        info.setWordWrap(True)
        info.setStyleSheet("""
            color: #7C3AED;
            font-size: 9pt;
            padding: 10px;
            background-color: transparent;
            border-left: 3px solid #7C3AED;
            border-radius: 4px;
        """)
        layout.addWidget(info)
        
        parent_layout.addWidget(group_box)
    
    def create_backup_section(self, parent_layout):
        """Create backup options section"""
        group_box = QGroupBox("Backup & Logging")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(18)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Auto-backup checkbox
        self.chk_auto_backup = QCheckBox("Auto-save Tailscale keys to backup file")
        self.chk_auto_backup.setChecked(True)
        self.chk_auto_backup.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px;")
        layout.addWidget(self.chk_auto_backup)
        
        # Detailed logging checkbox
        self.chk_detailed_logging = QCheckBox("Enable detailed logging")
        self.chk_detailed_logging.setChecked(True)
        self.chk_detailed_logging.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 8px;")
        layout.addWidget(self.chk_detailed_logging)
        
        # Info label
        info = QLabel("Backups and logs are saved in the backups/ and logs/ folders respectively.")
        info.setWordWrap(True)
        info.setStyleSheet("""
            color: #00B050;
            font-size: 10pt;
            padding: 10px;
            background-color: transparent;
            border-left: 3px solid #00B050;
            border-radius: 4px;
        """)
        layout.addWidget(info)
        
        parent_layout.addWidget(group_box)
    
    def get_config(self):
        """Get configuration from this tab"""
        # Parse topics
        topics_text = self.txt_repo_topics.text().strip()
        topics = [t.strip() for t in topics_text.split(',') if t.strip()] if topics_text else []
        
        return {
            # Workflow options
            'start_workflows': self.chk_start_workflows.isChecked(),
            'wait_workflow_completion': self.chk_wait_workflow.isChecked(),
            'retry_failed_workflows': self.chk_retry_workflow.isChecked(),
            'workflow_timeout': self.spin_workflow_timeout.value(),
            
            # Repository settings
            'enable_issues': self.chk_enable_issues.isChecked(),
            'enable_wiki': self.chk_enable_wiki.isChecked(),
            'enable_projects': self.chk_enable_projects.isChecked(),
            'repo_topics': topics,
            
            # Branch protection
            'protect_main_branch': self.chk_protect_main.isChecked(),
            'require_pr_reviews': self.chk_require_reviews.isChecked(),
            'require_status_checks': self.chk_require_checks.isChecked(),
            'restrict_push_access': self.chk_restrict_push.isChecked(),
            
            # GitHub Pages
            'enable_github_pages': self.chk_enable_pages.isChecked(),
            'pages_source': self.combo_pages_source.currentText(),
            
            # Backup & Logging
            'auto_backup': self.chk_auto_backup.isChecked(),
            'detailed_logging': self.chk_detailed_logging.isChecked()
        }
    
    def set_config(self, config):
        """Set configuration to this tab"""
        # Workflow options
        self.chk_start_workflows.setChecked(config.get('start_workflows', True))
        self.chk_wait_workflow.setChecked(config.get('wait_workflow_completion', False))
        self.chk_retry_workflow.setChecked(config.get('retry_failed_workflows', False))
        self.spin_workflow_timeout.setValue(config.get('workflow_timeout', 30))
        
        # Repository settings
        self.chk_enable_issues.setChecked(config.get('enable_issues', True))
        self.chk_enable_wiki.setChecked(config.get('enable_wiki', False))
        self.chk_enable_projects.setChecked(config.get('enable_projects', False))
        
        # Topics
        topics = config.get('repo_topics', [])
        if topics:
            self.txt_repo_topics.setText(', '.join(topics))
        
        # Branch protection
        self.chk_protect_main.setChecked(config.get('protect_main_branch', False))
        self.chk_require_reviews.setChecked(config.get('require_pr_reviews', False))
        self.chk_require_checks.setChecked(config.get('require_status_checks', False))
        self.chk_restrict_push.setChecked(config.get('restrict_push_access', False))
        
        # GitHub Pages
        self.chk_enable_pages.setChecked(config.get('enable_github_pages', False))
        pages_source = config.get('pages_source', 'main branch /root')
        index = self.combo_pages_source.findText(pages_source)
        if index >= 0:
            self.combo_pages_source.setCurrentIndex(index)
        
        # Backup & Logging
        self.chk_auto_backup.setChecked(config.get('auto_backup', True))
        self.chk_detailed_logging.setChecked(config.get('detailed_logging', True))
