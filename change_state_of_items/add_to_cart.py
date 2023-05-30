import sys
from neo4j import GraphDatabase
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton ,QVBoxLayout, QLabel


class LOGGING:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def check_log_data_result(self):
        with self.driver.session() as session:
            sucess=session.run("")
            result = (sucess.single())
            return result


class MainWindow(QDialog):
    connect = LOGGING("neo4j+s://6d5091ae.databases.neo4j.io:7687", 'neo4j',
                      'zBLSkWWE91Z9mo_3CqQQi8RW-AM9NbMltXocxlvx8VE')

    def __init__(self, parent = None):
        super(MainWindow,self).__init__(parent)
        self.setWindowTitle("zakupy")
        self.Label1 = QLabel("zakupy")


def window_function():
    app = QApplication.instance()
    if app is None:
        print("instancja nie istnieje")
        app = QApplication(sys.argv)
        body = MainWindow()
        body.show()
        app.exec()
    else:
        print("instancja istnieje")
        app.quit()
        app.exit()
        app.deleteLater()
    # reszta kodu
    app = QApplication(sys.argv)
    body = MainWindow()
    body.show()
    app.exec()