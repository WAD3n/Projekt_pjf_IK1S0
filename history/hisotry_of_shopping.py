import sys
from neo4j import GraphDatabase
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton ,QVBoxLayout, QLabel
from PySide6.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem)
from items_in_category import products


class LOGGING:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_data(self):
        data = []
        with self.driver.session() as session:
            count = session.run("match p=(n:Produkt_Kupiony)<-[z:in_history]-(k:Historia_zakupow)<-[:bought]-(h:LogData) where (h)-[:zalagowany]->(h) return n,count(z) as ile")
            for element in count:
                node = element["n"]
                product = node["name"]
                price = node["cena"]
                model = node["model"]
                data.append([product,price,model,element["ile"]])
            print("historia zakupow:",data)
            return data



class HistoryWindow(QDialog):

    connect = LOGGING("neo4j+s://6d5091ae.databases.neo4j.io:7687", 'neo4j',
                      'zBLSkWWE91Z9mo_3CqQQi8RW-AM9NbMltXocxlvx8VE')
    data = []

    def __init__(self,parent = None):
        super(HistoryWindow,self).__init__(parent)
        self.setWindowTitle("Historia")
        layout = QVBoxLayout(self)
        self.data = self.connect.get_data()
        table = QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(len(self.data))
        table.setHorizontalHeaderLabels(["Produkt","Price","Model","Quanity"])
        for i  in range(len(self.data)):
            for j in enumerate(self.data[i]):
                item = QTableWidgetItem(self.data[i][0])
                price = QTableWidgetItem(str(self.data[i][1]))
                model = QTableWidgetItem(self.data[i][2])
                quanity = QTableWidgetItem(str(self.data[i][3]))
                table.setItem(i, 0, item)
                table.setItem(i, 1, price)
                table.setItem(i, 2, model)
                table.setItem(i, 3, quanity)

        self.button = QPushButton("Back")
        self.button.show()
        self.button.clicked.connect(self.button_pressed)
        layout.addWidget(table)
        layout.addWidget(self.button)

    def button_pressed(self):
        print("back button pressed")
        self.connect.close()
        self.close()

def hisotry_function():
    app = QApplication.instance()
    if app is None:
        print("instancja nie istnieje")
        app = QApplication(sys.argv)
        body = HistoryWindow()
        body.show()
        app.exec()
    else:
        print("instancja istnieje")
        body = HistoryWindow()
        body.exec_()
