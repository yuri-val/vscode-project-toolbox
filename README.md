# Technical Documentation: VSCode Project Toolbox (Python + PyQt)

## 1. Overview

The VSCode Project Toolbox is a Python-based desktop application designed to manage and quickly open Visual Studio Code projects. It provides a user-friendly graphical interface where users can view and launch recent projects or add custom workspaces, enhancing productivity.

---

## 2. Features

1. **Project/Workspace Management**
   - Automatically fetches and displays a list of recent projects from VSCode.
   - Allows users to add custom projects or workspaces manually.
   - Displays project metadata such as the folder path and last opened date.

2. **Quick Launch**
   - Opens any project directly in VSCode with a double-click.
   - Utilizes the `code` CLI tool for seamless integration with VSCode.

3. **Search and Filter**
   - Real-time search to quickly locate projects by name or path.

4. **Cross-Platform Compatibility**
   - Runs on macOS and other platforms where Python and PyQt are supported.

5. **Customization**
   - Configurable settings for default project directories or additional features.

---

## 3. System Requirements

- **Operating System**: macOS, Windows, or Linux.
- **Python Version**: 3.8 or higher.
- **Dependencies**:
  - PyQt5
  - JSON (Python standard library)
  - Subprocess (Python standard library)

---

## 4. Architecture

### 4.1 Layers
1. **UI Layer**: Built using PyQt5 to provide a responsive and native-like graphical interface.
2. **Data Layer**: Reads and parses VSCode's `storage.json` file to retrieve recent projects.
3. **Integration Layer**: Executes shell commands to open projects in VSCode via the `code` CLI tool.

### 4.2 File Locations
- Recent projects are stored in `~/Library/Application Support/Code/User/storage.json` on macOS. The application reads this file to populate the project list.

### 4.3 Workflow
1. On startup, the app reads the `storage.json` file to fetch recent projects.
2. Users can add custom projects manually or via a drag-and-drop feature.
3. Double-clicking on a project launches it in VSCode using the CLI.

---

## 5. UI/UX Design

### 5.1 Main Window
- **Header**: Application title and a search bar for filtering projects.
- **Main Body**: A list of projects with the following details:
  - Project name.
  - Path.
  - Last opened date (if available).
- **Footer**: Buttons for adding or removing projects.

### 5.2 Interaction
- Projects are opened with a double-click.
- Real-time search updates the displayed project list as users type.

---

## 6. Implementation Details

### 6.1 Programming Language
- **Python**: Easy to learn and widely used, with extensive libraries for GUI and system interaction.

### 6.2 Key Dependencies
- **PyQt5**: For creating the graphical user interface.
- **JSON**: For parsing VSCode's `storage.json` file.
- **Subprocess**: For executing shell commands.

### 6.3 Fetching Recent Projects
Use Python's `os` and `json` modules to locate and parse the `storage.json` file. Example structure:
```json
{
  "openedPathsList": {
    "workspaces2": [
      "file:///Users/user/Development/ProjectA",
      "file:///Users/user/Development/ProjectB"
    ]
  }
}
```

### 6.4 Launching Projects
Execute the following command to open a project in VSCode:
```bash
code /path/to/project
```

---

## 7. Example Code

### 7.1 Main Application Code
```python name=toolbox.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget
import subprocess
import json
import os

class ToolboxApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VSCode Toolbox")
        self.resize(800, 600)
        
        # Main Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Project List
        self.project_list = QListWidget()
        self.layout.addWidget(self.project_list)

        # Load Recent Projects
        self.load_recent_projects()
        self.project_list.itemDoubleClicked.connect(self.open_project)

    def load_recent_projects(self):
        storage_path = os.path.expanduser("~/Library/Application Support/Code/User/storage.json")
        if os.path.exists(storage_path):
            with open(storage_path, "r") as f:
                data = json.load(f)
                projects = data.get("openedPathsList", {}).get("workspaces2", [])
                for project in projects:
                    self.project_list.addItem(project.replace("file://", ""))

    def open_project(self, item):
        project_path = item.text()
        subprocess.run(["code", project_path])

if __name__ == "__main__":
    app = QApplication([])
    window = ToolboxApp()
    window.show()
    app.exec_()
```

---

## 8. Installation and Usage

### 8.1 Installation
1. Install Python 3.8 or higher from [python.org](https://www.python.org/).
2. Ensure you have `pip` (Python's package installer) available.
3. Install PyQt5 using pip:
   ```bash
   pip install PyQt5
   ```
   *Note: Depending on your system configuration, you might need to use `pip3` instead of `pip`.*

### 8.2 Usage
1. Save the `toolbox.py` script to a file.
2. Run the script from your terminal:
   ```bash
   python toolbox.py
   ```
   *Note: Depending on your system configuration, you might need to use `python3` instead of `python`.*
3. Double-click a project in the list to open it in VSCode. Ensure the `code` command-line tool is installed and in your system's PATH (this is usually an option during VSCode installation).

---

## 9. Packaging for macOS (.app)

You can package this application into a standard macOS `.app` bundle using `pyinstaller`.

### 9.1 Installation of PyInstaller
Install `pyinstaller` using pip:
```bash
pip install pyinstaller
# or pip3 install pyinstaller
```

### 9.2 Building the Application
1.  Navigate to the directory containing `toolbox.py` in your terminal.
2.  Run the following `pyinstaller` command:

    ```bash
    pyinstaller --windowed --onefile --name VSCodeToolbox --icon=icon.icns toolbox.py
    ```

    *   `--windowed`: Prevents a terminal window from appearing when the app runs.
    *   `--onefile`: Bundles everything into a single executable file within the `.app` structure (optional, creates a larger initial file but simpler distribution). Remove this if you prefer a folder distribution.
    *   `--name VSCodeToolbox`: Sets the name of the output application bundle (e.g., `VSCodeToolbox.app`).
    *   `--icon=YourIcon.icns`: (Optional) Specify a path to an `.icns` file to use as the application icon. You'll need to create or find an icon file. If omitted, a default icon is used.
    *   `toolbox.py`: Your main script file.

3.  `pyinstaller` will create a `dist` folder. Inside `dist`, you will find `VSCodeToolbox.app`.
4.  You can move `VSCodeToolbox.app` to your `/Applications` folder or run it directly.

### 9.3 Notes
*   **Dependencies:** `pyinstaller` attempts to bundle necessary dependencies (like PyQt5), but sometimes specific libraries might need manual configuration in a `.spec` file (generated by `pyinstaller` on the first run without `--onefile`).
*   **Permissions:** On recent macOS versions, the packaged app might require explicit permissions (e.g., Accessibility, Files and Folders) to function correctly, especially for interacting with VS Code's files or launching processes. The system should prompt you when needed.
*   **`code` command:** The packaged app still relies on the `code` command-line tool being installed and accessible in the system's PATH.

---

## 10. Future Enhancements

1. **Drag-and-Drop Support**: Allow users to drag and drop folders to add custom projects.
2. **Git Integration**: Display the current Git branch for each project.
3. **Tagging and Grouping**: Enable users to organize projects based on tags or categories.
4. **Cloud Sync**: Sync project lists across devices using cloud storage.

---

## 11. Conclusion

The Python + PyQt5-based VSCode Project Toolbox offers a lightweight and customizable solution for managing and launching Visual Studio Code projects. Its focus on simplicity and extensibility makes it an ideal tool for developers.