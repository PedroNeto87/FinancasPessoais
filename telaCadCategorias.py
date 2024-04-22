from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from db import DataBase


class TelaCadCategorias:
    @staticmethod
    def mostrar_tela_cat_receita():
        tela_categoria_receita = QDialog()
        loadUi('ui_catReceita.ui', tela_categoria_receita)
        tela_categoria_receita.setWindowTitle('Cadastro')
        tela_categoria_receita.btn_inserir_cat_receita.clicked.connect(lambda: TelaCadCategorias.inserir_cat_receita(tela_categoria_receita))
        tela_categoria_receita.btn_cancelar_cat_receita.clicked.connect(lambda: TelaCadCategorias.fecharTela(tela_categoria_receita))
        tela_categoria_receita.exec_()

    @staticmethod
    def mostrar_tela_cat_despesa():
        tela_categoria_despesa = QDialog()
        loadUi('ui_catDespesa.ui', tela_categoria_despesa)
        tela_categoria_despesa.setWindowTitle('Cadastro')
        tela_categoria_despesa.btn_inserir_cat_despesa.clicked.connect(lambda: TelaCadCategorias.inserir_cat_despesa(tela_categoria_despesa))
        tela_categoria_despesa.btn_cancelar_cat_despesa.clicked.connect(lambda: TelaCadCategorias.fecharTela(tela_categoria_despesa))
        tela_categoria_despesa.exec_()

    @staticmethod
    def mostrar_tela_cat_invesitmento():
        tela_categoria_investimento = QDialog()
        loadUi('ui_catInvestimento.ui', tela_categoria_investimento)
        tela_categoria_investimento.setWindowTitle('Cadastro')
        tela_categoria_investimento.btn_inserir_cat_investimento.clicked.connect(lambda: TelaCadCategorias.inserir_cat_investimento(tela_categoria_investimento))
        tela_categoria_investimento.btn_cancelar_cat_investimento.clicked.connect(lambda: TelaCadCategorias.fecharTela(tela_categoria_investimento))
        tela_categoria_investimento.exec_()

    @staticmethod
    def inserir_cat_receita(tela_categoria_receita):
        descricao = tela_categoria_receita.txt_desc_cat_receita.text()

        db = DataBase()
        db.conectar()
        db.inserir_cat_receita(descricao)
        db.desconectar()

        msg = QMessageBox()
        msg.setWindowTitle('Cadastro de Categoria')
        msg.setText('Categoria cadastrada com sucesso')
        msg.exec()

        tela_categoria_receita.txt_desc_cat_receita.setText('')
        
    @staticmethod
    def inserir_cat_despesa(tela_categoria_despesa):
        descricao = tela_categoria_despesa.txt_desc_cat_despesa.text()

        db = DataBase()
        db.conectar()
        db.inserir_cat_despesa(descricao)
        db.desconectar()

        msg = QMessageBox()
        msg.setWindowTitle('Cadastro de Categoria')
        msg.setText('Categoria cadastrada com sucesso')
        msg.exec()

        tela_categoria_despesa.txt_desc_cat_despesa.setText('')

    @staticmethod
    def inserir_cat_investimento(tela_categoria_investimento):
        descricao = tela_categoria_investimento.txt_desc_cat_investimento.text()

        db = DataBase()
        db.conectar()
        db.inserir_cat_investimento(descricao)
        db.desconectar()

        msg = QMessageBox()
        msg.setWindowTitle('Cadastro de Categoria')
        msg.setText('Categoria cadastrada com sucesso')
        msg.exec()

        tela_categoria_investimento.txt_desc_cat_investimento.setText('')

    def fecharTela(self):
        self.reject()
