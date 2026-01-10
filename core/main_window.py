"""
Main Window for Github&Tailscale-Automation
Author: Haseeb Kaloya
Email: haseebkaloya@gmail.com

Main application window with modern sidebar navigation
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QStackedWidget, QMessageBox,
    QFileDialog, QApplication, QFrame
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

from core.config_manager import ConfigManager
from core.constants import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    COLOR_SUCCESS, APP_NAME, AUTHOR_NAME
)
from utils.logger import get_logger
from utils.paths import RESOURCES_DIR
from utils.icon_utils import get_cropped_icon
from gui.theme import AppTheme
from gui.widgets.sidebar import Sidebar

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.logger = get_logger()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_default_config()
        
        # Tab references (now pages)
        self.pages = {}
        
        self.init_ui()
        
        self.logger.info("Main window initialized")
    
    def init_ui(self):
        """Initialize the user interface"""
        # Set window properties
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Set window icon explicitly for maximum visibility in taskbar/titlebar
        self.setWindowIcon(get_cropped_icon(RESOURCES_DIR / "app_favicon.png"))
        
        # Determine background color based on theme
        self.setStyleSheet(f"background-color: {AppTheme.BG_MAIN};")
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout (Horizontal: Sidebar | Content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Sidebar (Left)
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.switch_page)
        main_layout.addWidget(self.sidebar)
        
        # 2. Content Area (Right)
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Stacked Widget for Pages
        self.stacked_widget = QStackedWidget()
        self.init_all_pages()
        content_layout.addWidget(self.stacked_widget)
        
        # Bottom Button Panel
        self.create_button_panel(content_layout)
        
        main_layout.addWidget(content_container)
        
        # Set font
        font = QFont("Segoe UI", 9)
        self.setFont(font)
        
        # Select first page by default (Accounts)
        self.sidebar.buttons[0].click()
    
    def init_all_pages(self):
        """Initialize all application pages"""
        # Import page modules
        from gui.tabs.tab_accounts import TabAccounts
        from gui.tabs.tab_files import TabFiles
        from gui.tabs.tab_repositories import TabRepositories
        from gui.tabs.tab_secrets import TabSecrets
        from gui.tabs.tab_actions import TabActions
        from gui.tabs.tab_about import TabAbout
        from gui.tabs.tab_disclaimer import TabDisclaimer
        
        # Create pages
        self.page_accounts = TabAccounts(self)
        self.page_files = TabFiles(self)
        self.page_repositories = TabRepositories(self)
        self.page_secrets = TabSecrets(self)
        self.page_actions = TabActions(self)
        self.page_about = TabAbout(self)
        self.page_disclaimer = TabDisclaimer(self)
        
        # Add to stacked widget in specific order matching Sidebar indices
        # 0: Accounts
        self.stacked_widget.addWidget(self.page_accounts)
        # 1: Files
        self.stacked_widget.addWidget(self.page_files)
        # 2: Repositories (Note: Sidebar swapped order visually, but indices matter)
        # In Sidebar we mapped: Accounts(0), Repos(2), Files(1)... wait.
        # Let's check Sidebar indices:
        # Accounts=0, Repositories=2, Files=1, Secrets=3, Actions=4, About=5, Disclaimer=6
        
        # We need to add them in order 0, 1, 2, 3...
        # So we MUST add Files at index 1 and Repos at index 2? 
        # Wait, QStackedWidget indices are based on add order.
        # So I should add them: Accounts, Files, Repositories, Secrets... 
        
        # Let's align with Sidebar:
        # 0: Accounts
        # 1: Files
        # 2: Repositories
        # 3: Secrets
        # 4: Actions
        # 5: About
        # 6: Disclaimer
        
        self.stacked_widget.addWidget(self.page_repositories) # Index 2
        self.stacked_widget.addWidget(self.page_secrets)      # Index 3
        self.stacked_widget.addWidget(self.page_actions)      # Index 4
        self.stacked_widget.addWidget(self.page_about)        # Index 5
        self.stacked_widget.addWidget(self.page_disclaimer)   # Index 6
        
        # Store references
        self.pages = {
            "Accounts": self.page_accounts,
            "Files": self.page_files,
            "Repositories": self.page_repositories,
            "Secrets": self.page_secrets,
            "Actions": self.page_actions,
            "About": self.page_about,
            "Disclaimer": self.page_disclaimer
        }
    
    def switch_page(self, index):
        """Switch current page in stacked widget"""
        self.stacked_widget.setCurrentIndex(index)
    
    def create_button_panel(self, parent_layout):
        """Create bottom button panel"""
        # Outer container (transparent)
        button_panel = QWidget()
        button_panel.setFixedHeight(100) # Increased height for floating feel
        button_panel.setStyleSheet("background-color: transparent;")
        
        # Layout for centering: [Stretch] [Card] [Stretch]
        panel_layout = QHBoxLayout(button_panel)
        panel_layout.setContentsMargins(0, 10, 0, 10)
        panel_layout.addStretch()
        
        # Inner Card Frame
        self.bottom_card_frame = QFrame()
        self.bottom_card_frame.setFixedHeight(80)
        # Match Upper Card Style
        self.bottom_card_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppTheme.BG_CARD};
                border: 1px solid {AppTheme.BORDER};
                border-radius: 8px;
            }}
        """)
        
        # Layout inside the card
        card_layout = QHBoxLayout(self.bottom_card_frame)
        card_layout.setContentsMargins(30, 15, 30, 15)
        card_layout.setSpacing(15)
        
        # Left side buttons
        btn_load_config = self.create_button("📂 Load", "secondary", self.on_load_config)
        card_layout.addWidget(btn_load_config)
        
        btn_save_config = self.create_button("📥 Save", "secondary", self.on_save_config)
        card_layout.addWidget(btn_save_config)
        
        # Spacer
        card_layout.addStretch()
        
        # Right side buttons
        btn_create_all = self.create_button("🔥 CREATE ALL", "success", self.on_create_all)
        btn_create_all.setFixedSize(180, 45) # Make it bigger
        card_layout.addWidget(btn_create_all)
        
        panel_layout.addWidget(self.bottom_card_frame)
        panel_layout.addStretch()
        
        parent_layout.addWidget(button_panel)
    
    def create_button(self, text, style_type, callback):
        """Create a styled button"""
        button = QPushButton(text)
        button.setCursor(Qt.PointingHandCursor)
        button.setFixedSize(140, 40)
        
        # Apply style from styles.py logic (manually applying stylesheet here for simplicity with new theme)
        if style_type == "primary":
            from gui.styles import BUTTON_PRIMARY
            button.setStyleSheet(BUTTON_PRIMARY)
        elif style_type == "secondary":
            from gui.styles import BUTTON_SECONDARY
            button.setStyleSheet(BUTTON_SECONDARY)
        elif style_type == "success":
            from gui.styles import BUTTON_SUCCESS
            button.setStyleSheet(BUTTON_SUCCESS)
            
        button.clicked.connect(callback)
        return button
    
    def on_load_config(self):
        """Handle Load Config button click"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "Load Configuration",
                str(self.config_manager.config_dir),
                "JSON Files (*.json);;All Files (*.*)"
            )
            
            if filename:
                config = self.config_manager.load_config(filename)
                if config:
                    self.config = config
                    self.apply_config_to_ui()
                    QMessageBox.information(self, "Success", "Configuration loaded successfully!")
                    self.logger.info(f"Configuration loaded from: {filename}")
                else:
                    QMessageBox.warning(self, "Error", "Failed to load configuration file.")
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred:\n\n{str(e)}")
    
    def on_save_config(self):
        """Handle Save Config button click"""
        try:
            self.collect_config_from_ui()
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Configuration",
                str(self.config_manager.config_dir / "config.json"),
                "JSON Files (*.json);;All Files (*.*)"
            )
            
            if filename:
                success = self.config_manager.save_config(filename, self.config)
                if success:
                    QMessageBox.information(self, "Success", "Configuration saved successfully!")
                    self.logger.info(f"Configuration saved to: {filename}")
                else:
                    QMessageBox.warning(self, "Error", "Failed to save configuration file.")
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred:\n\n{str(e)}")
    
    def on_create_all(self):
        """Handle CREATE ALL button click"""
        try:
            self.collect_config_from_ui()
            
            # Basic validation
            if not self.config.get('github_username') or not self.config.get('github_token'):
                QMessageBox.warning(self, "Missing Info", "Please configure GitHub credentials in Accounts tab.")
                self.sidebar.buttons[0].click() # Switch to Accounts
                return
            
            repo_count = self.config.get('repo_count', 0)
            reply = QMessageBox.question(
                self, "Confirm Creation",
                f"Ready to create {repo_count} repositories?\n\nContinue?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.start_creation_process()
                
        except Exception as e:
            self.logger.error(f"Error starting creation: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred:\n\n{str(e)}")
    
    def start_creation_process(self):
        """Start the repository creation process"""
        try:
            from gui.dialogs.progress_dialog import ProgressDialog
            from api.repository_creator import RepositoryCreator
            
            self.logger.info("Starting repository creation workflow")
            progress_dialog = ProgressDialog(self.config, self)
            worker = RepositoryCreator(self.config)
            
            worker.progress_updated.connect(lambda overall, step, act: progress_dialog.update_progress(overall, step, act))
            worker.stats_updated.connect(lambda t, c, cur, f: progress_dialog.update_stats(t, c, cur, f))
            worker.finished.connect(lambda s, m, r: self.on_creation_finished(s, m, r, progress_dialog))
            progress_dialog.btn_cancel.clicked.connect(worker.cancel)
            
            worker.start()
            progress_dialog.exec_()
            
        except Exception as e:
            self.logger.error(f"Error starting creation process: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to start creation process:\n\n{str(e)}")
    
    def on_creation_finished(self, success, message, results, progress_dialog):
        """Handle creation process completion"""
        from gui.dialogs.completion_dialog import CompletionDialog
        try:
            progress_dialog.set_completed(success, message)
            progress_dialog.accept()
            completion = CompletionDialog(success, message, results, self)
            completion.exec_()
            self.logger.info(f"Creation process completed: {message}")
        except Exception as e:
            self.logger.error(f"Error handling completion: {e}")
    
    def collect_config_from_ui(self):
        """Collect configuration from all pages"""
        try:
            self.config.update(self.page_accounts.get_config())
            self.config.update(self.page_files.get_config())
            self.config.update(self.page_repositories.get_config())
            self.config.update(self.page_secrets.get_config())
            self.config.update(self.page_actions.get_config())
            self.logger.debug("Configuration collected from all pages")
        except Exception as e:
            self.logger.error(f"Error collecting config: {e}")
    
    def apply_config_to_ui(self):
        """Apply loaded configuration to UI"""
        try:
            self.page_accounts.set_config(self.config)
            self.page_files.set_config(self.config)
            self.page_repositories.set_config(self.config)
            self.page_secrets.set_config(self.config)
            self.page_actions.set_config(self.config)
            self.logger.debug("Configuration applied to all pages")
        except Exception as e:
            self.logger.error(f"Error applying config: {e}")
    
    def resizeEvent(self, event):
        """Handle resize to update bottom card width"""
        super().resizeEvent(event)
        
        # Logic matching ResponsiveContainer in gui/responsive_widgets.py
        # max_width=1100 (from TabAccounts), min_width=900, percentage=80
        if hasattr(self, 'bottom_card_frame'):
            # Calculate available width (Window width - Sidebar width of 260)
            available_width = self.width() - 260
            
            # Use percentage of available width
            optimal_width = int(available_width * 0.80)
            
            # Clamp between min and max (matching upper cards)
            optimal_width = max(900, min(optimal_width, 1100))
            
            self.bottom_card_frame.setFixedWidth(optimal_width)

    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(
            self, "Confirm Exit", "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.logger.info("Application closed")
            event.accept()
        else:
            event.ignore()
