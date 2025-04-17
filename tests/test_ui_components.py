import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt5.QtWidgets import QApplication
from ui_components import ProjectListItem, ToolboxUI

@pytest.fixture(scope="session")
def app():
    """Ensure a QApplication exists for all tests."""
    import sys
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

def test_project_list_item_properties(app):
    folder_name = "TestProject"
    full_path = "/home/user/projects/TestProject"
    widget = ProjectListItem(folder_name, full_path)
    assert widget.name_label.text() == folder_name
    assert widget.path_label.text() == full_path
    assert widget.icon_label.pixmap() is not None

def test_toolbox_ui_add_project_item(app):
    from PyQt5.QtWidgets import QMainWindow
    main_window = QMainWindow()
    ui = ToolboxUI(main_window)
    folder_name = "Sample"
    full_path = "/some/very/long/path/to/Sample"
    item = ui.add_project_item(folder_name, full_path)
    # Check that the item is added to the list
    assert ui.project_list.count() == 1
    # Check that the widget is set and has correct data
    widget = ui.project_list.itemWidget(item)
    assert widget.name_label.text() == folder_name
    assert item.data(0x0100) == full_path  # Qt.UserRole

def test_toolbox_ui_shorten_path(app):
    from PyQt5.QtWidgets import QMainWindow
    ui = ToolboxUI(QMainWindow())
    # Use a path longer than 60 characters to trigger shortening
    long_path = "/very/long/path/with/many/segments/and/directories/that/exceeds/sixty/characters/for/testing/purposes"
    short = ui.shorten_path(long_path)
    assert "..." in short
    assert short.startswith("/.../")
    # The ending should be the last 3 segments joined by os.sep
    import os
    expected_end = os.sep.join(long_path.split(os.sep)[-3:])
    assert short.endswith(expected_end)

def test_toolbox_ui_filter_projects(app):
    from PyQt5.QtWidgets import QMainWindow
    ui = ToolboxUI(QMainWindow())
    ui.add_project_item("Alpha", "/projects/Alpha")
    ui.add_project_item("Beta", "/projects/Beta")
    ui.add_project_item("Gamma", "/projects/Gamma")
    # Filter for 'Beta'
    ui.filter_projects("Beta")
    visible = [not ui.project_list.item(i).isHidden() for i in range(ui.project_list.count())]
    assert visible == [False, True, False]
    # Filter for empty string (should show all)
    ui.filter_projects("")
    visible = [not ui.project_list.item(i).isHidden() for i in range(ui.project_list.count())]
    assert all(visible)