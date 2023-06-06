import sys
from neo4j import GraphDatabase
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton ,QVBoxLayout, QLabel


class LOGGING:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def check_log_data_result(self, login, password):
        with self.driver.session() as session:
            sucess=session.run("Match (n:LogData) Where n.username = $username and n.password = $password return n",username=login,password=password)
            if sucess != None:
                session.run("Match (n:LogData) Where n.username = $username and n.password = $password create (n)-[:zalagowany]->(n)",username=login,password=password)
            result = (sucess.single())
            return result

    def create_acc(self,login,password):
        with self.driver.session() as session:
            session.run("create (n:LogData {username: $username,password: $password})",username=login,password=password)
            session.run("match (n:LogData) where n.username = $username create (n)-[:shopping_cart]->(:Koszyk)",username=login)
            session.run("match (n:LogData) where n.username = $username create (n)-[:user_info]->(:UserData)",username=login)
            session.run("match (n:LogData) where n.username = $username create (n)-[:bought]->(:Historia_zakupow)",username=login)
            print("ACCOUNT CREATED")



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
        self.button2 = QPushButton("CREATE ACCOUNT")
        layout = QVBoxLayout(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.login)
        layout.addWidget(self.label2)
        layout.addWidget(self.password)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        self.button.clicked.connect(self.button_pressed)
        self.button2.clicked.connect(self.button2_pressed)
    def button_pressed(self):
        print("login atemppted")
        print(f"login:{self.login.text()}")
        print(f"password:{self.password.text()}")
        result = self.connect.check_log_data_result(self.login.text(),self.password.text())
        if result == None:
            print("logowanie nieudane")
        else:
            print("logwanie powiodlo sie")
            print(result)
            self.connect.close()
            self.close()
    def button2_pressed(self):
        self.connect.create_acc(self.login.text(),self.password.text())

def logconfig():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec()
