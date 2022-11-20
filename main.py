from frontend.mainwindow import Ui_MainWindow
from frontend.secondWindow import Ui_Form
from frontend.db_window import Ui_db
from backend.OpenWeatherMap_API import get_weather_data
from backend.create_db import create_database
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.conn = create_database()
        self.cursor = self.conn.cursor()
        self.setupUi(self)

        self.pushButton_start.clicked.connect(self.go_to_second)
        self.exit_pushButton.clicked.connect(self.exit)
        self.search_in_database_pushButton.clicked.connect(self.go_to_search_in_db)

    def go_to_second(self):
        self.close()
        self.nw = NewWidget()
        self.nw.show()

    def exit(self):
        self.close()

    def go_to_search_in_db(self):
        self.close()
        self.nw = db_widget()
        self.nw.show()


class NewWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super(NewWidget, self).__init__()
        self.setupUi(self)
        self.send_push_button.clicked.connect(self.send_text)
        self.push_button_go_back.clicked.connect(self.go_back)
        self.cursor = create_database().cursor()

    def send_text(self):
        text = self.place_to_send_cityName.text()
        try:
            self.listWidget.clear()
            result = get_weather_data(text)
            self.cursor.execute(
                'INSERT OR REPLACE INTO users_meteo_data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', result)

            self.listWidget.addItems([QListWidgetItem(str(i), self.listWidget) for i in result])
        except Exception as error:
            self.statusBar().showMessage(f'{error}')

    def go_back(self):
        self.close()
        self.main_widget = MyWidget()
        self.main_widget.show()


class db_widget(Ui_db, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cursor = create_database().cursor()
        self.searchPushButton.clicked.connect(self.update_result)
        self.Button_to_go_back.clicked.connect(self.back)

    def update_result(self):
        # Получили результат запроса, который ввели в текстовое поле
        try:
            result = self.cursor.execute("SELECT * FROM users_meteo_data").fetchall()
        except Exception as error:
            self.statusBar().showMessage(f'{error}')
        for i in result:
            self.place_to_print_data.setText(str(i))

    def back(self):
        self.close()
        self.nw = MyWidget()
        self.nw.show()
