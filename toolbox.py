from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt  # Add this import for Qt.UserRole
import subprocess
import json
import os
import platform
import sqlite3
import urllib.parse
from ui_components import ToolboxUI  # Import the new UI class

class ToolboxApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set up the UI using our new UI class
        self.ui = ToolboxUI(self)
        self.project_list = self.ui.get_project_list()
        
        # Set a fixed width for the main window to prevent horizontal scrolling
        self.setMinimumWidth(600)
        self.setMaximumWidth(800)
        
        # Load Recent Projects
        self.load_recent_projects()
        self.project_list.itemDoubleClicked.connect(self.open_project)

    def find_storage_location(self):
        """Tries to find the VSCode storage.json or state.vscdb path."""
        system = platform.system()
        home = os.path.expanduser("~")
        
        # Prioritize state.vscdb as it's more common in recent versions
        db_possible_paths = []
        json_possible_paths = []

        if system == 'Darwin':  # macOS
            base_paths = [
                os.path.join(home, "Library/Application Support/Code/User/"),
                os.path.join(home, "Library/Application Support/Code - Insiders/User/"),
            ]
        elif system == 'Linux':
            base_paths = [
                os.path.join(home, ".config/Code/User/"),
                os.path.join(home, ".config/Code - Insiders/User/"),
                os.path.join(home, ".var/app/com.visualstudio.code/config/Code/User/"),
                os.path.join(home, ".var/app/com.visualstudio.code.insiders/config/Code/User/"),
            ]
        elif system == 'Windows':
            base_paths = [
                os.path.join(home, "AppData/Roaming/Code/User/"),
                os.path.join(home, "AppData/Roaming/Code - Insiders/User/"),
            ]
        else:
            base_paths = []

        for base in base_paths:
            db_possible_paths.append(os.path.join(base, "globalStorage/state.vscdb"))
            json_possible_paths.append(os.path.join(base, "storage.json"))

        # Check for state.vscdb first
        for path in db_possible_paths:
            if os.path.exists(path):
                print(f"Found state database at: {path}")
                return path, 'db'
        
        # Fallback to storage.json
        for path in json_possible_paths:
            if os.path.exists(path):
                print(f"Found storage file at: {path}")
                return path, 'json'
                
        print("Could not find VSCode state.vscdb or storage.json in common locations.")
        print("Checked paths:")
        for path in db_possible_paths + json_possible_paths:
            print(f"- {path}")
        return None, None

    def load_recent_projects_from_db(self, db_path):
        """Loads recent projects from the state.vscdb SQLite database."""
        projects = set()
        try:
            conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)  # Read-only connection
            cursor = conn.cursor()
            # Query for the key that stores recently opened paths.
            # This key might change between VSCode versions. 'history.recentlyOpenedPathsList' is common.
            cursor.execute("SELECT value FROM ItemTable WHERE key = 'history.recentlyOpenedPathsList'")
            result = cursor.fetchone()
            conn.close()

            if result:
                # The value is often a JSON string
                data = json.loads(result[0])
                entries = data.get('entries', [])
                for entry in entries:
                    uri_str = entry.get('folderUri') or entry.get('fileUri')  # Prefer folders, fallback to files
                    if uri_str and uri_str.startswith('file://'):
                        # Decode percent-encoded characters and normalize path
                        parsed_uri = urllib.parse.unquote(uri_str.replace('file://', ''))
                        project_path = os.path.normpath(parsed_uri)
                        # On Windows, remove leading '/' if present after replacing 'file://'
                        if platform.system() == 'Windows' and project_path.startswith('/'):
                            # Handle drive letters correctly, e.g., /C:/Users -> C:/Users
                            if len(project_path) > 2 and project_path[2] == ':':
                                project_path = project_path[1:]
                        projects.add(project_path)
            else:
                print(f"Key 'history.recentlyOpenedPathsList' not found in {db_path}")

        except sqlite3.Error as e:
            print(f"SQLite error reading {db_path}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from database: {e}")
        except Exception as e:
            print(f"An error occurred while processing {db_path}: {e}")
        
        return projects

    def load_recent_projects_from_json(self, storage_path):
        """Loads recent projects from the storage.json file."""
        projects = set()
        try:
            with open(storage_path, "r", encoding='utf-8') as f:
                data = json.load(f)
                recent_paths_data = data.get("openedPathsList", {})
                # Combine entries from different potential keys
                entries = recent_paths_data.get("entries", []) + \
                          recent_paths_data.get("workspaces3", []) + \
                          recent_paths_data.get("files2", []) + \
                          recent_paths_data.get("workspaces2", [])  # Older keys

                for entry in entries:
                    path_uri = None
                    if isinstance(entry, str):  # Older format like "file:///path" or workspace path
                        if entry.startswith("file://"):
                            path_uri = entry
                        elif entry.endswith(".code-workspace"):  # Handle workspace file paths directly
                            # Use the directory containing the .code-workspace file
                            project_path = os.path.dirname(os.path.normpath(entry))
                            projects.add(project_path)
                            continue  # Skip further processing for this entry
                    elif isinstance(entry, dict):  # Newer format with folderUri or workspace.configPath
                        path_uri = entry.get("folderUri") or entry.get("workspace", {}).get("configPath")

                    if path_uri and path_uri.startswith("file://"):
                        # Decode URI and normalize path
                        project_path = os.path.normpath(urllib.parse.unquote(path_uri.replace("file://", "")))
                        # On Windows, remove leading '/' if present after replacing 'file://'
                        if platform.system() == 'Windows' and project_path.startswith('/'):
                            if len(project_path) > 2 and project_path[2] == ':':
                                project_path = project_path[1:]
                        # Add the parent directory for .code-workspace files referenced by URI
                        if project_path.endswith(".code-workspace"):
                            project_path = os.path.dirname(project_path)
                        projects.add(project_path)

        except json.JSONDecodeError:
            print(f"Error reading or parsing {storage_path}")
        except Exception as e:
            print(f"An error occurred while processing {storage_path}: {e}")
        return projects

    def load_recent_projects(self):
        storage_location, storage_type = self.find_storage_location()
        processed_paths = set()

        if storage_type == 'db':
            processed_paths = self.load_recent_projects_from_db(storage_location)
        elif storage_type == 'json':
            processed_paths = self.load_recent_projects_from_json(storage_location)
        else:
            # Message already printed by find_storage_location
            return 

        # Clear existing list before adding new items
        self.project_list.clear()

        # Add unique paths to the list widget
        for project_path in sorted(list(processed_paths)):
            # Display only the folder name for brevity
            folder_name = os.path.basename(project_path)
            # Use the new custom item widget
            self.ui.add_project_item(folder_name, project_path)

    def open_project(self, item):
        # Retrieve the full path stored in the item's data
        project_path = item.data(1) or item.data(Qt.UserRole)  # Try both roles for compatibility
        if project_path:
            try:
                # Add the --new-window flag to force opening in a new VS Code window
                subprocess.run(["code", "--new-window", project_path], check=True)
            except FileNotFoundError:
                print("Error: 'code' command not found. Make sure VSCode is installed and added to your PATH.")
            except Exception as e:
                print(f"Failed to open project: {e}")
        else:
            print("Error: Could not retrieve project path.")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ToolboxApp()
    window.show()
    sys.exit(app.exec_())
