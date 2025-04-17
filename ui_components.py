from PyQt5.QtWidgets import (QMainWindow, QListWidget, QVBoxLayout, QWidget,
                            QListWidgetItem, QLabel, QHBoxLayout, QLineEdit,
                            QPushButton, QFrame, QSizePolicy, QStyle)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize
import os  # Add this import for path operations

class ProjectListItem(QWidget):
    """Custom widget for project list items that looks more modern."""
    def __init__(self, folder_name, full_path, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 8, 10, 8)
        self.layout.setSpacing(12)  # Add spacing between icon and text container
        
        # Project icon (folder icon from system theme)
        self.icon_label = QLabel()
        self.icon_label.setPixmap(self.style().standardIcon(QStyle.SP_DirIcon).pixmap(24, 24))
        # Add padding to icon
        self.icon_label.setStyleSheet("padding: 4px; background-color: #3a3a3a; border-radius: 6px;")
        # Fix size for the icon container
        self.icon_label.setFixedSize(36, 36)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.icon_label)
        
        # Text container with vertical layout
        self.text_container = QWidget()
        self.text_container.setStyleSheet("background-color: #3a3a3a; border-radius: 8px; padding: 8px;")
        self.text_layout = QVBoxLayout(self.text_container)
        self.text_layout.setContentsMargins(8, 6, 8, 6)
        self.text_layout.setSpacing(4)  # Increased spacing between name and path
        
        # Project name with bold font
        self.name_label = QLabel(folder_name)
        font = QFont()
        font.setBold(True)
        self.name_label.setFont(font)
        self.name_label.setStyleSheet("background-color: transparent; padding: 2px 0px;")
        self.text_layout.addWidget(self.name_label)
        
        # Project path with smaller, gray font - with elided text to handle long paths
        self.path_label = QLabel(full_path)
        path_font = QFont()
        path_font.setPointSize(8)
        self.path_label.setFont(path_font)
        self.path_label.setStyleSheet("color: #888888; background-color: transparent; padding: 2px 0px;")
        
        # Enable text wrapping for long paths
        self.path_label.setWordWrap(True)
        # Set fixed width to avoid horizontal scrolling
        self.path_label.setMaximumWidth(500)
        # Use elided text (with ellipsis)
        self.path_label.setTextFormat(Qt.PlainText)
        
        self.text_layout.addWidget(self.path_label)
        
        self.layout.addWidget(self.text_container, 1)  # 1 stretch factor to take available space
        
        # Add rounded corners to the whole item
        self.setStyleSheet("QWidget { border-radius: 10px; }")

