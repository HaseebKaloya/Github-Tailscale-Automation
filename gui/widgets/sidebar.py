
"""
Professional Sidebar Navigation
Author: Haseeb Kaloya
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QRect
from PyQt5.QtGui import QIcon, QFont, QPixmap, QImage, QBitmap, QRegion

from gui.theme import AppTheme
from utils.paths import RESOURCES_DIR
from utils.icon_utils import get_cropped_icon
import os

class NavigationButton(QPushButton):
    """Custom flat navigation button with hover effects and active state"""
    
    def __init__(self, text, icon_path, parent=None):
        super().__init__(text, parent)
        self.icon_path = icon_path
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 10))
        self.is_active = False
        
        # Ensure text has some padding from the icon
        self.setStyleSheet("text-align: left; padding-left: 20px;")
        
        # Initial style
        self.update_style()
        
    def set_active(self, active):
        self.is_active = active
        self.update_style()
        
    def update_style(self):
        if self.is_active:
            # Softer, professional highlight (Light Blue instead of harsh Grey)
            bg_color = "#EFF6FC"  # Very subtle blue
            text_color = AppTheme.PRIMARY
            # Colored bar on left
            border_left = f"4px solid {AppTheme.PRIMARY}"
            font_weight = "600"
        else:
            bg_color = "transparent"
            text_color = AppTheme.TEXT_MAIN
            border_left = "4px solid transparent"
            font_weight = "400"
            
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-left: {border_left};
                border-radius: 6px;
                text-align: left;
                padding-left: 20px;
                font-weight: {font_weight};
                margin: 2px 10px; /* More horizontal breathing room */
                outline: none;
            }}
            QPushButton:hover {{
                background-color: {AppTheme.PRIMARY_LIGHT};
                color: {AppTheme.PRIMARY};
            }}
        """)
        
class Sidebar(QWidget):
    """Main vertical sidebar"""
    
    page_changed = pyqtSignal(int)  # Emits index of page to switch to
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300) # Increased width to fit long single-line title
        self.buttons = []
        
        self.init_ui()
        
    def init_ui(self):
        # Apply theme
        self.setStyleSheet(AppTheme.get_sidebar_style())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 1. Header / Logo Area
        self.create_logo_area(layout)
        
        # 2. Tight Navigation Start
        layout.addSpacing(0)
        
        # 3. Navigation Buttons
        # Define items: (Name, Icon Filename, Page Index)
        nav_items = [
            ("Accounts", "user.svg", 0),
            ("Repositories", "box.svg", 2),
            ("Files", "folder.svg", 1),
            ("Secrets", "key.svg", 3),
            ("Actions", "settings.svg", 4)
        ]
        
        for name, icon, index in nav_items:
            btn = self.create_nav_button(name, icon, index)
            layout.addWidget(btn)
            
        layout.addStretch()
        
        # 4. Bottom Buttons
        bottom_items = [
            ("About", "info.svg", 5),
            ("Disclaimer", "warning.svg", 6)
        ]
        
        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {AppTheme.DIVIDER}; border: none; max-height: 1px;")
        layout.addWidget(line)
        
        for name, icon, index in bottom_items:
            btn = self.create_nav_button(name, icon, index)
            layout.addWidget(btn)
            
        layout.addSpacing(10)
        
    def create_logo_area(self, layout):
        container = QWidget()
        container.setFixedHeight(200) # Slightly more compact for smaller logo stack
        container.setStyleSheet("background-color: transparent;")
        
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 10, 0, 5) # Professional top/bottom breathing room
        vbox.setSpacing(2) # Ultra-tight group spacing
        vbox.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        vbox.setSizeConstraint(QVBoxLayout.SetMinimumSize) # Shrinkwrap to content
        
        # --- 1. Brand Icon (High-Quality Favicon with Smart Crop) ---
        icon_label = QLabel()
        icon_path = RESOURCES_DIR / "app_favicon.png"
        icon = get_cropped_icon(icon_path)
        if not icon.isNull():
            pixmap = icon.pixmap(icon.actualSize(QSize(512, 512)))
            
            # Now scale the TIHGHTLY CROPPED logo to an elegant size
            # Balanced size for visibility (140x140)
            scaled_pixmap = pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
        else:
            icon_label.setText("GT")
            icon_label.setStyleSheet(f"color: {AppTheme.PRIMARY}; font-size: 24pt; font-weight: bold;")
            
        icon_label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(icon_label, 0, Qt.AlignCenter)
        
        # --- 2. Main Title (High Visibility Single Line) ---
        title_label = QLabel("Github & Tailscale Automation")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {AppTheme.TEXT_MAIN};
                font-family: 'Segoe UI'; 
                font-size: 11pt; /* Adjusted for single-line fit */
                font-weight: 800; /* Extra Bold as requested */
                letter-spacing: -0.2px; /* Tighten for premium look */
            }}
        """)
        vbox.addWidget(title_label)
        
        # --- 3. Subtitle / Product Badge ---
        badge = QLabel("PROFESSIONAL EDITION")
        badge.setAlignment(Qt.AlignCenter)
        badge.setFixedWidth(160)
        badge.setStyleSheet(f"""
            QLabel {{
                background-color: {AppTheme.PRIMARY_LIGHT};
                color: {AppTheme.PRIMARY};
                border-radius: 3px;
                font-family: 'Segoe UI';
                font-size: 7pt;
                font-weight: 800;
                letter-spacing: 1.2px;
                padding: 3px 0px;
                margin-top: 2px;
            }}
        """)
        vbox.addWidget(badge, 0, Qt.AlignCenter)

        # --- 4. Author Credit ---
        edition_label = QLabel("Haseeb Kaloya")
        edition_label.setAlignment(Qt.AlignCenter)
        edition_label.setStyleSheet(f"""
            QLabel {{
                color: {AppTheme.TEXT_SECONDARY};
                font-family: 'Segoe UI';
                font-size: 8pt;
                font-style: italic;
                margin-top: 1px;
            }}
        """)
        vbox.addWidget(edition_label)
        
        layout.addWidget(container)
        
    def create_nav_button(self, text, icon_name, index):
        # Load SVG icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "resources", "icons", icon_name)
        
        btn = NavigationButton(text, icon_path)
        
        # Set icon
        if os.path.exists(icon_path):
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20)) # Pro standard size
            
        btn.clicked.connect(lambda: self.on_nav_clicked(btn, index))
        self.buttons.append(btn)
        return btn
        
    def on_nav_clicked(self, clicked_btn, index):
        # Update active state
        for btn in self.buttons:
            btn.set_active(btn == clicked_btn)
            
        # Emit signal
        self.page_changed.emit(index)
        
    def set_active_index(self, index):
        # Programmatically set active button (e.g. on startup)
        # Note: mapping logic requires index to match button order if we used indices
        # But here we have sparse indices. We don't strictly need this unless distinct logic requires it.
        # For simple mapping:
        pass 
