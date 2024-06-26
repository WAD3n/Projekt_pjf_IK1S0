from PyQt6 import QtCore, QtGui, QtWidgets, uic
from neo4j import GraphDatabase
from PyQt6.QtWidgets import QLabel, QPushButton, QListWidget, QListWidgetItem
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QApplication

class LOGGING:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_choice(self):
        with self.driver.session() as session:
            result = session.run("Match (n:SELECTION) return n")
            record = result.single()
            node = record["n"]
            choice = node["choice"]
            session.run("Match (n:SELECTION) delete n")
            return choice



from logging_screen import logging
from home_screen import home
from change_state_of_items import add_to_cart
from show_cart import showcart
from history import hisotry_of_shopping

if __name__ == "__main__":
    connect = LOGGING("neo4j+s://6d5091ae.databases.neo4j.io:7687", 'neo4j',
                      'zBLSkWWE91Z9mo_3CqQQi8RW-AM9NbMltXocxlvx8VE')
    logging.logconfig()
    app = QApplication.instance()
    app.quit()
    app.exit()
    print("main is running")
    while(1):
        value = home.function()
        wybor = LOGGING.get_choice(self=connect)
        print("choice:",wybor)
        if wybor == 1:
            add_to_cart.category_function()
        elif wybor == 2:
            showcart.cart_window()
        elif wybor ==3:
            hisotry_of_shopping.hisotry_function()
        elif wybor == 4:
            connect.close()
            print("exit")
            exit()