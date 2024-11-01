import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QHBoxLayout, QLabel, QAction

from qfluentwidgets import StyleSheetBase, Enum, Action, SystemTrayMenu, MessageBox, setTheme, Theme, qconfig
from android_helper import get_emulator_path, get_available_emulators, launch_emulator

class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """
    WINDOW = "window"
    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f"qss/{theme.value.lower()}/{self.value}.qss"

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())
        self.setToolTip('LaunchLab')

        self.menu = SystemTrayMenu(parent=parent)
        default_actions = [
            Action('Help'),
            Action('About')
        ]

        emulator_path = get_emulator_path()
        if emulator_path:
            emulators = get_available_emulators(emulator_path)
            for emulator in emulators:
                action = QAction(emulator, self)
                action.triggered.connect(lambda checked, em=emulator: launch_emulator(emulator, emulator_path))
                self.menu.addAction(action)

            self.menu.addActions(default_actions)
        else:
            self.menu.addAction(Action('No emulator found'))
            self.menu.addActions(default_actions)

        self.setContextMenu(self.menu)

    def ikun(self):
        content = """巅峰产生虚伪的拥护，黄昏见证真正的使徒 🏀

                         ⠀⠰⢷⢿⠄
                   ⠀⠀⠀⠀⠀⣼⣷⣄
                   ⠀⠀⣤⣿⣇⣿⣿⣧⣿⡄
                   ⢴⠾⠋⠀⠀⠻⣿⣷⣿⣿⡀
                   ⠀⢀⣿⣿⡿⢿⠈⣿
                   ⠀⠀⠀⢠⣿⡿⠁⠀⡊⠀⠙
                   ⠀⠀⠀⢿⣿⠀⠀⠹⣿
                   ⠀⠀⠀⠀⠹⣷⡀⠀⣿⡄
                   ⠀⠀⠀⠀⣀⣼⣿⠀⢈⣧
        """
        w = MessageBox(
            title='坤家军！集合！',
            content=content,
            parent=self.parent()
        )
        w.yesButton.setText('献出心脏')
        w.cancelButton.setText('你干嘛~')
        w.exec()

class App(QWidget):
    def __init__(self):
        super().__init__()
        StyleSheet.WINDOW.apply(self)

        self.setWindowTitle('LaunchLab')
        self.resize(300, 600)

        self.setLayout(QHBoxLayout())

        self.label = QLabel('Right-click system tray icon', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.label)

        self.setStyleSheet('Demo{background: white} QLabel{font-size: 20px}')
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'LaunchLab.png')
        self.setWindowIcon(QIcon(icon_path))

        self.systemTrayIcon = SystemTrayIcon(self)
        self.systemTrayIcon.show()

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    QTApp = QApplication(sys.argv)
    app = App()
    QTApp.exec_()