class ToolboxUI:
    def __init__(self, main_window):
        """Set up the UI components for the Toolbox application.
        
        Args:
            main_window: The main QMainWindow instance to set up
        """
        self.main_window = main_window
        self.setup_main_window()
        self.setup_widgets()
        self.apply_stylesheet()
        
    def setup_main_window(self):
        """Configure the main window properties."""
        self.main_window.setWindowTitle("VSCode Project Toolbox")
        self.main_window.resize(600, 800)
        
    def setup_widgets(self):
        """Create and configure all UI widgets."""
        # Main Widget
        self.central_widget = QWidget()
        self.main_window.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(15)
        
        # Header with title and search
        self.header = QWidget()
        self.header_layout = QVBoxLayout(self.header)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        
        # App title
        self.title_label = QLabel("VSCode Projects")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.header_layout.addWidget(self.title_label)
        
        # Search bar
        self.search_container = QWidget()
        self.search_layout = QHBoxLayout(self.search_container)
        self.search_layout.setContentsMargins(0, 10, 0, 10)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search projects...")
        self.search_input.setMinimumHeight(36)
        self.search_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Search")
        self.search_button.setMinimumHeight(36)
        self.search_layout.addWidget(self.search_button)
        
        self.header_layout.addWidget(self.search_container)
        self.layout.addWidget(self.header)
        
        # Separator line
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.separator)
        
        # Projects section title
        self.projects_label = QLabel("Recent Projects")
        projects_font = QFont()
        projects_font.setPointSize(12)
        projects_font.setBold(True)
        self.projects_label.setFont(projects_font)
        self.layout.addWidget(self.projects_label)
        
        # Project List
        self.project_list = QListWidget()
        self.project_list.setSpacing(4)  # Add spacing between items
        self.project_list.setUniformItemSizes(False)  # Allow variable height items
        self.project_list.setFrameShape(QFrame.NoFrame)  # Remove the border
        self.layout.addWidget(self.project_list)
        
        # Connect search functionality
        self.search_input.textChanged.connect(self.filter_projects)
        self.search_button.clicked.connect(lambda: self.filter_projects(self.search_input.text()))
    
    def apply_stylesheet(self):
        """Apply custom styling to make the app look modern."""
        # Main application style
        self.main_window.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
            }
            QListWidget {
                background-color: #333333;
                border-radius: 8px;
                padding: 5px;
                outline: none;
            }
            QListWidget::item {
                border-radius: 4px;
                margin: 2px 0px;
            }
            QListWidget::item:selected {
                background-color: #4a76c9;
            }
            QListWidget::item:hover {
                background-color: #3a3a3a;
            }
            QLineEdit {
                background-color: #333333;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 5px;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #4a76c9;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a86d9;
            }
            QPushButton:pressed {
                background-color: #3a66b9;
            }
            QFrame[frameShape="4"] { /* Horizontal line */
                color: #444444;
                background-color: #444444;
                height: 1px;
                border: none;
            }
        """)
        
        # Set dark mode palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.WindowText, QColor(224, 224, 224))
        dark_palette.setColor(QPalette.Base, QColor(51, 51, 51))
        dark_palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.Text, QColor(224, 224, 224))
        dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ButtonText, QColor(224, 224, 224))
        dark_palette.setColor(QPalette.Link, QColor(74, 118, 201))
        dark_palette.setColor(QPalette.Highlight, QColor(74, 118, 201))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        
        self.main_window.setPalette(dark_palette)
        
    def add_project_item(self, folder_name, full_path):
        """Add a project to the list with a custom widget for better appearance."""
        item = QListWidgetItem(self.project_list)
        
        # Get a shortened display version of the path
        display_path = self.shorten_path(full_path)
        
        custom_widget = ProjectListItem(folder_name, display_path)
        item.setSizeHint(custom_widget.sizeHint())
        self.project_list.setItemWidget(item, custom_widget)
        
        # Store the full path data for use when opening
        item.setData(Qt.UserRole, full_path)
        # Show full path on hover
        item.setToolTip(full_path)
        return item

    def shorten_path(self, path):
        """Shorten a long path for display purposes while keeping important parts."""
        # If path is short enough, return it as is
        if len(path) < 60:
            return path
            
        # For longer paths, keep the beginning and end parts
        parts = path.split(os.sep)
        
        # Handle paths with different lengths
        if len(parts) <= 4:
            return path  # Too short to meaningfully truncate
        
        # Keep first part (drive/root), ellipsis, and last 2-3 parts
        shortened_path = parts[0] + os.sep + "..." + os.sep + os.sep.join(parts[-3:])
        return shortened_path
        
    def get_project_list(self):
        """Return the project list widget."""
        return self.project_list
        
    def filter_projects(self, search_text):
        """Filter projects based on search text."""
        search_text = search_text.lower()
        for i in range(self.project_list.count()):
            item = self.project_list.item(i)
            widget = self.project_list.itemWidget(item)
            folder_name = widget.name_label.text().lower()
            full_path = widget.path_label.text().lower()
            
            # Show the item if the search text is in the name or path
            if search_text in folder_name or search_text in full_path:
                item.setHidden(False)
            else:
                item.setHidden(True)
