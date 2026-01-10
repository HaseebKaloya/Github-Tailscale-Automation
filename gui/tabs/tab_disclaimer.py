"""
Disclaimer Tab for Github&Tailscale-Automation
Author: Haseeb Kaloya

Legal disclaimer and usage terms
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.constants import AUTHOR_NAME, AUTHOR_EMAIL, AUTHOR_CONTACT
from gui.responsive_widgets import ResponsiveContainer

class TabDisclaimer(QWidget):
    """Disclaimer tab widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        # Create responsive container with dynamic width
        container = ResponsiveContainer(self, max_width=1500, width_percentage=78)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        layout = container.get_layout()
        layout.setSpacing(12)
        
        # Title with enhanced styling
        title = QLabel("IMPORTANT DISCLAIMER")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #C00000;
            background-color: transparent;
            padding: 18px;
            border: 2px solid #C00000;
            border-radius: 10px;
        """)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Please read carefully before using this software")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            color: #856404;
            padding: 14px;
            background-color: transparent;
            border: 2px solid #FFE69C;
            border-radius: 8px;
            font-weight: 600;
        """)
        layout.addWidget(subtitle)
        
        # Disclaimer text - Human-written, friendly but professional
        disclaimer_text = f"""
<div style="font-family: Segoe UI; font-size: 10pt; line-height: 1.8;">

<div style="background-color: transparent; padding: 22px; border-radius: 12px; margin-bottom: 20px; border: 3px solid #5C6BC0;">
    <h2 style="margin: 0; font-size: 16pt; color: #1A237E; font-weight: bold;">Welcome! Let's Talk About Using This Tool Wisely</h2>
    <p style="margin: 10px 0 0 0; font-size: 10pt; line-height: 1.6; color: #283593;">Hey! Before you dive into automating all the things, let's have a quick chat about responsible usage and what you need to know.</p>
</div>

<div style="background-color: transparent; padding: 20px; border-radius: 10px; border-left: 5px solid #2196F3; margin-bottom: 20px;">
    <h3 style="color: #1565C0; margin-top: 0;">The Straight Talk</h3>
    <p>Look, I've built this tool to save you tons of time and make your life easier. It's powerful, it's fast, and it works great when used correctly. But here's the thing – with great power comes great responsibility.</p>
    <p><strong>In simple terms:</strong> This software is provided "as is" – meaning I've done my best to make it awesome, but I can't guarantee it'll work perfectly in every single situation. Use it wisely, and we'll all be happy!</p>
</div>

<div style="background-color: transparent; padding: 20px; border-radius: 10px; border-left: 5px solid #FF9800; margin-bottom: 20px;">
    <h3 style="color: #E65100; margin-top: 0;">Your Part of the Deal</h3>
    
    <p><strong>Play by the Rules:</strong></p>
    <ul style="line-height: 1.8;">
        <li><strong>GitHub & Tailscale have rules</strong> – Make sure you follow their Terms of Service and API guidelines. They're pretty reasonable, just don't abuse the APIs!</li>
        <li><strong>Keep your secrets... secret!</strong> Your API tokens and credentials are powerful. Store them securely, don't share them, and treat them like your house keys.</li>
        <li><strong>Be cool, be legal</strong> – Only use this tool for legitimate purposes. No funny business, please!</li>
    </ul>
    
    <p><strong>API Limits (Important!):</strong></p>
    <ul style="line-height: 1.8;">
        <li><strong>GitHub has rate limits</strong> – If you go too crazy with API calls, GitHub might temporarily block you. The software has built-in delays to help prevent this, but still... don't create 500 repos in one go, okay?</li>
        <li><strong>Tailscale limits key generation</strong> – They're generous, but don't abuse it. Use the auto-generation feature responsibly.</li>
        <li><strong>Pro tip:</strong> Start small! Test with a few repositories first, then scale up once you're comfortable.</li>
    </ul>
</div>

<div style="background-color: transparent; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 20px;">
    <h3 style="color: #1B5E20; margin-top: 0;">Privacy & Security (You'll Love This)</h3>
    
    <p><strong>Good news!</strong> Your data stays on YOUR machine. Here's what you need to know:</p>
    <ul style="line-height: 1.8;">
        <li><strong>Everything is local</strong> – Your tokens, credentials, and config files are stored only on your computer</li>
        <li><strong>No sneaky tracking</strong> – I don't collect any data about you or your usage</li>
        <li><strong>Only official APIs</strong> – The software only talks to GitHub and Tailscale APIs (that's kind of the whole point!)</li>
        <li><strong>But remember:</strong> You're responsible for keeping your credentials safe. Use strong passwords, enable 2FA, the usual good stuff!</li>
    </ul>
</div>

<div style="background-color: transparent; padding: 20px; border-radius: 10px; border-left: 5px solid #E91E63; margin-bottom: 20px;">
    <h3 style="color: #880E4F; margin-top: 0;">The Legal Bit (I Promise It's Short)</h3>
    
    <p><strong>Here's the deal:</strong></p>
    <ul style="line-height: 1.8;">
        <li>I ({AUTHOR_NAME}) built this tool with care, but I can't be held responsible for how you use it or what happens</li>
        <li>Always double-check what you're automating before hitting that Create button!</li>
        <li>If something goes wrong, you're responsible for fixing it (but hey, that's why there's a Cancel button!)</li>
        <li>Use at your own risk – but honestly, if you use it sensibly, you'll be fine!</li>
    </ul>
</div>

<div style="background-color: transparent; padding: 20px; border-radius: 10px; border-left: 5px solid #9C27B0; margin-bottom: 20px;">
    <h3 style="color: #4A148C; margin-top: 0;">Pro Tips for Success</h3>
    
    <ul style="line-height: 1.8;">
        <li><strong>Test first!</strong> Create 2-3 repositories as a test before bulk creation</li>
        <li><strong>Monitor the progress dialog</strong> – It shows you exactly what's happening</li>
        <li><strong>Use the Cancel button</strong> if something doesn't look right</li>
        <li><strong>Enable auto-backup</strong> for Tailscale keys – you'll thank me later!</li>
        <li><strong>Check the logs</strong> if something unexpected happens</li>
    </ul>
</div>

<div style="background-color: transparent; padding: 20px; border-radius: 10px; border-left: 5px solid #FBC02D; margin-bottom: 20px;">
    <h3 style="color: #F57F17; margin-top: 0;">Need Help or Custom Work?</h3>
    
    <p><strong>Got questions? Need something custom?</strong></p>
    <p>While this software is provided "as-is" (meaning no guaranteed support), I'm always happy to help where I can! If you need custom features, have a unique automation challenge, or want professional development services, just reach out!</p>
    
    <p style="text-align: center; margin: 15px 0;">
        <strong>{AUTHOR_EMAIL}</strong><br>
        <strong>{AUTHOR_CONTACT}</strong>
    </p>
    
    <p style="background-color: transparent; padding: 15px; border: 2px solid #FBC02D; border-radius: 8px; text-align: center;">
        <strong>Professional automation development services available!</strong><br>
        Quick turnaround • Clean code • Ongoing support
    </p>
</div>

<div style="background-color: transparent; padding: 25px; border-radius: 12px; margin-bottom: 20px; text-align: center; border: 3px solid #5C6BC0;">
    <h3 style="margin: 0 0 12px 0; font-size: 14pt; color: #1A237E; font-weight: bold;">By Using This Software</h3>
    <p style="margin: 0; font-size: 10pt; line-height: 1.7; color: #283593; font-weight: 500;">You confirm that you've read this page, understand the guidelines, and agree to use the software responsibly and in compliance with all applicable terms of service. Basically: be smart, be cool, and automate awesome things!</p>
</div>

<p style="text-align: center; color: #666666; font-size: 10pt; margin-top: 30px; padding: 20px; background-color: transparent; border: 1px solid #E0E0E0; border-radius: 10px;">
    <strong>© 2026 {AUTHOR_NAME}. All rights reserved.</strong><br>
    <span style="font-size: 9pt; color: #888888;">Made with heart and lots of coffee for the automation community</span>
</p>

</div>
        """
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(disclaimer_text)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #F5F5F5;
                color: #000000;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 15px;
                font-size: 10pt;
                line-height: 1.6;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #0078D4;
            }
        """)
        layout.addWidget(text_edit)
    
    def get_config(self):
        """Get configuration from this tab"""
        return {}
    
    def set_config(self, config):
        """Set configuration to this tab"""
        pass
