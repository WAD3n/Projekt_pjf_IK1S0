import sys

from neo4j import GraphDatabase
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

import show_cart.showcart


class LOGGING:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_cart_info(self):
        data = []
        with self.driver.session() as session:
            count = session.run("match p=(n:Produkt)-[z:in_cart]->(k:Koszyk)<-[:shopping_cart]-(h:LogData) where (h)-[:zalagowany]->(h) return n,count(z) as ile")

            for element in count:
                node = element["n"]
                product = node["name"]
                price = node["cena"]
                model = node["model"]
                data.append([product,price,model,element["ile"]])
            print("data:",data)
            return data

    def remove(self, index):
        data = []
        with self.driver.session() as session:
            count=session.run("match p=(n:Produkt)-[z:in_cart]->(k:Koszyk)<-[:shopping_cart]-(h:LogData) where (h)-[:zalagowany]->(h) return n,count(z) as ile")
            for element in count:
                node = element["n"]
                product = node["name"]
                price = node["cena"]
                model = node["model"]
                data.append([product, price, model])
            session.run("match p=(n:Produkt)-[r:in_cart]->(k:Koszyk)<-[:shopping_cart]-(u:LogData) where n.name = $var1 and n.model = $var2 and (u)-[:zalagowany]->(u)  with r limit 1 delete r ",var1=data[index][0] , var2= data[index][2])
            print("usunieto",data[index][0],data[index][2])

    def remove_whole_cart(self):
         with self.driver.session() as session:
            session.run("match p=(n:Produkt)-[r:in_cart]->(k:Koszyk)<-[:shopping_cart]-(u:LogData) where  (u)-[:zalagowany]->(u)   delete r ")
         print("usunieto koszyk")

    def bought_items(self):
        data = []
        with self.driver.session() as session:
            count=session.run("match p=(n:Produkt)-[z:in_cart]->(k:Koszyk)<-[:shopping_cart]-(h:LogData) where (h)-[:zalagowany]->(h) return n,count(z) as ile")
            for element in count:
                node = element["n"]
                product = node["name"]
                price = node["cena"]
                model = node["model"]
                quanity = node["ilosc"]
                data.append([product, price, model,quanity,element["ile"]])
        print(" koszyk data :", data)
        for i in range(len(data)):
            if data[i][3] < data[i][4]:
                print("za duzo produtku nr :",i)
                return
        print("zakupiono przedmioty")
        with self.driver.session() as session2:
            for i in range(len(data)):
                print("iterator :", i)
                session2.run("match (n:Produkt) where n.name = $var1 and n.model = $var2 set n.ilosc = n.ilosc - $var3",var1= data[i][0], var2=data[i][2], var3=data[i][4])
                session2.run("match (n:LogData)-[:zalagowany]->(n)-[:bought]->(h:Historia_zakupow) create (z:Produkt_Kupiony {name: $var1 , model: $var2 , quanity: $var3 })<-[:in_history]-(h)", var1= data[i][0], var2=data[i][2], var3=data[i][4])
            self.remove_whole_cart()


class Window(QDialog):

    data = []
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.connect = LOGGING("neo4j+s://6d5091ae.databases.neo4j.io:7687", 'neo4j',
                               'zBLSkWWE91Z9mo_3CqQQi8RW-AM9NbMltXocxlvx8VE')
        self.setWindowTitle("CART")
        self.data= self.connect.get_cart_info()
        table = QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(len(self.data))
        table.setHorizontalHeaderLabels(["Produkt", "Price", "Model", "Quanity", "Remove"])
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
                table.setItem(i,4,QTableWidgetItem(f"REMOVE-{str(i)}"))
        layout = QVBoxLayout(self)
        button2 = QPushButton("Zatwierdz")
        button3 = QPushButton("usun koszyk")
        button = QPushButton("HOME")
        button.pressed.connect(self.button_pressed)
        button2.pressed.connect(self.button_zatwierdz_pressed)
        button3.pressed.connect(self.button_anuluj_pressed)
        table.itemClicked.connect(self.remove_product_from_cart)
        layout.addWidget(table)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button)
    def remove_product_from_cart(self, item):
        x=item.text()
        x= x.split('-')
        print("x = ",x)
        if x[0] != 'REMOVE':
            print("pressed:",item.text())
            pass
        else:
            print(f"pressed-{item.text()}")
            index = int(x[1])
            print("index",index)
            self.connect.remove(index)
            self.connect.close()
            self.close()
            show_cart.showcart.cart_window()

    def button_pressed(self):
        print("pressed button")
        self.connect.close()
        self.close()

    def button_anuluj_pressed(self):
        print("usun koszyk pressed")
        self.connect.remove_whole_cart()
        self.connect.close()
        self.close()
        show_cart.showcart.cart_window()

    def button_zatwierdz_pressed(self):
        print("zatwierdz pressed")
        self.connect.bought_items()
        self.connect.close()
        self.close()
        show_cart.showcart.cart_window()

def cart_window():
    app = QApplication.instance()
    if app is None:
        print("Instance does not exist 2")
        app = QApplication(sys.argv)
    else:
        print("Instance exists")
    body = Window()
    body.exec_()
