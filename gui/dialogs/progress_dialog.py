"""
Progress Dialog for Github&Tailscale-Automation
Author: Haseeb Kaloya

Real-time progress tracking during repository creation
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QTextEdit, QGroupBox, QFrame, QSizePolicy, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from utils.logger import get_logger
from gui.theme import AppTheme
from gui.styles import GROUPBOX_STYLE, BUTTON_PRIMARY, BUTTON_SECONDARY

class ProgressDialog(QDialog):
    """Progress tracking dialog"""
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.logger = get_logger()
        self.cancel_requested = False
        
        # Statistics
        self.total_repos = 0
        self.created_repos = 0
        self.failed_repos = 0
        self.current_repo = 0
        
        self.init_ui()
    
    def center_window(self):
        """Center the window on the screen"""
        try:
            # Get screen geometry (fixed deprecated QDesktopWidget)
            screen = QApplication.primaryScreen().geometry()
            # Get window geometry
            window = self.geometry()
            # Calculate center position
            x = (screen.width() - window.width()) // 2
            y = (screen.height() - window.height()) // 2
            # Move window to center
            self.move(x, y)
        except Exception as e:
            self.logger.warning(f"Could not center window: {e}")
    
    def init_ui(self):
        """Initialize the enhanced UI with fixed size"""
        self.setWindowTitle("Repository Creation in Progress")
        self.setModal(True)
        
        # Adjusted size for better visibility - taller and slightly wider
        dialog_width = 850
        dialog_height = 700
        
        self.setMinimumSize(dialog_width, dialog_height)
        self.resize(dialog_width, dialog_height)
        
        # Center window on screen
        self.center_window()
        
        # Allow resizing for better user control
        self.setWindowFlags(
            Qt.Dialog |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint |
            Qt.WindowMaximizeButtonHint
        )
        
        # Apply AppTheme stylesheet
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {AppTheme.BG_MAIN};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("Repository Creation in Progress")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {AppTheme.PRIMARY};
                padding: 12px;
                background-color: {AppTheme.BG_CARD};
                border-radius: 8px;
                border: 2px solid {AppTheme.PRIMARY};
            }}
        """)
        layout.addWidget(title)
        
        # Statistics Cards
        self.create_stats_cards(layout)
        
        # Overall Progress Section
        self.create_overall_section(layout)
        
        # Current Step Section
        self.create_step_section(layout)
        
        # Activity Log Section
        self.create_log_section(layout)
        
        # Buttons
        self.create_buttons(layout)
    
    def create_stats_cards(self, parent_layout):
        """Create beautiful statistics cards"""
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(8)
        
        # Total Repositories Card
        self.lbl_stat_total = self.create_stat_card(
            "Total",
            "0",
            AppTheme.PRIMARY,
            AppTheme.BG_CARD
        )
        stats_layout.addWidget(self.lbl_stat_total)
        
        # Created Successfully Card
        self.lbl_stat_created = self.create_stat_card(
            "Created",
            "0",
            AppTheme.SUCCESS,
            AppTheme.BG_CARD
        )
        stats_layout.addWidget(self.lbl_stat_created)
        
        # In Progress Card
        self.lbl_stat_current = self.create_stat_card(
            "Current",
            "0",
            AppTheme.WARNING,
            AppTheme.BG_CARD
        )
        stats_layout.addWidget(self.lbl_stat_current)
        
        # Failed Card
        self.lbl_stat_failed = self.create_stat_card(
            "Failed",
            "0",
            AppTheme.ERROR,
            AppTheme.BG_CARD
        )
        stats_layout.addWidget(self.lbl_stat_failed)
        
        parent_layout.addLayout(stats_layout)
    
    def create_stat_card(self, title, value, border_color, bg_color):
        """Create a single stat card widget optimized for fixed dialog width"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 8px;
                padding: 12px;
                min-width: 160px;
                max-width: 180px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        layout.setContentsMargins(6, 6, 6, 6)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        title_label.setStyleSheet(f"color: {border_color}; border: none;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        value_label.setStyleSheet(f"color: {border_color}; border: none;")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName("value_label")
        layout.addWidget(value_label)
        
        return card
    
    def create_overall_section(self, parent_layout):
        """Create enhanced overall progress section"""
        group = QGroupBox("Overall Progress")
        group.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Label
        self.lbl_overall = QLabel("Initializing...")
        self.lbl_overall.setFont(QFont("Segoe UI", 10))
        self.lbl_overall.setStyleSheet(f"color: {AppTheme.TEXT_MAIN}; background-color: transparent; border: none;")
        layout.addWidget(self.lbl_overall)
        
        # Progress bar
        self.progress_overall = QProgressBar()
        self.progress_overall.setMinimum(0)
        self.progress_overall.setMaximum(100)
        self.progress_overall.setValue(0)
        self.progress_overall.setTextVisible(True)
        self.progress_overall.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {AppTheme.PRIMARY};
                border-radius: 6px;
                text-align: center;
                height: 28px;
                background-color: {AppTheme.INPUT_BG};
                font-weight: 600;
                color: {AppTheme.TEXT_MAIN};
                font-family: 'Segoe UI';
            }}
            QProgressBar::chunk {{
                background-color: {AppTheme.PRIMARY};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.progress_overall)
        
        parent_layout.addWidget(group)
    
    def create_step_section(self, parent_layout):
        """Create enhanced current step section"""
        group = QGroupBox("Current Activity")
        group.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Step label
        self.lbl_step = QLabel("Waiting to start...")
        self.lbl_step.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.lbl_step.setStyleSheet(f"color: {AppTheme.PRIMARY}; background-color: transparent; border: none;")
        layout.addWidget(self.lbl_step)
        
        # Activity label
        self.lbl_activity = QLabel("Ready to begin repository creation")
        self.lbl_activity.setFont(QFont("Segoe UI", 9))
        self.lbl_activity.setStyleSheet(f"color: {AppTheme.TEXT_SECONDARY}; background-color: transparent; border: none;")
        self.lbl_activity.setWordWrap(True)
        layout.addWidget(self.lbl_activity)
        
        parent_layout.addWidget(group)
    
    def create_log_section(self, parent_layout):
        """Create enhanced activity log section"""
        group = QGroupBox("Activity Log")
        group.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Text edit with modern styling - allowed to expand
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setFont(QFont("Consolas", 9))
        self.txt_log.setMinimumHeight(200) 
        self.txt_log.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.txt_log.setStyleSheet(f"""
            QTextEdit {{
                background-color: {AppTheme.INPUT_BG};
                border: 1px solid {AppTheme.INPUT_BORDER};
                border-radius: 6px;
                padding: 10px;
                color: {AppTheme.TEXT_MAIN};
                font-size: 8pt;
            }}
        """)
        # Add log with fixed height
        layout.addWidget(self.txt_log)
        
        parent_layout.addWidget(group)
    
    def create_buttons(self, parent_layout):
        """Create button section"""
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        # Minimize button
        self.btn_minimize = QPushButton("Minimize")
        self.btn_minimize.setFixedSize(120, 40)
        self.btn_minimize.setCursor(Qt.PointingHandCursor)
        self.btn_minimize.setStyleSheet(BUTTON_SECONDARY)
        self.btn_minimize.clicked.connect(self.showMinimized)
        btn_layout.addWidget(self.btn_minimize)
        
        # Cancel button
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setFixedSize(120, 40)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppTheme.ERROR};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-family: 'Segoe UI';
                font-weight: 600;
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: #C00000;
            }}
            QPushButton:disabled {{
                background-color: {AppTheme.BORDER};
                color: {AppTheme.TEXT_SECONDARY};
            }}
        """)
        self.btn_cancel.clicked.connect(self.on_cancel)
        btn_layout.addWidget(self.btn_cancel)
        
        parent_layout.addLayout(btn_layout)
    
    def update_progress(self, overall_percent, step_name, activity):
        """
        Update progress display
        
        Args:
            overall_percent: Overall progress percentage (0-100)
            step_name: Current step name
            activity: Current activity description
        """
        try:
            # Ensure progress is within bounds
            overall_percent = max(0, min(100, overall_percent))
            
            # Update overall progress
            self.progress_overall.setValue(overall_percent)
            self.lbl_overall.setText(f"Progress: {overall_percent}%")
            
            # Update step (no emojis)
            self.lbl_step.setText(step_name)
            
            # Update activity with better formatting
            self.lbl_activity.setText(activity)
            
            # Log activity with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.add_log(f"[{timestamp}] [{overall_percent}%] {activity}")
            
            # Force UI update
            self.repaint()
            
        except Exception as e:
            self.logger.error(f"Error updating progress: {e}")
    
    def update_stats(self, total=None, created=None, current=None, failed=None):
        """Update statistics cards"""
        try:
            if total is not None:
                self.total_repos = total
                total_label = self.lbl_stat_total.findChild(QLabel, "value_label")
                if total_label:
                    total_label.setText(str(total))
            
            if created is not None:
                self.created_repos = created
                created_label = self.lbl_stat_created.findChild(QLabel, "value_label")
                if created_label:
                    created_label.setText(str(created))
            
            if current is not None:
                self.current_repo = current
                current_label = self.lbl_stat_current.findChild(QLabel, "value_label")
                if current_label:
                    current_label.setText(str(current))
            
            if failed is not None:
                self.failed_repos = failed
                failed_label = self.lbl_stat_failed.findChild(QLabel, "value_label")
                if failed_label:
                    failed_label.setText(str(failed))
            
            # Update progress percentage based on completion
            if self.total_repos > 0:
                completion_percent = int((self.created_repos + self.failed_repos) / self.total_repos * 100)
                if completion_percent != self.progress_overall.value():
                    self.progress_overall.setValue(completion_percent)
        
        except Exception as e:
            self.logger.error(f"Error updating stats: {e}")
    
    def add_log(self, message):
        """Add message to activity log"""
        try:
            # Add color coding for different message types (no emojis)
            if '[SUCCESS]' in message or 'success' in message.lower():
                formatted_message = f'<span style="color: {AppTheme.SUCCESS};">{message}</span>'
            elif '[ERROR]' in message or 'error' in message.lower() or 'failed' in message.lower():
                formatted_message = f'<span style="color: {AppTheme.ERROR};">{message}</span>'
            elif '[WARNING]' in message or 'warning' in message.lower():
                formatted_message = f'<span style="color: {AppTheme.WARNING};">{message}</span>'
            else:
                formatted_message = message
            
            self.txt_log.append(formatted_message)
            
            # Auto-scroll to bottom
            scrollbar = self.txt_log.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            
            # Limit log size to prevent memory issues
            if self.txt_log.document().blockCount() > 1000:
                cursor = self.txt_log.textCursor()
                cursor.movePosition(cursor.Start)
                cursor.movePosition(cursor.Down, cursor.KeepAnchor, 100)
                cursor.removeSelectedText()
            
        except Exception as e:
            self.logger.error(f"Error adding log: {e}")
    
    def on_cancel(self):
        """Handle cancel button click"""
        from PyQt5.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self,
            "Confirm Cancellation",
            "Are you sure you want to cancel the operation?\n\n"
            "Repositories created so far will remain, but the process will stop.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.cancel_requested = True
            self.btn_cancel.setEnabled(False)
            self.btn_cancel.setText("Cancelling...")
            self.add_log("[ERROR] Cancellation requested by user")
            self.logger.info("User requested cancellation")
    
    def set_completed(self, success, message):
        """
        Mark operation as completed
        
        Args:
            success: Whether operation succeeded
            message: Completion message
        """
        try:
            if success:
                self.progress_overall.setValue(100)
                self.lbl_overall.setText("Completed Successfully!")
                self.lbl_overall.setStyleSheet(f"color: {AppTheme.SUCCESS}; font-weight: bold; background-color: transparent; border: none;")
                self.add_log(f"[SUCCESS] {message}")
            else:
                self.lbl_overall.setText("Operation Failed")
                self.lbl_overall.setStyleSheet(f"color: {AppTheme.ERROR}; font-weight: bold; background-color: transparent; border: none;")
                self.add_log(f"[ERROR] {message}")
            
            # Update buttons
            self.btn_cancel.setEnabled(False)
            self.btn_cancel.setText("Close")
            self.btn_cancel.setStyleSheet(BUTTON_SECONDARY)
            self.btn_cancel.clicked.disconnect()
            self.btn_cancel.clicked.connect(self.accept)
            
        except Exception as e:
            self.logger.error(f"Error setting completed: {e}")
    
    def closeEvent(self, event):
        """Handle close event"""
        # Prevent closing during operation
        if not self.cancel_requested and self.btn_cancel.isEnabled():
            event.ignore()
        else:
            event.accept()
