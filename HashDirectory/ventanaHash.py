import sys
from PyQt5 import QtWidgets as QtW
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

from HashDirectory.Hash import TransfClaves

class HashView(QtW.QGroupBox):

    def __init__(self, p: QWidget):
        super().__init__(p)

        self.hash = None

        self.setStyleSheet("background-color:#DECCA6")

        self.tabla = QtW.QTableWidget(self)
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Clave", "Valor"])
        self.tabla.setGeometry(995, 20, 300, 820)
        self.tabla.horizontalScrollBar().setVisible(False)
        self.tabla.setColumnWidth(0, 145)
        self.tabla.setFont(QFont("Arial", 12, QFont.Bold))
        self.tabla.setColumnWidth(1, 145)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setStyleSheet("QTableWidget{border:1px solid black; background-color:#EBE6D2}")

        # seccion de entradas
        label = QtW.QLabel("Metodo hash", self)
        label.move(10, 10)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        self.opcionMetodoHash = QtW.QComboBox(self)
        self.opcionMetodoHash.addItems(["Mod", "Cuadratico", "Plegamiento", "Truncamiento"])
        self.opcionMetodoHash.move(10, 40)
        self.opcionMetodoHash.resize(150, 30)
        self.opcionMetodoHash.setFont(QFont("Arial", 12, QFont.Bold))
        self.opcionMetodoHash.setStyleSheet("background-color:#EBE6D2")

        label = QtW.QLabel("Metodo Solucion de Colisiones", self)
        label.move(190, 10)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        self.opcionSolColision = QtW.QComboBox(self)
        self.opcionSolColision.addItems(["Lineal", "Cuadratico", "Doble Hash"])
        self.opcionSolColision.move(190, 40)
        self.opcionSolColision.resize(150, 30)
        self.opcionSolColision.setFont(QFont("Arial", 12, QFont.Bold))
        self.opcionSolColision.setStyleSheet("background-color:#EBE6D2")

        label = QtW.QLabel("Tamaño Estructura", self)
        label.move(480, 10)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        self.tamanoEstructura = QtW.QTextEdit(self)
        self.tamanoEstructura.setFrameStyle(1)
        self.tamanoEstructura.move(480, 40)
        self.tamanoEstructura.resize(140, 30)
        self.tamanoEstructura.setFont(QFont("Arial", 12))
        self.tamanoEstructura.setStyleSheet("background-color:#EBE6D2")

        label = QtW.QLabel("Ingresar Registro (Solo se admiten registro numericos)", self)
        label.move(10, 100)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        self.ingresoDato = QtW.QTextEdit(self)
        self.ingresoDato.setFrameStyle(1)
        self.ingresoDato.move(10, 140)
        self.ingresoDato.resize(200, 30)
        self.ingresoDato.setFont(QFont("Arial", 12))
        self.ingresoDato.setStyleSheet("background-color:#EBE6D2")

        self.labelWarning = QtW.QLabel("Error: ", self)
        self.labelWarning.move(10, 300)
        self.labelWarning.setFont(QFont("Arial", 14, QFont.Bold))
        self.labelWarning.resize(750, 30)
        self.labelWarning.setStyleSheet("color:red")

        self.labelSuccess = QtW.QLabel("Success: ", self)
        self.labelSuccess.move(10, 330)
        self.labelSuccess.setFont(QFont("Arial", 14, QFont.Bold))
        self.labelSuccess.resize(750, 30)
        self.labelSuccess.setStyleSheet("color:green")

        self.registroProcess = QtW.QTextEdit(self)
        self.registroProcess.setFrameStyle(1)
        self.registroProcess.move(10, 370)
        self.registroProcess.resize(960, 465)
        self.registroProcess.setReadOnly(True)
        self.registroProcess.setFont(QFont("Arial", 12))
        self.registroProcess.setStyleSheet("QTextEdit{border:1px solid black; background-color:#D0C0A7}")

        self.bnEstructura = QtW.QPushButton("Crear Estructura", self)
        self.bnEstructura.setGeometry(720, 40, 170, 30)
        self.bnEstructura.setStyleSheet("QPushButton{background-color:#b0c9bb; border:1px solid black;}"
                                        "QPushButton::hover{background-color :#8fa89a;}"
                                        "QPushButton::pressed{background-color:#6e8679; }")
        self.bnEstructura.setFont(QFont("Arial", 12))
        self.bnEstructura.clicked.connect(self.testEstructure)

        self.bnIngresar = QtW.QPushButton("Agregar", self)
        self.bnIngresar.setGeometry(220, 140, 170, 30)
        self.bnIngresar.setStyleSheet("QPushButton{background-color:#b0c9bb; border:1px solid black;}"
                                        "QPushButton::hover{background-color :#8fa89a;}"
                                        "QPushButton::pressed{background-color:#6e8679; }")
        self.bnIngresar.setFont(QFont("Arial", 12))
        self.bnIngresar.clicked.connect(self.ingresarDato)

        self.bnReiniciar = QtW.QPushButton("Reiniciar", self)
        self.bnReiniciar.setGeometry(570, 140, 170, 30)
        self.bnReiniciar.setStyleSheet("QPushButton{background-color:#D7A184; border:1px solid black;}"
                                   "QPushButton::hover{background-color :#D4C2AD;}"
                                   "QPushButton::pressed{background-color:#EFDFCC; }")
        self.bnReiniciar.setFont(QFont("Arial", 12))
        self.bnReiniciar.clicked.connect(self.reiniciar)
        self.bnReiniciar.setEnabled(False)

    def testEstructure(self):
        t = 0
        try:
            if(self.tamanoEstructura.toPlainText() != ''):
                t = int(self.tamanoEstructura.toPlainText())
            if(t <= 0):
                self.errWarning("Por Favor el tamaño debe ser mayor a 0")
                return
        except:
            self.errWarning("Ingresó para tamaño letras o caracteres, ingrese valores numericos")
            return

        self.hash = TransfClaves(self.opcionMetodoHash.currentText(), t, self.opcionSolColision.currentText())
        self.processSuccess("Estructura definida")
        self.errWarning("")
        self.crearTabla()
        self.bnEstructura.setEnabled(False)
        self.opcionMetodoHash.setEnabled(False)
        self.opcionSolColision.setEnabled(False)
        self.tamanoEstructura.setEnabled(False)
        self.bnReiniciar.setEnabled(True)

    def ingresarDato(self):
        d = 0
        if self.hash is None:
            self.errWarning("Estructura no definida")
            return
        try:
            if(self.ingresoDato.toPlainText() != ''):
                d = int(self.ingresoDato.toPlainText())
            if(d <= 0):
                self.errWarning("Por Favor ingrese un Registro numerico mayor a 0")
                return
        except:
            self.errWarning("Ingresó por Registro, caracteres o letras, ingrese registros numericos")
            return

        self.hash.ingresarValor(d)
        self.processSuccess("Dato Ingresado (" + str(d) + ")")
        self.errWarning("")
        self.cargarDatos()
        self.registrarProceso()
    def errWarning(self, mensaje):
        self.labelWarning.setText("Error: " + mensaje)

    def processSuccess(self, mensaje):
        self.labelSuccess.setText("Success: " + mensaje)

    def reiniciar(self):
        self.hash = None
        self.tabla.setRowCount(0)
        self.bnEstructura.setEnabled(True)
        self.opcionMetodoHash.setEnabled(True)
        self.opcionSolColision.setEnabled(True)
        self.tamanoEstructura.setEnabled(True)
        self.bnReiniciar.setEnabled(False)
        self.registroProcess.setText("")
        self.labelSuccess.setText("Success:")

    def crearTabla(self):
        for i in range(0, self.hash.tamaño):
            self.tabla.insertRow(i)
            self.tabla.setItem(i, 0, QtW.QTableWidgetItem(str(i + 1)))

    def cargarDatos(self):
        for i in self.hash.estructura:
            self.tabla.setItem(i - 1, 1, QtW.QTableWidgetItem(str(self.hash.estructura[i])))

    def registrarProceso(self):
        if self.hash.mError != "":
            self.registroProcess.setText(self.registroProcess.toPlainText() + "\n> " + self.hash.mError)
        if self.hash.mIngreso != "":
            self.registroProcess.setText(self.registroProcess.toPlainText() + "\n> " + self.hash.mIngreso)
        if self.hash.mColision != "":
            self.registroProcess.setText(self.registroProcess.toPlainText() + "\n> " + self.hash.mColision)
        if self.hash.mSolColision != "":
            self.registroProcess.setText(self.registroProcess.toPlainText() + "\n> " + self.hash.mSolColision)