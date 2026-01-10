"""
Monitor Tab for Github&Tailscale-Automation
Author: Haseeb Kaloya

Repository status monitoring (simplified version)
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from datetime import datetime

from gui.responsive_widgets import ResponsiveContainer
from gui.styles import GROUPBOX_STYLE, BUTTON_PRIMARY

class TabMonitor(QWidget):
    """Monitor tab widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.repositories = []
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_status)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        # Create responsive container
        container = ResponsiveContainer(self, max_width=1400)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        content_layout = container.get_layout()
        
        # Stats section
        self.create_stats_section(content_layout)
        
        # Repository table section
        self.create_table_section(content_layout)
        
        # Control buttons
        self.create_controls_section(content_layout)
        
        content_layout.addStretch()
    
    def create_stats_section(self, parent_layout):
        """Create statistics cards section"""
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        # Total Repositories
        self.lbl_total = self.create_stat_card("📦 Total Repositories", "0", "#0078D4")
        stats_layout.addWidget(self.lbl_total)
        
        # Active
        self.lbl_active = self.create_stat_card("✅ Active", "0", "#00B050")
        stats_layout.addWidget(self.lbl_active)
        
        # Pending
        self.lbl_pending = self.create_stat_card("⏳ Pending", "0", "#FFA500")
        stats_layout.addWidget(self.lbl_pending)
        
        # Failed
        self.lbl_failed = self.create_stat_card("❌ Failed", "0", "#C00000")
        stats_layout.addWidget(self.lbl_failed)
        
        parent_layout.addLayout(stats_layout)
    
    def create_stat_card(self, title, value, color):
        """Create a stat card widget"""
        card = QGroupBox()
        card.setStyleSheet(f"""
            QGroupBox {{
                background: white;
                border: 2px solid {color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {color}; font-weight: 600; font-size: 10pt;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 20pt;")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName("value_label")
        layout.addWidget(value_label)
        
        return card
    
    def create_table_section(self, parent_layout):
        """Create repository table section"""
        group_box = QGroupBox("📊 Repository Status")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Repository", "Status", "Created", "Updated", "Workflows", "Actions"
        ])
        
        # Style table
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: white;
                gridline-color: #E0E0E0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #0078D4;
                font-weight: 600;
                color: #333333;
            }
        """)
        
        # Configure table
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.table)
        
        # Info label
        info_label = QLabel("📝 Monitoring repository status and workflow activities")
        info_label.setStyleSheet("""
            color: #0078D4;
            font-size: 9pt;
            padding: 8px;
            background-color: #F0F8FF;
            border-left: 3px solid #0078D4;
            border-radius: 4px;
        """)
        layout.addWidget(info_label)
        
        parent_layout.addWidget(group_box)
    
    def create_controls_section(self, parent_layout):
        """Create control buttons section"""
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        # Refresh button
        btn_refresh = QPushButton("🔄 Refresh Status")
        btn_refresh.setFixedSize(150, 40)
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.setStyleSheet(BUTTON_PRIMARY)
        btn_refresh.clicked.connect(self.refresh_status)
        btn_layout.addWidget(btn_refresh)
        
        # Auto-refresh toggle
        self.btn_auto_refresh = QPushButton("⏸️ Auto-Refresh: OFF")
        self.btn_auto_refresh.setFixedSize(180, 40)
        self.btn_auto_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_auto_refresh.setStyleSheet(BUTTON_PRIMARY)
        self.btn_auto_refresh.clicked.connect(self.toggle_auto_refresh)
        btn_layout.addWidget(self.btn_auto_refresh)
        
        btn_layout.addStretch()
        
        # Last updated label
        self.lbl_last_update = QLabel("🕒 Last updated: Never")
        self.lbl_last_update.setStyleSheet("color: #666666; font-size: 9pt;")
        btn_layout.addWidget(self.lbl_last_update)
        
        parent_layout.addLayout(btn_layout)
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh timer"""
        if self.refresh_timer.isActive():
            self.refresh_timer.stop()
            self.btn_auto_refresh.setText("⏸️ Auto-Refresh: OFF")
        else:
            self.refresh_timer.start(30000)  # 30 seconds
            self.btn_auto_refresh.setText("▶️ Auto-Refresh: ON")
            self.refresh_status()
    
    def refresh_status(self):
        """Refresh repository status"""
        # Update last update time
        now = datetime.now().strftime("%H:%M:%S")
        self.lbl_last_update.setText(f"🕒 Last updated: {now}")
        
        # Get repositories from parent (if available)
        if hasattr(self.parent, 'tab_repositories'):
            # Simulate getting repository data
            # In real implementation, this would fetch from GitHub API
            self.update_sample_data()
    
    def update_sample_data(self):
        """Update with sample data for demonstration"""
        # Sample data
        sample_repos = [
            ("example-repo-1", "✅ Active", "2025-11-10", "2 hours ago", "5"),
            ("example-repo-2", "⏳ Pending", "2025-11-11", "1 hour ago", "3"),
            ("example-repo-3", "✅ Active", "2025-11-09", "5 hours ago", "8"),
        ]
        
        # Clear table
        self.table.setRowCount(0)
        
        # Populate table
        for idx, (name, status, created, updated, workflows) in enumerate(sample_repos):
            self.table.insertRow(idx)
            
            # Repository name
            self.table.setItem(idx, 0, QTableWidgetItem(name))
            
            # Status
            status_item = QTableWidgetItem(status)
            if "✅" in status:
                status_item.setForeground(QColor("#00B050"))
            elif "⏳" in status:
                status_item.setForeground(QColor("#FFA500"))
            elif "❌" in status:
                status_item.setForeground(QColor("#C00000"))
            self.table.setItem(idx, 1, status_item)
            
            # Other columns
            self.table.setItem(idx, 2, QTableWidgetItem(created))
            self.table.setItem(idx, 3, QTableWidgetItem(updated))
            self.table.setItem(idx, 4, QTableWidgetItem(workflows))
            
            # Actions button
            self.table.setItem(idx, 5, QTableWidgetItem("🔗 View"))
        
        # Update stats
        self.update_stats(len(sample_repos), 2, 1, 0)
    
    def update_stats(self, total, active, pending, failed):
        """Update statistics cards"""
        self.lbl_total.findChild(QLabel, "value_label").setText(str(total))
        self.lbl_active.findChild(QLabel, "value_label").setText(str(active))
        self.lbl_pending.findChild(QLabel, "value_label").setText(str(pending))
        self.lbl_failed.findChild(QLabel, "value_label").setText(str(failed))
    
    def get_config(self):
        """Get configuration from this tab"""
        return {}
    
    def set_config(self, config):
        """Set configuration to this tab"""
        pass
