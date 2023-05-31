from PyQt6 import QtCore, QtGui, QtWidgets, uic
from neo4j import GraphDatabase
from PyQt6.QtWidgets import QLabel, QPushButton, QListWidget, QListWidgetItem
from PySide6.QtCore import Slot, Signal

import main
from change_state_of_items import add_to_cart

class LOGGING:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node_choice(self, wybor):
        with self.driver.session() as session:
            sucess=session.run("CREATE (n:SELECTION {choice: $choice})", choice=wybor)

class MyWindow(QtWidgets.QMainWindow):


    connect = LOGGING("neo4j+s://6d5091ae.databases.neo4j.io:7687",'neo4j','zBLSkWWE91Z9mo_3CqQQi8RW-AM9NbMltXocxlvx8VE')
    def __init__(self):
        super().__init__()
        # Inicjalizacja interfejsu użytkownika z pliku .ui
        uic.loadUi("home.ui", self)
        self.pushButton_4.clicked.connect(self.button4_pressed)
        self.pushButton.clicked.connect(self.button_pressed)
        self.pushButton_2.clicked.connect(self.button2_pressed)
        self.pushButton_3.clicked.connect(self.button3_pressed)
    def button_pressed(self):
        self.connect.create_node_choice(1)
        self.connect.close()
        self.close()
    def button2_pressed(self):
        self.connect.create_node_choice(2)
        self.connect.close()
        self.close()

    def button3_pressed(self):
        self.connect.create_node_choice(3)
        self.connect.close()
        self.close()
    def button4_pressed(self):
        self.connect.create_node_choice(4)
        self.connect.close()
        self.close()
def function():
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec()