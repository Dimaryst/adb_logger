import sys, platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import Qt, QProcess, QTextCodec
from PyQt5.QtGui import QTextCursor


class LogCollector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADB Unity Log Collector")
        self.setGeometry(100, 100, 800, 400)
        self.adb_bin = "bin/adb"
        if platform.system() == "Windows":
            self.adb_bin = "bin/adb.exe"
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.setCentralWidget(self.text_edit)

        self.adb_process = None

        self.start_logging()

    def start_logging(self):
        self.adb_process = QProcess()
        self.adb_process.readyReadStandardOutput.connect(self.handle_output)
        self.adb_process.finished.connect(self.restart_logging)
        self.adb_process.setProcessChannelMode(QProcess.MergedChannels)

        self.start_logcat()

    def start_logcat(self):
        self.adb_process.start(self.adb_bin, ["logcat", "-s", "Unity"])

    def restart_logging(self):
        # Перезапуск сбора логов после завершения предыдущего процесса
        self.start_logcat()

    def handle_output(self):
        output = self.adb_process.readAllStandardOutput()
        output = QTextCodec.codecForLocale().toUnicode(output)

        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.insertPlainText(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LogCollector()
    window.show()

    sys.exit(app.exec_())