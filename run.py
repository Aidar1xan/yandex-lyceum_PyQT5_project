import sys
from main import MyWidget
from PyQt5.QtWidgets import QApplication

print("ccr")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.exit(app.exec())

