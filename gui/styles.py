"""
Beautiful styling components for Github&Tailscale-Automation
Author: Haseeb Kaloya

Provides consistent, professional styling across all GUI components
"""

from gui.theme import AppTheme

# Group Box Styles (Modern Card Look)
GROUPBOX_STYLE = f"""
    QGroupBox {{
        border: 1px solid {AppTheme.BORDER};
        border-radius: 8px;
        margin-top: 24px;
        background-color: {AppTheme.BG_CARD};
        font-weight: 600;
        color: {AppTheme.PRIMARY};
        font-family: "Segoe UI";
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 20px;
        padding: 0 5px;
        color: {AppTheme.PRIMARY};
        background-color: transparent;
    }}
"""

# 2. Input Field Style (Modern & Flat)
INPUT_STYLE = f"""
QLineEdit {{
    border: 1px solid {AppTheme.INPUT_BORDER};
    border-radius: 6px;
    padding: 10px 12px; /* Comfortable padding */
    background-color: {AppTheme.INPUT_BG};
    color: {AppTheme.TEXT_MAIN};
    font-family: 'Segoe UI';
    font-size: 10pt;
    selection-background-color: {AppTheme.PRIMARY};
    selection-color: white;
}}

QLineEdit:focus {{
    border: 2px solid {AppTheme.PRIMARY}; /* Highlight on focus */
    padding: 9px 11px; /* Adjust for border width change */
    background-color: white;
}}

QLineEdit:disabled {{
    background-color: {AppTheme.HOVER_BG};
    color: {AppTheme.TEXT_SECONDARY};
    border: 1px solid {AppTheme.BORDER};
}}
"""

# 3. Primary Button Style (Solid Vivid Blue)
BUTTON_PRIMARY = f"""
QPushButton {{
    background-color: {AppTheme.PRIMARY};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-family: 'Segoe UI';
    font-weight: 600;
    font-size: 10pt;
}}

QPushButton:hover {{
    background-color: {AppTheme.PRIMARY_HOVER};
}}

QPushButton:pressed {{
    background-color: {AppTheme.PRIMARY_PRESSED};
    padding-top: 11px; /* Subtle press effect */
}}

QPushButton:disabled {{
    background-color: {AppTheme.BORDER};
    color: {AppTheme.TEXT_SECONDARY};
}}
"""

# 4. Secondary Button Style (Ghost/Outline)
BUTTON_SECONDARY = f"""
QPushButton {{
    background-color: white;
    color: {AppTheme.TEXT_MAIN};
    border: 1px solid {AppTheme.BORDER};
    border-radius: 6px;
    padding: 10px 20px;
    font-family: 'Segoe UI';
    font-weight: 600;
    font-size: 10pt;
}}

QPushButton:hover {{
    background-color: {AppTheme.HOVER_BG};
    border: 1px solid {AppTheme.TEXT_SECONDARY};
}}

QPushButton:pressed {{
    background-color: {AppTheme.BORDER};
}}
"""

# 5. Success Button Style (Green)
BUTTON_SUCCESS = f"""
QPushButton {{
    background-color: {AppTheme.SUCCESS};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-family: 'Segoe UI';
    font-weight: bold;
    font-size: 11pt;
}}

QPushButton:hover {{
    background-color: #0E700E; /* Darker Green */
}}

QPushButton:pressed {{
    background-color: #0A580A;
}}
"""

# 6. Checkbox Style
CHECKBOX_STYLE = f"""
QCheckBox {{
    spacing: 8px;
    font-family: 'Segoe UI';
    font-size: 10pt;
    color: {AppTheme.TEXT_MAIN};
    background-color: transparent;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 1px solid {AppTheme.INPUT_BORDER};
    border-radius: 4px;
    background-color: white;
}}

QCheckBox::indicator:checked {{
    background-color: {AppTheme.PRIMARY};
    border: 1px solid {AppTheme.PRIMARY};
    image: url(resources/icons/check_white.png); 
}}

QCheckBox::indicator:hover {{
    border: 1px solid {AppTheme.PRIMARY};
}}
"""

# 7. Radio Button Style
RADIO_STYLE = f"""
QRadioButton {{
    spacing: 8px;
    font-family: 'Segoe UI';
    font-size: 10pt;
    color: {AppTheme.TEXT_MAIN};
    background-color: transparent;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 10px;
    border: 1px solid {AppTheme.INPUT_BORDER};
    background-color: white;
}}

QRadioButton::indicator:checked {{
    border: 5px solid {AppTheme.PRIMARY}; /* Creates the dot */
    background-color: white;
}}

QRadioButton::indicator:hover {{
    border-color: {AppTheme.PRIMARY};
}}
"""

# 8. Slider Style
SLIDER_STYLE = f"""
QSlider::groove:horizontal {{
    border: 1px solid {AppTheme.BORDER};
    height: 8px; /* Slimmer groove */
    background: {AppTheme.INPUT_BG};
    margin: 2px 0;
    border-radius: 4px;
}}

QSlider::handle:horizontal {{
    background: {AppTheme.PRIMARY};
    border: 1px solid {AppTheme.PRIMARY};
    width: 18px;
    height: 18px;
    margin: -7px 0; /* center on groove */
    border-radius: 9px;
}}

QSlider::handle:horizontal:hover {{
    background: {AppTheme.PRIMARY_HOVER};
    border-color: {AppTheme.PRIMARY_HOVER};
}}

QSlider::sub-page:horizontal {{
    background: {AppTheme.PRIMARY};
    border-radius: 4px;
}}

QSlider::add-page:horizontal {{
    background: {AppTheme.INPUT_BG};
    border-radius: 4px;
}}

QSlider {{
    background: transparent;
    min-height: 24px;
}}
"""

LABEL_TITLE = f"""
    QLabel {{
        font-family: 'Segoe UI';
        font-size: 14pt;
        font-weight: bold;
        color: {AppTheme.PRIMARY};
        background-color: transparent;
        padding: 5px;
    }}
"""

LABEL_SUBTITLE = f"""
    QLabel {{
        font-size: 10pt;
        color: {AppTheme.TEXT_SECONDARY};
        background-color: transparent;
    }}
"""

LABEL_SUCCESS = f"""
    QLabel {{
        color: {AppTheme.SUCCESS};
        font-weight: 600;
        padding: 5px;
        background-color: transparent;
    }}
"""

LABEL_ERROR = f"""
    QLabel {{
        color: {AppTheme.ERROR};
        font-weight: 600;
        padding: 5px;
        background-color: transparent;
    }}
"""

LABEL_WARNING = f"""
    QLabel {{
        color: {AppTheme.WARNING};
        font-weight: 600;
        padding: 5px;
        background-color: transparent;
    }}
"""

# Helper function to apply styles
def apply_style(widget, style_name):
    """Apply a predefined style to a widget"""
    styles = {
        'groupbox': GROUPBOX_STYLE,
        'input': INPUT_STYLE,
        'button_primary': BUTTON_PRIMARY,
        'button_secondary': BUTTON_SECONDARY,
        'button_success': BUTTON_SUCCESS,
        'checkbox': CHECKBOX_STYLE,
        'radio': RADIO_STYLE,
        'slider': SLIDER_STYLE,
        'label_title': LABEL_TITLE,
        'label_subtitle': LABEL_SUBTITLE,
        'label_success': LABEL_SUCCESS,
        'label_error': LABEL_ERROR,
        'label_warning': LABEL_WARNING,
    }
    
    if style_name in styles:
        widget.setStyleSheet(styles[style_name])
