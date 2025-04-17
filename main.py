import sys
from PyQt5.QtWidgets import QApplication
from toolbox import ToolboxApp

def main():
    app = QApplication(sys.argv)
    window = ToolboxApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
