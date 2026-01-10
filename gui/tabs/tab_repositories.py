"""
Repositories Tab for Github&Tailscale-Automation
Author: Haseeb Kaloya

Repository configuration: count, naming, and options
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QCheckBox, QSlider, QFileDialog, QMessageBox, QButtonGroup, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pathlib import Path

from utils.helpers import read_lines_from_file
from utils.logger import get_logger
from core.constants import (
    MIN_REPO_COUNT, MAX_REPO_COUNT, DEFAULT_REPO_COUNT,
    STRATEGY_AUTO_GENERATE, STRATEGY_CUSTOM, STRATEGY_SEQUENTIAL, STRATEGY_IMPORT_FILE,
    AUTO_GEN_PREFIXES, FILTER_TEXT
)
from gui.responsive_widgets import ResponsiveContainer, OptimalFormLayout
from gui.styles import GROUPBOX_STYLE, INPUT_STYLE, BUTTON_PRIMARY, CHECKBOX_STYLE, RADIO_STYLE, SLIDER_STYLE

class TabRepositories(QWidget):
    """Repositories tab widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.logger = get_logger()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        # Create responsive container
        container = ResponsiveContainer(self, max_width=1200)
        
        # Set container as main widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        
        # Get content layout from container
        content_layout = container.get_layout()
        
        # Repository Count Section
        self.create_count_section(content_layout)
        
        # Naming Strategy Section
        self.create_naming_section(content_layout)
        
        # Repository Options Section
        self.create_options_section(content_layout)
        
        # Spacer
        content_layout.addStretch()
    
    def create_count_section(self, parent_layout):
        """Create repository count section"""
        group_box = QGroupBox("Repository Count")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(18)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Label
        lbl = QLabel("Number of repositories:")
        lbl.setStyleSheet("font-size: 10pt; color: #333333; font-weight: 500; background-color: transparent;")
        layout.addWidget(lbl)
        
        # Slider and value
        slider_layout = QHBoxLayout()
        
        self.slider_repo_count = QSlider(Qt.Horizontal)
        self.slider_repo_count.setMinimum(MIN_REPO_COUNT)
        self.slider_repo_count.setMaximum(MAX_REPO_COUNT)
        self.slider_repo_count.setValue(DEFAULT_REPO_COUNT)
        self.slider_repo_count.setTickPosition(QSlider.TicksBelow)
        self.slider_repo_count.setTickInterval(10)
        self.slider_repo_count.setMaximumWidth(600)
        self.slider_repo_count.setStyleSheet(SLIDER_STYLE)
        self.slider_repo_count.valueChanged.connect(self.on_repo_count_changed)
        
        self.lbl_repo_value = QLabel(str(DEFAULT_REPO_COUNT))
        self.lbl_repo_value.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.lbl_repo_value.setFixedWidth(60)
        self.lbl_repo_value.setAlignment(Qt.AlignCenter)
        self.lbl_repo_value.setStyleSheet("""
            QLabel {
                color: #0078D4;
                background-color: transparent;
                border: 2px solid #0078D4;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        
        slider_layout.addWidget(self.slider_repo_count)
        slider_layout.addWidget(self.lbl_repo_value)
        slider_layout.addStretch()
        layout.addLayout(slider_layout)
        
        # Preview label
        self.lbl_repo_preview = QLabel(f"Will create: {DEFAULT_REPO_COUNT} repositories")
        self.lbl_repo_preview.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.lbl_repo_preview.setAlignment(Qt.AlignCenter)
        self.lbl_repo_preview.setStyleSheet("""
            QLabel {
                color: #00B050;
                padding: 10px;
                background-color: transparent;
                border-left: 4px solid #00B050;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.lbl_repo_preview)
        
        parent_layout.addWidget(group_box)
    
    def create_naming_section(self, parent_layout):
        """Create naming strategy section"""
        group_box = QGroupBox("Repository Naming Strategy")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(18)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Button group for radio buttons
        self.naming_group = QButtonGroup()
        
        # Auto-generate - Enhanced with category selection
        auto_layout = QVBoxLayout()
        
        self.radio_auto = QRadioButton("Smart Auto-Generate (Professional Names)")
        self.radio_auto.setChecked(True)
        self.radio_auto.setStyleSheet(RADIO_STYLE + " font-size: 10pt; padding: 5px;")
        self.radio_auto.toggled.connect(self.on_naming_strategy_changed)
        self.naming_group.addButton(self.radio_auto)
        auto_layout.addWidget(self.radio_auto)
        
        # Category selection for auto-generate
        category_sub_layout = QHBoxLayout()
        category_sub_layout.setContentsMargins(30, 5, 0, 5)
        
        category_label = QLabel("Style:")
        category_label.setStyleSheet("font-size: 9pt; color: #666; min-width: 50px; background-color: transparent;")
        category_sub_layout.addWidget(category_label)
        
        from PyQt5.QtWidgets import QComboBox
        self.combo_naming_category = QComboBox()
        self.combo_naming_category.addItems([
            "Mixed (All Categories)",
            "Tech & Development", 
            "Business & Professional",
            "Modern & Creative",
            "Abstract & Elegant"
        ])
        self.combo_naming_category.setStyleSheet("""
            QComboBox {
                border: 1px solid #D0D0D0;
                border-radius: 4px;
                padding: 5px 8px;
                font-size: 9pt;
                background: white;
                min-width: 200px;
            }
            QComboBox:hover {
                border: 1px solid #0078D4;
            }
        """)
        self.combo_naming_category.setEnabled(False)
        category_sub_layout.addWidget(self.combo_naming_category)
        category_sub_layout.addStretch()
        
        auto_layout.addLayout(category_sub_layout)
        layout.addLayout(auto_layout)
        
        # Custom prefix
        custom_layout = QHBoxLayout()
        self.radio_custom = QRadioButton("Custom prefix:")
        self.radio_custom.setStyleSheet(RADIO_STYLE + " font-size: 10pt; padding: 5px;")
        self.radio_custom.toggled.connect(self.on_naming_strategy_changed)
        self.naming_group.addButton(self.radio_custom)
        custom_layout.addWidget(self.radio_custom)
        
        self.txt_custom_prefix = QLineEdit()
        self.txt_custom_prefix.setPlaceholderText("e.g., myrepo")
        self.txt_custom_prefix.setEnabled(False)
        self.txt_custom_prefix.setMaxLength(50)
        self.txt_custom_prefix.setStyleSheet(INPUT_STYLE)
        self.txt_custom_prefix.setMinimumHeight(35)
        self.txt_custom_prefix.setMaximumWidth(400)
        custom_layout.addWidget(self.txt_custom_prefix)
        custom_layout.addStretch()
        layout.addLayout(custom_layout)
        
        # Sequential prefix
        seq_layout = QHBoxLayout()
        self.radio_sequential = QRadioButton("Sequential prefix:")
        self.radio_sequential.setStyleSheet(RADIO_STYLE + " font-size: 10pt; padding: 5px;")
        self.radio_sequential.toggled.connect(self.on_naming_strategy_changed)
        self.naming_group.addButton(self.radio_sequential)
        seq_layout.addWidget(self.radio_sequential)
        
        self.txt_sequential_prefix = QLineEdit()
        self.txt_sequential_prefix.setPlaceholderText("e.g., project")
        self.txt_sequential_prefix.setEnabled(False)
        self.txt_sequential_prefix.setMaxLength(50)
        self.txt_sequential_prefix.setStyleSheet(INPUT_STYLE)
        self.txt_sequential_prefix.setMinimumHeight(35)
        self.txt_sequential_prefix.setMaximumWidth(400)
        seq_layout.addWidget(self.txt_sequential_prefix)
        seq_layout.addStretch()
        layout.addLayout(seq_layout)
        
        # Import from file
        file_layout = QHBoxLayout()
        self.radio_import = QRadioButton("Import from file:")
        self.radio_import.setStyleSheet(RADIO_STYLE + " font-size: 10pt; padding: 5px;")
        self.radio_import.toggled.connect(self.on_naming_strategy_changed)
        self.naming_group.addButton(self.radio_import)
        file_layout.addWidget(self.radio_import)
        
        self.txt_names_file = QLineEdit()
        self.txt_names_file.setPlaceholderText("Select file with repository names...")
        self.txt_names_file.setEnabled(False)
        self.txt_names_file.setReadOnly(True)
        self.txt_names_file.setStyleSheet(INPUT_STYLE)
        self.txt_names_file.setMinimumHeight(35)
        self.txt_names_file.setMaximumWidth(400)
        file_layout.addWidget(self.txt_names_file)
        
        self.btn_browse_names = QPushButton("Browse...")
        self.btn_browse_names.setFixedSize(120, 35)
        self.btn_browse_names.setEnabled(False)
        self.btn_browse_names.setCursor(Qt.PointingHandCursor)
        self.btn_browse_names.setStyleSheet(BUTTON_PRIMARY)
        self.btn_browse_names.clicked.connect(self.browse_names_file)
        file_layout.addWidget(self.btn_browse_names)
        file_layout.addStretch()
        layout.addLayout(file_layout)
        
        # Preview button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_preview = QPushButton("Preview Names")
        btn_preview.setFixedSize(180, 45)
        btn_preview.setCursor(Qt.PointingHandCursor)
        btn_preview.setStyleSheet(BUTTON_PRIMARY)
        btn_preview.clicked.connect(self.preview_names)
        btn_layout.addWidget(btn_preview)
        layout.addLayout(btn_layout)
        
        parent_layout.addWidget(group_box)
    
    def create_options_section(self, parent_layout):
        """Create repository options section"""
        group_box = QGroupBox("Repository Options")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(18)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Visibility
        visibility_layout = QHBoxLayout()
        lbl_visibility = QLabel("Visibility:")
        lbl_visibility.setStyleSheet("font-size: 10pt; font-weight: 500; min-width: 100px; background-color: transparent;")
        visibility_layout.addWidget(lbl_visibility)
        
        self.visibility_group = QButtonGroup()
        
        self.radio_private = QRadioButton("Private")
        self.radio_private.setChecked(True)
        self.radio_private.setStyleSheet(RADIO_STYLE + " font-size: 10pt; padding: 5px;")
        self.visibility_group.addButton(self.radio_private)
        visibility_layout.addWidget(self.radio_private)
        
        self.radio_public = QRadioButton("Public")
        self.radio_public.setStyleSheet(RADIO_STYLE + " font-size: 10pt; padding: 5px;")
        self.visibility_group.addButton(self.radio_public)
        visibility_layout.addWidget(self.radio_public)
        
        visibility_layout.addStretch()
        layout.addLayout(visibility_layout)
        
        # Initialize with README
        self.chk_init_readme = QCheckBox("Initialize with README")
        self.chk_init_readme.setChecked(True)
        self.chk_init_readme.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 5px;")
        layout.addWidget(self.chk_init_readme)
        
        # Description
        self.txt_description = QLineEdit()
        self.txt_description.setText("Automated repository created with Github&Tailscale-Automation")
        self.txt_description.setMaxLength(200)
        self.txt_description.setStyleSheet(INPUT_STYLE)
        self.txt_description.setMinimumHeight(40)
        
        desc_row = OptimalFormLayout.create_field_row(
            "Description:",
            self.txt_description,
            label_width=120
        )
        layout.addLayout(desc_row)
        
        parent_layout.addWidget(group_box)
    
    def on_repo_count_changed(self, value):
        """Handle repository count slider change"""
        self.lbl_repo_value.setText(str(value))
        self.lbl_repo_preview.setText(f"Will create: {value} repositories")
    
    def on_naming_strategy_changed(self):
        """Handle naming strategy radio button change"""
        # Enable/disable controls based on selection
        self.combo_naming_category.setEnabled(self.radio_auto.isChecked())
        self.txt_custom_prefix.setEnabled(self.radio_custom.isChecked())
        self.txt_sequential_prefix.setEnabled(self.radio_sequential.isChecked())
        self.txt_names_file.setEnabled(self.radio_import.isChecked())
        self.btn_browse_names.setEnabled(self.radio_import.isChecked())
    
    def browse_names_file(self):
        """Browse for names file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Names File",
            "",
            FILTER_TEXT
        )
        
        if filename:
            try:
                # Count names in file
                names = read_lines_from_file(filename)
                if names:
                    self.txt_names_file.setText(filename)
                    QMessageBox.information(
                        self,
                        "File Loaded",
                        f"Found {len(names)} repository names in file."
                    )
                    self.logger.info(f"Names file loaded: {filename} ({len(names)} names)")
                else:
                    QMessageBox.warning(
                        self,
                        "Empty File",
                        "The selected file is empty or contains no valid names."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to read file:\n{str(e)}"
                )
                self.logger.error(f"Error reading names file: {e}")
    
    def preview_names(self):
        """Preview repository names based on current strategy"""
        try:
            count = self.slider_repo_count.value()
            names = self.generate_names(count)
            
            if not names:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "Could not generate names. Please check your settings."
                )
                return
            
            # Show preview (first 20)
            preview_count = min(20, len(names))
            preview_text = f"Repository Names Preview (first {preview_count} of {len(names)}):\n\n"
            preview_text += "\n".join(names[:preview_count])
            
            if len(names) > 20:
                preview_text += f"\n\n... and {len(names) - 20} more"
            
            QMessageBox.information(
                self,
                "Name Preview",
                preview_text
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to generate preview:\n{str(e)}"
            )
            self.logger.error(f"Error previewing names: {e}")
    
    def generate_names(self, count):
        """Generate repository names based on strategy"""
        try:
            if self.radio_auto.isChecked():
                # Professional auto-generate with category support
                from core.constants import NAMING_CATEGORIES
                import random
                
                category_index = self.combo_naming_category.currentIndex()
                names = []
                
                # Select appropriate word list
                if category_index == 0:  # Mixed (All Categories)
                    available_words = AUTO_GEN_PREFIXES.copy()
                elif category_index == 1:  # Tech & Development
                    available_words = NAMING_CATEGORIES["tech"].copy()
                elif category_index == 2:  # Business & Professional
                    available_words = NAMING_CATEGORIES["business"].copy()
                elif category_index == 3:  # Modern & Creative
                    available_words = NAMING_CATEGORIES["creative"].copy()
                elif category_index == 4:  # Abstract & Elegant
                    available_words = NAMING_CATEGORIES["elegant"].copy()
                else:
                    available_words = AUTO_GEN_PREFIXES.copy()
                
                # Shuffle for randomness while ensuring variety
                random.shuffle(available_words)
                
                # Generate names with professional patterns
                patterns = [
                    "{word}-{suffix}",      # word-project, word-app
                    "{word}-{num:02d}",     # word-01, word-02  
                    "{word}-dev-{num:02d}", # word-dev-01
                    "{prefix}-{word}",      # project-word, app-word
                    "{word}"                # just word (for shorter lists)
                ]
                
                suffixes = ["project", "app", "repo", "hub", "lab", "studio", "works", "dev"]
                prefixes = ["my", "the", "new", "pro", "dev", "test", "demo"]
                
                used_names = set()
                
                for i in range(count):
                    # Select word (cycle through if needed)
                    word = available_words[i % len(available_words)]
                    
                    # Choose pattern based on position for variety
                    if count <= 20:
                        # For small counts, use simpler patterns
                        pattern = patterns[i % 3]  # Use first 3 patterns
                    else:
                        # For larger counts, use all patterns
                        pattern = patterns[i % len(patterns)]
                    
                    # Generate name based on pattern
                    if pattern == "{word}-{suffix}":
                        suffix = suffixes[i % len(suffixes)]
                        name = f"{word}-{suffix}"
                    elif pattern == "{word}-{num:02d}":
                        name = f"{word}-{i+1:02d}"
                    elif pattern == "{word}-dev-{num:02d}":
                        name = f"{word}-dev-{i+1:02d}"
                    elif pattern == "{prefix}-{word}":
                        prefix = prefixes[i % len(prefixes)]
                        name = f"{prefix}-{word}"
                    else:  # {word}
                        name = f"{word}-{i+1:02d}" if i > 0 else word
                    
                    # Ensure uniqueness
                    original_name = name
                    counter = 1
                    while name in used_names:
                        name = f"{original_name}-{counter}"
                        counter += 1
                    
                    used_names.add(name)
                    names.append(name)
                
                return names
            
            elif self.radio_custom.isChecked():
                prefix = self.txt_custom_prefix.text().strip()
                if not prefix:
                    prefix = "repo"
                return [f"{prefix}-{i+1:02d}" for i in range(count)]
            
            elif self.radio_sequential.isChecked():
                prefix = self.txt_sequential_prefix.text().strip()
                if not prefix:
                    prefix = "project"
                return [f"{prefix}-{i+1:02d}" for i in range(count)]
            
            elif self.radio_import.isChecked():
                filename = self.txt_names_file.text().strip()
                if not filename or not Path(filename).exists():
                    return []
                
                names = read_lines_from_file(filename)
                return names[:count]
            
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Error generating names: {e}")
            return []
    
    def get_config(self):
        """Get configuration from this tab"""
        # Determine strategy
        if self.radio_auto.isChecked():
            strategy = STRATEGY_AUTO_GENERATE
        elif self.radio_custom.isChecked():
            strategy = STRATEGY_CUSTOM
        elif self.radio_sequential.isChecked():
            strategy = STRATEGY_SEQUENTIAL
        else:
            strategy = STRATEGY_IMPORT_FILE
        
        return {
            'repo_count': self.slider_repo_count.value(),
            'naming_strategy': {
                'strategy': strategy,
                'category': self.combo_naming_category.currentIndex(),
                'custom_prefix': self.txt_custom_prefix.text().strip(),
                'sequential_prefix': self.txt_sequential_prefix.text().strip(),
                'names_file': self.txt_names_file.text().strip()
            },
            'private': self.radio_private.isChecked(),
            'auto_init': self.chk_init_readme.isChecked(),
            'description': self.txt_description.text().strip()
        }
    
    def set_config(self, config):
        """Set configuration to this tab"""
        # Set repo count
        self.slider_repo_count.setValue(config.get('repo_count', DEFAULT_REPO_COUNT))
        
        # Set naming strategy
        naming = config.get('naming_strategy', {})
        strategy = naming.get('strategy', STRATEGY_AUTO_GENERATE)
        
        if strategy == STRATEGY_AUTO_GENERATE:
            self.radio_auto.setChecked(True)
            # Set category selection
            category_index = naming.get('category', 0)  # Default to Mixed
            self.combo_naming_category.setCurrentIndex(category_index)
        elif strategy == STRATEGY_CUSTOM:
            self.radio_custom.setChecked(True)
            self.txt_custom_prefix.setText(naming.get('custom_prefix', ''))
        elif strategy == STRATEGY_SEQUENTIAL:
            self.radio_sequential.setChecked(True)
            self.txt_sequential_prefix.setText(naming.get('sequential_prefix', ''))
        elif strategy == STRATEGY_IMPORT_FILE:
            self.radio_import.setChecked(True)
            self.txt_names_file.setText(naming.get('names_file', ''))
        
        # Set options
        if config.get('private', True):
            self.radio_private.setChecked(True)
        else:
            self.radio_public.setChecked(True)
        
        self.chk_init_readme.setChecked(config.get('auto_init', True))
        self.txt_description.setText(config.get('description', ''))
