
"""
Theme definitions for Github&Tailscale-Automation
Provides a centralized color palette for Light/Dark modes (currently Light focus)
"""

class AppTheme:
    # Primary Colors (Professional Blue)
    PRIMARY = "#0078D4"
    PRIMARY_HOVER = "#006CBD"
    PRIMARY_PRESSED = "#005A9E"
    PRIMARY_LIGHT = "#EFF6FC"  # Very subtle blue for accents
    PRIMARY_TEXT = "#FFFFFF"

    # Backgrounds
    BG_MAIN = "#F3F3F3"       # Main window background (light grey)
    BG_SIDEBAR = "#FFFFFF"    # Sidebar background (white)
    BG_CARD = "#FFFFFF"       # Card/Panel background (white)
    
    # Text
    TEXT_MAIN = "#323130"
    TEXT_SECONDARY = "#605E5C"
    TEXT_DISABLED = "#A19F9D"
    
    # Status Colors
    SUCCESS = "#107C10"
    WARNING = "#D83B01"
    ERROR = "#D13438"
    INFO = "#0078D4"

    # UI Elements
    BORDER = "#E1DFDD"
    DIVIDER = "#EDEBE9"
    HOVER_BG = "#F3F2F1"      # Subtle hover background for lists/items
    
    # Inputs
    INPUT_BG = "#FFFFFF"
    INPUT_BORDER = "#8A8886"
    INPUT_FOCUS = "#0078D4"

    @classmethod
    def get_sidebar_style(cls):
        return f"""
            QWidget {{
                background-color: {cls.BG_SIDEBAR};
                border-right: 1px solid {cls.BORDER};
            }}
        """

    @classmethod
    def get_card_style(cls):
        return f"""
            QFrame {{
                background-color: {cls.BG_CARD};
                border: 1px solid {cls.BORDER};
                border-radius: 8px;
            }}
            QLabel {{
                color: {cls.TEXT_MAIN};
            }}
        """
