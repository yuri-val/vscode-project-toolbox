# 📦 VSCode Project Toolbox

## 🔍 Overview

VSCode Project Toolbox is a Python-based desktop application designed to help you manage and quickly access your Visual Studio Code projects. With a modern, dark-themed interface, it provides a seamless way to browse and launch your recent VSCode projects.

---

## ✨ Features

- 🚀 **Quick Launch** - Open any project in VSCode with just a double-click
- 🔍 **Smart Search** - Filter projects in real-time as you type
- 🌈 **Modern UI** - Clean, dark-themed interface with custom project items 
- 🔄 **Auto-Discovery** - Automatically detects and displays your recent VSCode projects
- 💻 **Cross-Platform** - Works on macOS, Windows, and Linux

---

## 🖥️ Screenshots

[Screenshots would go here]

---

## 🛠️ System Requirements

- **Operating System**: macOS, Windows, or Linux
- **Python**: Version 3.8 or higher
- **Dependencies**: PyQt5, SQLite3 (built into Python)
- **VSCode**: Must have the `code` command-line tool installed

---

## ⚙️ Architecture

### Application Structure

The application is organized into three main Python files:

1. **`main.py`** - Entry point that initializes the application
2. **`toolbox.py`** - Core functionality for detecting and opening projects
3. **`ui_components.py`** - UI components and styling for the application

### Data Sources

The application can read recent projects from:
- **SQLite database** (`state.vscdb`) - Used by newer versions of VSCode
- **JSON file** (`storage.json`) - Used by older versions of VSCode

---

## 📊 Implementation Details

### Project Detection

The application automatically finds your VSCode configuration by checking common installation paths based on your operating system. It supports:

- Standard VSCode installation
- VSCode Insiders builds
- Flatpak installations (Linux)

### User Interface

Built with PyQt5, featuring:
- Custom-styled project list items
- Modern dark theme with accent colors
- Responsive layout with proper scrolling
- Search functionality with real-time filtering

---

## 📥 Installation

1. **Install Python 3.8 or higher**
   ```
   https://www.python.org/downloads/
   ```

2. **Install PyQt5**
   ```bash
   pip install PyQt5
   ```
   *Note: You might need to use `pip3` instead of `pip` depending on your system.*

3. **Ensure VSCode's CLI is available**
   The `code` command should be accessible from your terminal.
   In VSCode, you can install this by pressing `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux)
   and running "Shell Command: Install 'code' command in PATH".

---

## 🚀 Usage

1. **Start the application**
   ```bash
   python main.py
   ```
   *Note: You might need to use `python3` instead of `python` depending on your system.*

2. **Find your project** using the search bar at the top

3. **Double-click any project** to open it in VSCode

---

## 📦 Packaging

### Manual Packaging

#### For macOS (.app)

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Create the application bundle**
   ```bash
   pyinstaller --onefile --windowed --name "VSCode Project Toolbox" --icon=assets/icon.icns main.py
   ```

   Options:
   - `--onefile`: Packages everything into a single executable
   - `--windowed`: Prevents a terminal window from appearing
   - `--name`: Sets the application name
   - `--icon`: Path to an .icns file for the app icon

3. **Find your application** in the `dist` folder

#### For Windows (.exe)

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Create the executable**
   ```bash
   pyinstaller --onefile --windowed --name "VSCode Project Toolbox" --icon=assets/icon.ico main.py
   ```

3. **Find your application** in the `dist` folder

#### For Linux

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Create the executable**
   ```bash
   pyinstaller --onefile --windowed --name "VSCode Project Toolbox" main.py
   ```

3. **Find your application** in the `dist` folder

### 🔄 Automated Builds via GitHub Actions

This project includes a GitHub Actions workflow that automatically builds executables for multiple platforms when a new tag is pushed to the repository:

- **Windows**: 64-bit executable (.exe)
- **macOS**: Intel and Apple Silicon builds
- **Linux**: 64-bit executable

To create a new release:

1. **Tag your commit**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Wait for the build workflow to complete**
   The GitHub Action will automatically:
   - Build the application for all platforms
   - Create a new GitHub Release with the same name as the tag
   - Upload all executables as release assets

3. **Access your release**
   After the workflow completes, find your executables on the "Releases" page of the GitHub repository

#### Build Requirements

The GitHub Actions workflow installs all necessary dependencies, including:
- Python 3.12.8
- PyQt5 and related Qt libraries
- PyInstaller

All dependencies are specified in the `requirements.txt` file.

---

## 🔜 Future Enhancements

- 📝 **Project Notes** - Add and view notes for each project
- 🏷️ **Custom Tags** - Organize projects with custom categories
- 📊 **Project Statistics** - Track which projects you use most frequently
- ⚡ **Quick Commands** - Execute common VSCode commands directly from the toolbox

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

## 📄 License

[Your license information here]