"""
Files Tab for Github&Tailscale-Automation
Author: Haseeb Kaloya

File and folder selection for uploading
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog, QMessageBox,
    QListView, QTreeView, QAbstractItemView
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont
from pathlib import Path
import os

from utils.validators import validate_file_path, validate_folder_path
from utils.helpers import count_files_in_directory, get_directory_size, format_file_size
from utils.logger import get_logger
from core.constants import FILTER_WORKFLOW, FILTER_GITIGNORE
from gui.responsive_widgets import ResponsiveContainer, OptimalFormLayout
from gui.styles import GROUPBOX_STYLE, INPUT_STYLE, BUTTON_PRIMARY, CHECKBOX_STYLE

class TabFiles(QWidget):
    """Files tab widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.logger = get_logger()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        # Create responsive container
        container = ResponsiveContainer(self, max_width=1150)
        
        # Set container as main widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        
        # Get content layout from container
        content_layout = container.get_layout()
        
        # Workflow File Section
        self.create_workflow_section(content_layout)
        
        # Project Folder Section
        self.create_folder_section(content_layout)
        
        # .gitignore Section
        self.create_gitignore_section(content_layout)
        
        # Validate Button
        self.create_validate_section(content_layout)
        
        # Spacer
        content_layout.addStretch()
    
    def create_workflow_section(self, parent_layout):
        """Create workflow file section"""
        group_box = QGroupBox("GitHub Workflow File (.yml)")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # File path
        self.txt_workflow_path = QLineEdit()
        self.txt_workflow_path.setPlaceholderText("Select workflow file (.yml)...")
        self.txt_workflow_path.setReadOnly(True)
        self.txt_workflow_path.setStyleSheet(INPUT_STYLE)
        self.txt_workflow_path.setMinimumHeight(40)
        
        btn_browse = QPushButton("Browse...")
        btn_browse.setFixedSize(120, 40)
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.setStyleSheet(BUTTON_PRIMARY)
        btn_browse.clicked.connect(self.browse_workflow)
        
        path_row = OptimalFormLayout.create_field_row(
            "Path:",
            self.txt_workflow_path,
            btn_browse,
            label_width=100
        )
        layout.addLayout(path_row)
        
        # Upload checkbox
        self.chk_upload_workflow = QCheckBox("Upload to all repositories")
        self.chk_upload_workflow.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 5px;")
        layout.addWidget(self.chk_upload_workflow)
        
        # Info label
        self.lbl_workflow_info = QLabel("Target location: .github/workflows/main.yml")
        self.lbl_workflow_info.setStyleSheet("""
            color: #0078D4;
            font-style: italic;
            font-size: 10pt;
            padding: 8px;
            background-color: transparent;
            border-left: 3px solid #0078D4;
            border-radius: 4px;
        """)
        layout.addWidget(self.lbl_workflow_info)
        
        parent_layout.addWidget(group_box)
    
    def create_folder_section(self, parent_layout):
        """Create project folder/file section"""
        group_box = QGroupBox("Project Files/Folders (Optional)")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Store selected paths
        self.selected_paths = []  # List to store multiple paths
        
        # File/Folder path display
        self.txt_folder_path = QLineEdit()
        self.txt_folder_path.setPlaceholderText("Select project files/folders to upload (multiple selection supported)...")
        self.txt_folder_path.setReadOnly(True)
        self.txt_folder_path.setStyleSheet(INPUT_STYLE)
        self.txt_folder_path.setMinimumHeight(40)
        
        btn_browse = QPushButton("Browse...")
        btn_browse.setFixedSize(120, 40)
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.setStyleSheet(BUTTON_PRIMARY)
        btn_browse.clicked.connect(self.browse_folder)
        
        path_row = OptimalFormLayout.create_field_row(
            "Path:",
            self.txt_folder_path,
            btn_browse,
            label_width=100
        )
        layout.addLayout(path_row)
        
        # Info label
        self.lbl_folder_info = QLabel("")
        self.lbl_folder_info.setAlignment(Qt.AlignCenter)
        self.lbl_folder_info.setStyleSheet("""
            QLabel {
                color: #0078D4;
                font-weight: bold;
                padding: 8px;
                background-color: transparent;
                border-radius: 4px;
                font-size: 10pt;
            }
        """)
        layout.addWidget(self.lbl_folder_info)
        
        # Options row
        options_layout = QHBoxLayout()
        
        self.chk_upload_folder = QCheckBox("Upload to all repositories")
        self.chk_upload_folder.setChecked(True)
        self.chk_upload_folder.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 5px;")
        options_layout.addWidget(self.chk_upload_folder)
        
        options_layout.addStretch()
        
        btn_preview = QPushButton("Preview...")
        btn_preview.setFixedSize(150, 40)
        btn_preview.setCursor(Qt.PointingHandCursor)
        btn_preview.setStyleSheet(BUTTON_PRIMARY)
        btn_preview.clicked.connect(self.preview_folder)
        options_layout.addWidget(btn_preview)
        
        layout.addLayout(options_layout)
        
        # Dynamic target location label
        self.lbl_target_location = QLabel("Target location: (No file/folder selected)")
        self.lbl_target_location.setStyleSheet("""
            color: #0078D4;
            font-style: italic;
            font-size: 10pt;
            padding: 8px;
            background-color: transparent;
            border-left: 3px solid #0078D4;
            border-radius: 4px;
        """)
        layout.addWidget(self.lbl_target_location)
        
        parent_layout.addWidget(group_box)
    
    def create_gitignore_section(self, parent_layout):
        """Create .gitignore section"""
        group_box = QGroupBox(".gitignore File (Optional)")
        group_box.setFont(QFont("Segoe UI", 11, QFont.Bold))
        group_box.setStyleSheet(GROUPBOX_STYLE)
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # File path
        self.txt_gitignore_path = QLineEdit()
        self.txt_gitignore_path.setPlaceholderText("Select .gitignore file...")
        self.txt_gitignore_path.setReadOnly(True)
        self.txt_gitignore_path.setStyleSheet(INPUT_STYLE)
        self.txt_gitignore_path.setMinimumHeight(40)
        
        btn_browse = QPushButton("Browse...")
        btn_browse.setFixedSize(120, 40)
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.setStyleSheet(BUTTON_PRIMARY)
        btn_browse.clicked.connect(self.browse_gitignore)
        
        path_row = OptimalFormLayout.create_field_row(
            "Path:",
            self.txt_gitignore_path,
            btn_browse,
            label_width=100
        )
        layout.addLayout(path_row)
        
        # Upload checkbox
        self.chk_upload_gitignore = QCheckBox("Upload to all repositories")
        self.chk_upload_gitignore.setChecked(False)
        self.chk_upload_gitignore.setStyleSheet(CHECKBOX_STYLE + " font-size: 10pt; padding: 5px;")
        layout.addWidget(self.chk_upload_gitignore)
        
        # Info label
        lbl_info = QLabel("Target location: /.gitignore")
        lbl_info.setStyleSheet("""
            color: #0078D4;
            font-style: italic;
            font-size: 10pt;
            padding: 8px;
            background-color: transparent;
            border-left: 3px solid #0078D4;
            border-radius: 4px;
        """)
        layout.addWidget(lbl_info)
        
        parent_layout.addWidget(group_box)
    
    def create_validate_section(self, parent_layout):
        """Create validation section"""
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_validate = QPushButton("Validate All Files")
        btn_validate.setFixedSize(200, 45)
        btn_validate.setCursor(Qt.PointingHandCursor)
        btn_validate.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00C853,
                    stop:1 #00B050
                );
                color: white;
                border: 2px solid #00A040;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00E676,
                    stop:1 #00C853
                );
            }
            QPushButton:pressed {
                background: #00A040;
                padding-top: 12px;
            }
        """)
        btn_validate.clicked.connect(self.validate_files)
        btn_layout.addWidget(btn_validate)
        
        parent_layout.addLayout(btn_layout)
    
    def browse_workflow(self):
        """Browse for workflow file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Workflow File",
            "",
            FILTER_WORKFLOW
        )
        
        if filename:
            self.txt_workflow_path.setText(filename)
            self.logger.info(f"Workflow file selected: {filename}")
    
    def browse_folder(self):
        """Browse for project files or folders (multiple selection supported)"""
        # Show custom selection dialog
        selected_items = self.show_file_folder_dialog()
        
        if selected_items:
            # Store all selected paths
            self.selected_paths = selected_items
            self.logger.info(f"Selected {len(selected_items)} item(s): {selected_items}")
            
            # Update display
            self.update_multiple_items_display()
    
    def show_file_folder_dialog(self):
        """Professional file/folder selection dialog with clear options"""
        from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                   QPushButton, QListWidget, QListWidgetItem,
                                   QButtonGroup, QRadioButton, QMessageBox)
        from PyQt5.QtCore import Qt
        
        # Create custom dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Files & Folders")
        dialog.setFixedSize(600, 500)
        dialog.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Choose what you want to upload:")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color: #0078D4; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Selection mode buttons
        mode_group = QButtonGroup(dialog)
        mode_layout = QHBoxLayout()
        
        radio_files = QRadioButton("Select Files")
        radio_files.setChecked(True)
        radio_files.setStyleSheet("font-size: 11pt; padding: 8px;")
        mode_group.addButton(radio_files)
        mode_layout.addWidget(radio_files)
        
        radio_folders = QRadioButton("Select Folders")
        radio_folders.setStyleSheet("font-size: 11pt; padding: 8px;")
        mode_group.addButton(radio_folders)
        mode_layout.addWidget(radio_folders)
        
        radio_mixed = QRadioButton("Select Both")
        radio_mixed.setStyleSheet("font-size: 11pt; padding: 8px;")
        mode_group.addButton(radio_mixed)
        mode_layout.addWidget(radio_mixed)
        
        mode_layout.addStretch()
        layout.addLayout(mode_layout)
        
        # Selected items display
        selected_label = QLabel("Selected Items:")
        selected_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        layout.addWidget(selected_label)
        
        selected_list = QListWidget()
        selected_list.setMaximumHeight(150)
        selected_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: #FFFFFF;
                font-size: 10pt;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #F0F0F0;
            }
        """)
        layout.addWidget(selected_list)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        btn_add = QPushButton("Add Items")
        btn_add.setFixedSize(120, 40)
        btn_add.setStyleSheet(BUTTON_PRIMARY)
        control_layout.addWidget(btn_add)
        
        btn_remove = QPushButton("Remove")
        btn_remove.setFixedSize(120, 40)
        btn_remove.setStyleSheet("""
            QPushButton {
                background: #FF6B6B;
                color: white;
                border: 2px solid #FF5252;
                border-radius: 6px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background: #FF5252;
            }
        """)
        control_layout.addWidget(btn_remove)
        
        btn_clear = QPushButton("Clear All")
        btn_clear.setFixedSize(120, 40)
        btn_clear.setStyleSheet("""
            QPushButton {
                background: #9E9E9E;
                color: white;
                border: 2px solid #757575;
                border-radius: 6px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background: #757575;
            }
        """)
        control_layout.addWidget(btn_clear)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedSize(100, 40)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background: #9E9E9E;
                color: white;
                border: 2px solid #757575;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #757575;
            }
        """)
        button_layout.addWidget(btn_cancel)
        
        btn_ok = QPushButton("OK")
        btn_ok.setFixedSize(100, 40)
        btn_ok.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: 2px solid #45A049;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #45A049;
            }
        """)
        button_layout.addWidget(btn_ok)
        
        layout.addLayout(button_layout)
        
        # Store selected paths
        selected_paths = []
        
        def add_items():
            """Add files or folders based on current mode"""
            if radio_files.isChecked():
                # File selection mode
                files, _ = QFileDialog.getOpenFileNames(
                    dialog,
                    "Select Files",
                    "",
                    "All Files (*.*)"
                )
                for file_path in files:
                    if file_path not in selected_paths:
                        selected_paths.append(file_path)
                        item = QListWidgetItem(f"[File] {Path(file_path).name}")
                        item.setData(Qt.UserRole, file_path)
                        item.setToolTip(file_path)
                        selected_list.addItem(item)
            
            elif radio_folders.isChecked():
                # Folder selection mode
                folder = QFileDialog.getExistingDirectory(
                    dialog,
                    "Select Folder"
                )
                if folder and folder not in selected_paths:
                    selected_paths.append(folder)
                    item = QListWidgetItem(f"[Folder] {Path(folder).name}")
                    item.setData(Qt.UserRole, folder)
                    item.setToolTip(folder)
                    selected_list.addItem(item)
            
            else:
                # Mixed mode - show submenu
                from PyQt5.QtWidgets import QMenu, QAction
                menu = QMenu(dialog)
                
                action_files = QAction("Add Files", menu)
                action_folder = QAction("Add Folder", menu)
                
                menu.addAction(action_files)
                menu.addAction(action_folder)
                
                action = menu.exec_(btn_add.mapToGlobal(btn_add.rect().bottomLeft()))
                
                if action == action_files:
                    files, _ = QFileDialog.getOpenFileNames(
                        dialog,
                        "Select Files",
                        "",
                        "All Files (*.*)"
                    )
                    for file_path in files:
                        if file_path not in selected_paths:
                            selected_paths.append(file_path)
                            item = QListWidgetItem(f"[File] {Path(file_path).name}")
                            item.setData(Qt.UserRole, file_path)
                            item.setToolTip(file_path)
                            selected_list.addItem(item)
                
                elif action == action_folder:
                    folder = QFileDialog.getExistingDirectory(
                        dialog,
                        "Select Folder"
                    )
                    if folder and folder not in selected_paths:
                        selected_paths.append(folder)
                        item = QListWidgetItem(f"[Folder] {Path(folder).name}")
                        item.setData(Qt.UserRole, folder)
                        item.setToolTip(folder)
                        selected_list.addItem(item)
        
        def remove_selected():
            """Remove selected item from list"""
            current_row = selected_list.currentRow()
            if current_row >= 0:
                item = selected_list.takeItem(current_row)
                if item:
                    path = item.data(Qt.UserRole)
                    if path in selected_paths:
                        selected_paths.remove(path)
        
        def clear_all():
            """Clear all selected items"""
            selected_list.clear()
            selected_paths.clear()
        
        def accept_selection():
            """Accept and return selected paths"""
            if not selected_paths:
                QMessageBox.information(dialog, "Info", "Please select at least one file or folder.")
                return
            dialog.accept()
        
        # Connect signals
        btn_add.clicked.connect(add_items)
        btn_remove.clicked.connect(remove_selected)
        btn_clear.clicked.connect(clear_all)
        btn_ok.clicked.connect(accept_selection)
        btn_cancel.clicked.connect(dialog.reject)
        
        # Execute dialog
        if dialog.exec_() == QDialog.Accepted:
            return selected_paths
        
        return []
    
    def update_multiple_items_display(self):
        """Update display for multiple selected items"""
        if not self.selected_paths:
            self.txt_folder_path.clear()
            self.lbl_folder_info.setText("")
            self.update_target_location()
            return
        
        try:
            total_files = 0
            total_size = 0
            file_count = 0
            folder_count = 0
            
            # Count and calculate totals
            for path_str in self.selected_paths:
                path_obj = Path(path_str)
                if path_obj.is_file():
                    file_count += 1
                    total_files += 1
                    total_size += path_obj.stat().st_size
                elif path_obj.is_dir():
                    folder_count += 1
                    total_files += count_files_in_directory(path_str)
                    total_size += get_directory_size(path_str)
            
            # Update path display
            if len(self.selected_paths) == 1:
                self.txt_folder_path.setText(self.selected_paths[0])
            else:
                self.txt_folder_path.setText(f"{len(self.selected_paths)} items selected")
            
            # Update info label
            items_text = []
            if file_count > 0:
                items_text.append(f"{file_count} file(s)")
            if folder_count > 0:
                items_text.append(f"{folder_count} folder(s)")
            
            info_text = " + ".join(items_text) + f" | Total files: {total_files} | Size: {format_file_size(total_size)}"
            self.lbl_folder_info.setText(info_text)
            self.lbl_folder_info.setStyleSheet("color: #00B050;")
            
            # Update target location
            self.update_target_location()
            
        except Exception as e:
            self.lbl_folder_info.setText("Error reading items")
            self.lbl_folder_info.setStyleSheet("color: #C00000;")
            self.logger.error(f"Error reading items: {e}")
    
    def update_item_info(self, path):
        """Update info label based on selected file or folder (for single item)"""
        try:
            from pathlib import Path
            path_obj = Path(path)
            
            if path_obj.is_file():
                # Single file
                file_size = path_obj.stat().st_size
                self.lbl_folder_info.setText(f"File: {path_obj.name} | Size: {format_file_size(file_size)}")
                self.lbl_folder_info.setStyleSheet("color: #00B050;")
            elif path_obj.is_dir():
                # Folder
                file_count = count_files_in_directory(path)
                folder_size = get_directory_size(path)
                self.lbl_folder_info.setText(f"Files: {file_count} | Size: {format_file_size(folder_size)}")
                self.lbl_folder_info.setStyleSheet("color: #00B050;")
            else:
                self.lbl_folder_info.setText("Invalid path")
                self.lbl_folder_info.setStyleSheet("color: #C00000;")
        except Exception as e:
            self.lbl_folder_info.setText("Error reading item")
            self.lbl_folder_info.setStyleSheet("color: #C00000;")
            self.logger.error(f"Error reading item: {e}")
    
    def update_target_location(self):
        """Update target location label dynamically for multiple items"""
        if not self.selected_paths:
            self.lbl_target_location.setText("🎯 Target location: (No files/folders selected)")
            return
        
        if len(self.selected_paths) == 1:
            # Single item
            from pathlib import Path
            path_obj = Path(self.selected_paths[0])
            item_name = path_obj.name
            self.lbl_target_location.setText(f"🎯 Target location: /{item_name}")
        else:
            # Multiple items - show all names
            from pathlib import Path
            item_names = [Path(p).name for p in self.selected_paths]
            if len(item_names) <= 3:
                names_display = ", ".join([f"/{name}" for name in item_names])
            else:
                names_display = ", ".join([f"/{name}" for name in item_names[:3]]) + f" (+{len(item_names)-3} more)"
            self.lbl_target_location.setText(f"🎯 Target locations: {names_display}")
    
    def browse_gitignore(self):
        """Browse for .gitignore file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select .gitignore File",
            "",
            FILTER_GITIGNORE
        )
        
        if filename:
            self.txt_gitignore_path.setText(filename)
            self.logger.info(f".gitignore file selected: {filename}")
    
    def preview_folder(self):
        """Preview selected file(s) or folder(s) in file explorer"""
        if not self.selected_paths:
            QMessageBox.warning(self, "Warning", "Please select files or folders first.")
            return
        
        # Preview first item (or all if multiple)
        item_path = self.selected_paths[0]
        path_obj = Path(item_path)
        if not path_obj.exists():
            QMessageBox.warning(self, "Warning", "The selected path does not exist.")
            return
        
        # Open in file explorer
        import subprocess
        import platform
        
        try:
            if platform.system() == 'Windows':
                # If it's a file, use /select to highlight it in explorer
                if path_obj.is_file():
                    subprocess.Popen(['explorer', '/select,', str(path_obj)])
                else:
                    subprocess.Popen(['explorer', str(path_obj)])
            elif platform.system() == 'Darwin':  # macOS
                if path_obj.is_file():
                    subprocess.Popen(['open', '-R', str(path_obj)])
                else:
                    subprocess.Popen(['open', str(path_obj)])
            else:  # Linux
                # Open parent folder for files
                if path_obj.is_file():
                    subprocess.Popen(['xdg-open', str(path_obj.parent)])
                else:
                    subprocess.Popen(['xdg-open', str(path_obj)])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open folder:\n{str(e)}")
    
    def validate_files(self):
        """Validate all selected files"""
        errors = []
        
        # Validate workflow file
        if self.chk_upload_workflow.isChecked():
            workflow_path = self.txt_workflow_path.text().strip()
            if not workflow_path:
                errors.append("Workflow file path is empty")
            else:
                is_valid, error_msg = validate_file_path(workflow_path)
                if not is_valid:
                    errors.append(f"Workflow file: {error_msg}")
        
        # Validate project folder
        if self.chk_upload_folder.isChecked():
            folder_path = self.txt_folder_path.text().strip()
            if not folder_path:
                errors.append("Project folder path is empty")
            else:
                is_valid, error_msg = validate_folder_path(folder_path)
                if not is_valid:
                    errors.append(f"Project folder: {error_msg}")
        
        # Validate .gitignore
        if self.chk_upload_gitignore.isChecked():
            gitignore_path = self.txt_gitignore_path.text().strip()
            if not gitignore_path:
                errors.append(".gitignore file path is empty")
            else:
                is_valid, error_msg = validate_file_path(gitignore_path)
                if not is_valid:
                    errors.append(f".gitignore file: {error_msg}")
        
        # Show results
        if errors:
            QMessageBox.warning(
                self,
                "Validation Failed",
                "The following errors were found:\n\n" + "\n".join(f"• {e}" for e in errors)
            )
        else:
            QMessageBox.information(
                self,
                "Validation Successful",
                "All selected files are valid!"
            )
    
    def get_config(self):
        """Get configuration from this tab"""
        # Store multiple paths as a list (backward compatible)
        project_paths = self.selected_paths if self.chk_upload_folder.isChecked() else []
        
        return {
            'workflow_file': self.txt_workflow_path.text().strip() if self.chk_upload_workflow.isChecked() else '',
            'project_folder': project_paths[0] if len(project_paths) == 1 else '',  # Backward compatibility
            'project_paths': project_paths,  # New field for multiple paths
            'gitignore_file': self.txt_gitignore_path.text().strip() if self.chk_upload_gitignore.isChecked() else ''
        }
    
    def set_config(self, config):
        """Set configuration to this tab"""
        self.txt_workflow_path.setText(config.get('workflow_file', ''))
        self.txt_gitignore_path.setText(config.get('gitignore_file', ''))
        
        # Load multiple paths (new format) or single path (backward compatibility)
        if 'project_paths' in config and config['project_paths']:
            self.selected_paths = config['project_paths']
            self.update_multiple_items_display()
        elif config.get('project_folder'):
            # Backward compatibility with old single-path configs
            self.selected_paths = [config['project_folder']]
            self.update_multiple_items_display()
