import sys

from neo4j import GraphDatabase
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from change_state_of_items import add_to_cart

class LOGGING:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_products(self, category):
        var = category.text()
        print(type(var), var)
        data = []
        with self.driver.session() as session:
            for i in range(3):
                result = session.run("MATCH (n:Produkt)-[:kategoria]->(y:Rodzaj_Produktu) where y.name = $var and n.produkt_ref_key = $iterator RETURN n", var=var,iterator= i+1)
                record = result.single()
                if record != None:
                    node = record["n"]
                    product = node["name"]
                    price = node["cena"]
                    model = node["model"]
                    quantity = node["ilosc"]
                    data.append([product,price,model,quantity])
            print(data)
            return data


class Window(QDialog):
    def __init__(self, item, parent=None):
        super(Window, self).__init__(parent)
        print("przekazana kategoria", item.text())
        self.setWindowTitle("produkty")
        self.Label1 = QLabel("produkty")
        layout = QVBoxLayout(self)
        layout.addWidget(self.Label1)
        self.connect = LOGGING("neo4j+s://6d5091ae.databases.neo4j.io:7687", 'neo4j',
                               'zBLSkWWE91Z9mo_3CqQQi8RW-AM9NbMltXocxlvx8VE')
        data = self.connect.get_products(item)
        table = QTableWidget()
        self.button = QPushButton("HOME_PAGE")
        self.button.clicked.connect(self.go_home)
        self.button2 = QPushButton("back")
        self.button2.clicked.connect(self.go_back)
        table.setColumnCount(4)
        table.setRowCount(len(data))
        table.setHorizontalHeaderLabels(["Produkt","Price","Model","Quanity"])
        for i, produkty in enumerate(data):
            item = QTableWidgetItem(produkty[0])
            price = QTableWidgetItem(str(produkty[1]))
            model = QTableWidgetItem(produkty[2])
            quanity = QTableWidgetItem(str(produkty[3]))
            table.setItem(i, 0, item)
            table.setItem(i, 1, price)
            table.setItem(i, 2, model)
            table.setItem(i, 3, quanity)
        table.show()
        layout.addWidget(table)
        layout.addWidget(self.button2)
        layout.addWidget(self.button)
    def go_home(self):
        print("nacisnieto1")
        self.connect.close()
        self.deleteLater()
        self.close()

    def go_back(self):
        print("nacisnieto2")
        self.connect.close()
        self.deleteLater()
        self.close()
        add_to_cart.category_function()

def product_window(item):
    app = QApplication.instance()
    if app is None:
        print("Instance does not exist")
        app = QApplication(sys.argv)
    else:
        print("Instance exists")
    body = Window(item)
    body.exec_()
