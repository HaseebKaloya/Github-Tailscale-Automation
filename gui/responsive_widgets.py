"""
Responsive Widget Components for Github&Tailscale-Automation
Author: Haseeb Kaloya

Provides responsive, scrollable containers with optimal sizing
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame
from PyQt5.QtCore import Qt

class ResponsiveContainer(QWidget):
    """
    A responsive container that:
    - Adds scroll area automatically
    - Centers content
    - Dynamically adapts width based on window size
    - Adapts to window resizing
    """
    
    def __init__(self, parent=None, max_width=1600, width_percentage=80):
        super().__init__(parent)
        self.max_width = max_width
        self.min_width = 900
        self.width_percentage = width_percentage  # Percentage of window width to use
        self.init_ui()
    
    def init_ui(self):
        """Initialize the responsive container"""
        # Main layout for the responsive container
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create wrapper widget for centering
        wrapper_widget = QWidget()
        wrapper_layout = QHBoxLayout(wrapper_widget)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add left stretch
        wrapper_layout.addStretch(1)
        
        # Create content widget with dynamic width
        self.content_widget = QWidget()
        # Initial width - will be adjusted dynamically
        self.content_widget.setMaximumWidth(self.max_width)
        self.content_widget.setMinimumWidth(self.min_width)
        
        # Content layout
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)
        
        # Add content widget to wrapper
        wrapper_layout.addWidget(self.content_widget)
        
        # Add right stretch
        wrapper_layout.addStretch(1)
        
        # Set wrapper widget to scroll area
        scroll_area.setWidget(wrapper_widget)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)
    
    def add_widget(self, widget):
        """Add a widget to the content layout"""
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add a layout to the content layout"""
        self.content_layout.addLayout(layout)
    
    def add_stretch(self):
        """Add vertical stretch"""
        self.content_layout.addStretch()
    
    def get_layout(self):
        """Get the content layout for direct manipulation"""
        return self.content_layout
    
    def resizeEvent(self, event):
        """Handle window resize to dynamically adjust content width"""
        super().resizeEvent(event)
        
        # Calculate optimal width based on window size
        window_width = self.width()
        
        # Use percentage of window width
        optimal_width = int(window_width * (self.width_percentage / 100))
        
        # Clamp between min and max
        optimal_width = max(self.min_width, min(optimal_width, self.max_width))
        
        # Update content widget width
        self.content_widget.setMaximumWidth(optimal_width)
        self.content_widget.setMinimumWidth(min(self.min_width, optimal_width))


class OptimalFormLayout(QVBoxLayout):
    """
    Form layout with optimal sizing:
    - Labels have fixed width
    - Input fields have max width
    - Responsive to window size
    """
    
    LABEL_WIDTH = 140
    INPUT_MAX_WIDTH = 750
    BUTTON_WIDTH = 120
    
    @staticmethod
    def create_field_row(label_text, input_widget, button_widget=None, label_width=LABEL_WIDTH):
        """
        Create a horizontal form field row
        
        Args:
            label_text: Label text
            input_widget: Input widget (QLineEdit, etc.)
            button_widget: Optional button widget
            label_width: Width of label
            
        Returns:
            QHBoxLayout: The row layout
        """
        from PyQt5.QtWidgets import QHBoxLayout, QLabel
        
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)
        
        # Label
        from gui.theme import AppTheme
        label = QLabel(label_text)
        label.setFixedWidth(label_width)
        # Fix choppy highlights: Transparent bg, Bold text, Larger size
        label.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                font-family: 'Segoe UI';
                font-size: 11pt;
                font-weight: 600;
                color: {AppTheme.TEXT_MAIN};
                padding-right: 10px;
            }}
        """)
        row_layout.addWidget(label)
        
        # Input widget with max width
        input_widget.setMaximumWidth(OptimalFormLayout.INPUT_MAX_WIDTH)
        row_layout.addWidget(input_widget)
        
        # Optional button
        if button_widget:
            button_widget.setFixedWidth(OptimalFormLayout.BUTTON_WIDTH)
            row_layout.addWidget(button_widget)
        
        # Stretch to fill remaining space
        row_layout.addStretch()
        
        return row_layout


class CenteredButtonRow(QWidget):
    """
    A row of buttons that stays centered and doesn't stretch
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the button row"""
        from PyQt5.QtWidgets import QHBoxLayout
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(15)
        
        # Left stretch
        layout.addStretch()
        
        # Store button layout reference
        self.button_layout = layout
    
    def add_button(self, button, width=150):
        """Add a button to the row"""
        button.setFixedWidth(width)
        # Insert before the last item (which is stretch)
        self.button_layout.insertWidget(self.button_layout.count() - 1, button)
    
    def finish(self):
        """Call this after adding all buttons to add right stretch"""
        self.button_layout.addStretch()
