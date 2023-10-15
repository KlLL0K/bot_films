import sys


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit


class WordTrick(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 100, 300, 100)
        self.setWindowTitle('WordTrick')
        self.trick_button = QPushButton('->', self)
        self.trick_button.resize(40, 30)
        self.trick_button.move(130, 30)
        self.trick_button.clicked.connect(self.hello)
        self.first_value = QLineEdit(self)
        self.first_value.resize(100, 40)
        self.first_value.move(18, 25)

        self.second_value = QLineEdit(self)
        self.second_value.resize(100, 40)
        self.second_value.move(180, 25)

    def hello(self):
        if self.trick_button.text() == '->':
            self.trick_button.setText('<-')
            self.second_value.setText(self.first_value.text())
            self.first_value.setText('')
        else:
            self.trick_button.setText('->')
            self.first_value.setText(self.second_value.text())
            self.second_value.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WordTrick()
    ex.show()
    sys.exit(app.exec())