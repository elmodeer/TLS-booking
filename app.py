import re

import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QPushButton, QMessageBox, QLabel, QLineEdit, \
    QGridLayout

from tlsBook import TlsChecker
import validators


class TlsCheckerGui(QWidget):
    def __init__(self):
        super().__init__()

        self.checker = None

        # Initialize timer
        self.timer = QTimer()
        self.timer.setInterval(1000 * 60 * 5)  # ms * sec * minute = 5 minutes
        self.timer.timeout.connect(self.recurring_timer)

        # Initialize main components
        self.startBtn = QPushButton('Start Checking')
        self.quitBtn = QPushButton('Quit')
        self.emailEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.targetEmailEdit = QLineEdit()

        self.init_ui()

    def init_ui(self):
        email = QLabel('Your Email')
        password = QLabel('Your Password')
        target_email = QLabel('Recipient Email(s)')

        self.startBtn.clicked.connect(self.start_checking)
        self.quitBtn.clicked.connect(QApplication.instance().quit)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(email, 1, 0)
        grid.addWidget(self.emailEdit, 1, 1, 1, 9)
        grid.addWidget(QLabel('Please the email you used to register your TLS application.'), 2, 1)

        grid.addWidget(password, 3, 0)
        grid.addWidget(self.passwordEdit, 3, 1, 1, 9)
        grid.addWidget(QLabel('Please the password your used to register your TLS application (we do not record your password).'), 4, 1)

        grid.addWidget(target_email, 5, 0)
        grid.addWidget(self.targetEmailEdit, 5, 1, 1, 9)
        grid.addWidget(QLabel('Please list of emails that will receive the notification. Separate the emails with a \',\' character.'), 6,
                       1)

        grid.setRowStretch(7, 4)

        grid.addWidget(self.startBtn, 9, 6)
        grid.addWidget(self.quitBtn, 9, 8)

        self.setLayout(grid)

        self.resize(640, 480)
        self.center()
        self.setWindowTitle('TLS Checker')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def check_inputs(self):
        email = self.emailEdit.text()
        password = self.passwordEdit.text()
        target_email = self.targetEmailEdit.text()

        email_check = validators.concat_emails(email, target_email)

        if not validators.validate_emails(email_check) or not target_email:
            msg = QMessageBox()
            msg.setText("Please enter a valid email")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return False

        if not validators.validate_required(password):
            msg = QMessageBox()
            msg.setText("Password field is required!")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return False

        return True

    def start_checking(self):
        if not self.check_inputs():
            self.timer.stop()
            return

        # Timer has already started, then time to stop it!
        if self.timer.isActive():
            self.startBtn.setText('Start Checking')
            self.timer.stop()
            return

        # Checker itself hasn't been instantiated yet, we need proper emails and password before starting
        if not self.checker:
            self.checker = TlsChecker(self.emailEdit.text(), self.passwordEdit.text(), self.targetEmailEdit.text())

        self.startBtn.setText('Stop Checking')
        self.timer.start()

    def recurring_timer(self):
        self.checker.check()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TlsCheckerGui()
    sys.exit(app.exec_())
