import sys
from neo4j import GraphDatabase
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton ,QVBoxLayout, QLabel
from PySide6.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem)

class LOGGING:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_items_category(self):
        data = []
        with self.driver.session() as session:
            # zwiekszyc zasieg by zgadzal sie z liczba kategorii
            for i in range(2):
                sucess=session.run("Match (n:Rodzaj_Produktu) where n.ref_code = $iterator return n",iterator = i+1)
                result = (sucess.single())
                node = result["n"]
                type = node["name"]
                data.append(type)
        return data



class MainWindow(QDialog):
    connect = LOGGING("neo4j+s://6d5091ae.databases.neo4j.io:7687", 'neo4j',
                      'zBLSkWWE91Z9mo_3CqQQi8RW-AM9NbMltXocxlvx8VE')

    def __init__(self, parent = None):
        super(MainWindow,self).__init__(parent)
        self.setWindowTitle("zakupy")
        self.Label1 = QLabel("zakupy")
        layout = QVBoxLayout(self)
        layout.addWidget(self.Label1)
        data = self.connect.get_items_category()
        table = QTableWidget()
        table.setColumnCount(1)
        table.setRowCount(len(data))
        table.setHorizontalHeaderLabels(["Kategoria"])
        self.button = QPushButton("HOME_PAGE")
        self.button.clicked.connect(self.go_home)
        for i , kategoria in enumerate(data):
            item = QTableWidgetItem(kategoria)
            table.setItem(i, 0, item)
        table.show()
        layout.addWidget(table)
        layout.addWidget(self.button)
        print(data)

    def go_home(self):
        print("nacisnieto")
        self.connect.close()
        self.deleteLater()
        self.close()

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
        app = QApplication(sys.argv)
        body = MainWindow()
        body.show()
        app.exec()
