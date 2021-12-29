import random

from PySide2 import QtWidgets, QtCore
from PingMonitor_design_back import Ui_Form as Ui_Form_Ping
from PingMonitorSettings_design_back import Ui_Form as Ui_Form_Setting
from Tracert_design_back import Ui_Form as Ui_Form_Tracert

import pythonping as pg

class MyWidgetsMain(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWidgetsMain, self).__init__(parent)
        self.ui = Ui_Form_Ping()
        self.ui.setupUi(self)

        self.setting = MyWidgetsSetting()
        self.tracert = MyWidgetsTracert()

        self.ui.pushButton_4.clicked.connect(self.open_settings)
        self.ui.pushButton_3.clicked.connect(self.open_tracert)

        self.ui.pushButton.clicked.connect(self.start)

        self.setting.signal.connect(self.show_list)

        self.start_add_ip = MyThread()
        self.start_add_ip.signal.connect(lambda x: print(x))

    def show_list(self, data):
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(0)
        for i in range(len(data)):
            self.ui.tableWidget.insertRow(i)
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(data[i])))

    def open_settings(self):
        self.setting.show()

    def open_tracert(self):
        self.tracert.show()

    def start(self):
        self.start_add_ip.set_ip(self.return_list())
        self.start_add_ip.start()
        # self.start_add_ip.ip_list(self)

    def return_list(self):
        list_ip = []
        for i in range(self.ui.tableWidget.rowCount()):
            row_ip = self.ui.tableWidget.item(i, 0).text()
            list_ip.append(row_ip)
        return list_ip


class MyThread(QtCore.QThread):
    signal = QtCore.Signal(str)

    def set_ip(self, data):
        self.ip_list = data

    def run(self) -> None:
        while True:
            for i in self.ip_list:
                status = random.choice(["Доступен", "Недоступен"])
                self.sleep(1)
                self.signal.emit(f"IP {i} - {status}")


class MyWidgetsSetting(QtWidgets.QWidget):
    signal = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(MyWidgetsSetting, self).__init__(parent)
        self.ui = Ui_Form_Setting()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.add_ip)
        self.ui.pushButton_2.clicked.connect(self.del_ip)

    def add_ip(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Введите IP", "Какой IP хотите ввести?")
        check = self.check_valid(text)

        if check:
            self.ui.listWidget.addItem(text)
            self.signal.emit(self.return_list())

    def del_ip(self):
        listItems = self.ui.listWidget.selectedItems()
        if not listItems:
            return

        for item in listItems:
            self.ui.listWidget.takeItem(self.ui.listWidget.row(item))

    def check_valid(self, text):
        list_text = text.split(".")
        errorMsg = QtWidgets.QErrorMessage(self)

        if len(list_text) != 4:
            errorMsg.showMessage(str("IP введен неверно, введите заново"))
            return False

        for simbol in list_text:
            if not isinstance(int(simbol), int):
                errorMsg.showMessage(str("IP введен неверно, введите заново"))
                return False

            if int(simbol) < 0 or int(simbol) > 255:
                errorMsg.showMessage(str("IP введен неверно, введите заново"))
                return False

        return True

    def return_list(self):
        list_ip = []
        for i in range(self.ui.listWidget.count()):
            row_ip = self.ui.listWidget.item(i).text()
            list_ip.append(row_ip)
        return list_ip


class MyWidgetsTracert(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWidgetsTracert, self).__init__(parent)
        self.ui = Ui_Form_Tracert()
        self.ui.setupUi(self)



if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = MyWidgetsMain()
    window.show()

    app.exec_()
