import sys
from neo4j import GraphDatabase
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton ,QVBoxLayout, QLabel


class LOGGING:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def check_log_data_result(self, login, password):
        with self.driver.session() as session:
            sucess=session.run("Match (n:LogData) Where n.username = $username and n.password = $password return n",username=login,password=password)
            print(sucess.single())




class Form(QDialog):

    connect = LOGGING("neo4j+s://6d5091ae.databases.neo4j.io:7687",'neo4j','zBLSkWWE91Z9mo_3CqQQi8RW-AM9NbMltXocxlvx8VE')

    def __init__(self, parent = None, login = None, password = None, button = None, label1= None, label2 = None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("LOGIN")
        self.label1 = QLabel("login")
        self.login = QLineEdit("")
        self.label2 = QLabel("password")
        self.password = QLineEdit("")
        self.button = QPushButton("Enter")
        layout = QVBoxLayout(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.login)
        layout.addWidget(self.label2)
        layout.addWidget(self.password)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.button_pressed)

    def button_pressed(self):
        print("login atemppted")
        print(f"login:{self.login.text()}")
        print(f"password:{self.password.text()}")
        self.connect.check_log_data_result(self.login.text(),self.password.text())



def appconfig():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())

