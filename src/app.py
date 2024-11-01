import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QHBoxLayout, QLabel

from qfluentwidgets import StyleSheetBase, Enum, Action, SystemTrayMenu, MessageBox, setTheme, Theme, qconfig


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
        self.menu.addActions([
            Action('🎤   唱'),
            Action('🕺   跳'),
            Action('🤘🏼   RAP'),
            Action('🎶   Music'),
            Action('🏀   篮球', triggered=self.ikun),
        ])
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
        self.setWindowIcon(QIcon('assets/LaunchLab.png'))

        self.systemTrayIcon = SystemTrayIcon(self)
        self.systemTrayIcon.show()



if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    QTApp = QApplication(sys.argv)
    app = App()
    app.show()
    QTApp.exec_()