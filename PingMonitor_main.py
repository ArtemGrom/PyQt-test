from PySide2 import QtWidgets, QtCore
from PingMonitor_design_back import Ui_Form as Ui_Form_Ping
from PingMonitorSettings_design_back import Ui_Form as Ui_Form_Setting
from Tracert_design_back import Ui_Form as Ui_Form_Tracert


class MyWidgetsMain(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWidgetsMain, self).__init__(parent)
        self.ui = Ui_Form_Ping()
        self.ui.setupUi(self)

        self.setting = MyWidgetsSetting()
        self.tracert = MyWidgetsTracert()

        self.ui.pushButton_4.clicked.connect(self.open_settings)
        self.ui.pushButton_3.clicked.connect(self.open_tracert)

        self.ui.pushButton.clicked.connect(self.return_list)

        self.start_add_ip = MyThread()

    def open_settings(self):
        self.setting.show()

    def open_tracert(self):
        self.tracert.show()

    def start(self):
        self.return_list()
        # self.start_add_ip.ip_list(self)


    def return_list(self):
        list_ip = []
        for i in range(self.ui.tableWidget.rowCount()):
            row_ip = self.ui.tableWidget.item(i, 0).text()
            list_ip.append(row_ip)
        return list_ip

class MyThread(QtCore.QThread):
    signal = QtCore.Signal(int)

    def run(self) -> None:
        pass

    def ip_list(self, count: int):
        self.count = count


class MyWidgetsSetting(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWidgetsSetting, self).__init__(parent)
        self.ui = Ui_Form_Setting()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.add_ip)

    def add_ip(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Введите IP", "Какой IP хотите ввести?")
        if ok:
            self.ui.listWidget.addItem(text)


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
