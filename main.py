import sqlite3
import pandas as pd
import os
import sys
import locale
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QMessageBox, QTableWidgetItem)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from ui_main import Ui_MainWindow
from db import DataBase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from collections import defaultdict
from datetime import datetime


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)
        self.setWindowTitle('Orçamento Pessoal')
        
        appIcon = QIcon('imgs/logo.png')
        self.setWindowIcon(appIcon)
        
        self.atualizar_funcoes()
        self.valores_sistema()
        
        
        # Páginas do sistema
        self.btn_dashboard.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_dashboard))
        self.btn_transacoes.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_transacoes))
        self.btn_receita.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_novo_receita))
        self.btn_despesa.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_novo_despesa))
        self.btn_investimento.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_novo_investimento))
        # Botão cancelar lançamento de receita/despesa/investimento
        self.btn_cancelar_receita.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_transacoes))
        self.btn_cancelar_despesa.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_transacoes))
        self.btn_cancelar_investimento.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_transacoes))
        # Botão cadastrar categoria de receita/despesa/investimento
        self.btn_add_cat_receita.clicked.connect(self.mostrar_tela_cat_receita)
        self.btn_add_cat_despesa.clicked.connect(self.mostrar_tela_cat_despesa)
        self.btn_add_cat_investimento.clicked.connect(self.mostrar_tela_cat_invesitmento)
        # Botão cadastrar receita/despesa/investimento
        self.btn_inserir_receita.clicked.connect(self.inserir_receita)
        self.btn_inserir_despesa.clicked.connect(self.inserir_despesa)
        self.btn_inserir_investimento.clicked.connect(self.inserir_investimento)
        # Botão editar receita/despesa/investimento
        self.btn_editar_receita.clicked.connect(self.editar_receitas)
        self.btn_editar_despesa.clicked.connect(self.editar_despesas)
        self.btn_editar_investimento.clicked.connect(self.editar_investimentos)
        # Botão excluir receita/despesa/investimento
        self.btn_excluir_receita.clicked.connect(self.deletar_receita)
        self.btn_excluir_despesa.clicked.connect(self.deletar_despesa)
        self.btn_excluir_investimento.clicked.connect(self.deletar_investimento)
        # Botão gerar excel receita/despesa/investimento
        self.btn_excel_receita.clicked.connect(self.excel_receitas)
        self.btn_excel_despesa.clicked.connect(self.excel_despesas)
        self.btn_excel_investimento.clicked.connect(self.excel_investimentos)

        # Gráficos transações receitas/despesas/investimentos
        self.gr_bar_rec_ = grafico_barra_receitas()
        self.gr_bar_receita.addWidget(self.gr_bar_rec_)
        self.gr_pie_rec_ = grafico_pizza_receitas()
        self.gr_pie_receita.addWidget(self.gr_pie_rec_)

        self.gr_bar_desp_ = grafico_barra_despesas()
        self.gr_bar_despesa.addWidget(self.gr_bar_desp_)
        self.gr_pie_desp_tp_ = grafico_pizza_despesas_tp()
        self.gr_pie_despesa_tp.addWidget(self.gr_pie_desp_tp_)
        self.gr_pie_desp_gr_ = grafico_pizza_despesas_gr()
        self.gr_pie_despesa_gr.addWidget(self.gr_pie_desp_gr_)

        self.gr_bar_inves_ = grafico_barra_investimentos()
        self.gr_bar_investimento.addWidget(self.gr_bar_inves_)
        self.gr_pie_inves_ = grafico_pizza_investimentos()
        self.gr_pie_investimento.addWidget(self.gr_pie_inves_)
        
        # Graficos Dashboard
        self.gr_linha_dash_ = grafico_linha_dash()
        self.gr_linha_dash.addWidget(self.gr_linha_dash_)

        self.gr_bar_comparativo_dash_ = grafico_barra_dash()
        self.gr_bar_comparativo_dash.addWidget(self.gr_bar_comparativo_dash_)

        self.gr_pie_rec_dash_ = grafico_pizza_receitas_dash()
        self.gr_pizza_receita_dash.addWidget(self.gr_pie_rec_dash_)

        self.gr_pie_desp_dash_ = grafico_pizza_despesas_dash()
        self.gr_pizza_despesa_dash.addWidget(self.gr_pie_desp_dash_)

    # Função para mostrar tela de cadastro de categorias
    def mostrar_tela_cat_receita(self):
        tela_categoria_receita = QDialog()
        loadUi('ui_catReceita.ui', tela_categoria_receita)
        tela_categoria_receita.setWindowTitle('Cadastro')
        tela_categoria_receita.btn_inserir_cat_receita.clicked.connect(lambda: MainWindow.inserir_cat_receita(tela_categoria_receita))
        tela_categoria_receita.btn_cancelar_cat_receita.clicked.connect(lambda: MainWindow.fecharTela(tela_categoria_receita))
        tela_categoria_receita.exec_()
        
        self.atualizar_cb_cat_receita()

    def mostrar_tela_cat_despesa(self):
        tela_categoria_despesa = QDialog()
        loadUi('ui_catDespesa.ui', tela_categoria_despesa)
        tela_categoria_despesa.setWindowTitle('Cadastro')
        tela_categoria_despesa.btn_inserir_cat_despesa.clicked.connect(lambda: MainWindow.inserir_cat_despesa(tela_categoria_despesa))
        tela_categoria_despesa.btn_cancelar_cat_despesa.clicked.connect(lambda: MainWindow.fecharTela(tela_categoria_despesa))
        tela_categoria_despesa.exec_()

        self.atualizar_cb_cat_despesa()

    def mostrar_tela_cat_invesitmento(self):
        tela_categoria_investimento = QDialog()
        loadUi('ui_catInvestimento.ui', tela_categoria_investimento)
        tela_categoria_investimento.setWindowTitle('Cadastro')
        tela_categoria_investimento.btn_inserir_cat_investimento.clicked.connect(lambda: MainWindow.inserir_cat_investimento(tela_categoria_investimento))
        tela_categoria_investimento.btn_cancelar_cat_investimento.clicked.connect(lambda: MainWindow.fecharTela(tela_categoria_investimento))
        tela_categoria_investimento.exec_()

        self.atualizar_cb_cat_investimento()

    # Função para cadastrar categorias
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

    # Função para atualizar o comboBox das categorias
    def atualizar_cb_cat_receita(self):
        categorias = db.ver_cat_receita()
        self.cb_cat_receita.clear()
        self.cb_cat_receita.addItems(categorias)
    
    def atualizar_cb_cat_despesa(self):
        categorias = db.ver_cat_despesa()
        self.cb_cat_despesa.clear()
        self.cb_cat_despesa.addItems(categorias)
    
    def atualizar_cb_cat_investimento(self):
        categorias = db.ver_cat_investimento()
        self.cb_cat_investimento.clear()
        self.cb_cat_investimento.addItems(categorias)

    # Função para fechar janela
    def fecharTela(self):
        self.reject()
    
    # Função para cadastrar receitas/despesas/investimentos
    def inserir_receita(self):
        categoria = self.cb_cat_receita.currentText()
        descricao = self.txt_desc_receita.text()
        data = self.calendar_receita.selectedDate().toString("dd-MM-yyyy")
        valor = float(self.txt_valor_receita.text().replace(',', '.'))
        tipo = 'Fixo' if self.rb_tipo_receita_1.isChecked() else 'Variável'
        
        db = DataBase()
        db.conectar()
        db.inserir_receita(categoria, descricao, data, valor, tipo)
        db.desconectar()

        msg = QMessageBox()
        msg.setWindowTitle('Lançamento de Receita')
        msg.setText('Receita inserida com sucesso')
        msg.exec()

        self.txt_valor_receita.setText('')
        self.txt_desc_receita.setText('')
        
        self.tabela_receitas()
        self.valores_sistema()
        self.atualizar_graficos()

    def inserir_despesa(self):
        categoria = self.cb_cat_despesa.currentText()
        descricao = self.txt_desc_despesa.text()
        data = self.calendar_despesa.selectedDate().toString("dd-MM-yyyy")
        valor = float(self.txt_valor_despesa.text())
        tipo = 'Fixo' if self.rb_tipo_despesa_1.isChecked() else 'Variável'
        grupo = 'Essencial' if self.chb_grupo_1.isChecked() else 'Não Essencial'

        db = DataBase()
        db.conectar()
        db.inserir_despesa(categoria, descricao, data, valor, tipo, grupo)
        db.desconectar()

        msg = QMessageBox()
        msg.setWindowTitle('Lançamento de Despesa')
        msg.setText('Receita inserida com sucesso')
        msg.exec()

        self.txt_valor_despesa.setText('')
        self.txt_desc_despesa.setText('')
        self.chb_grupo_1.setChecked(False)
        self.chb_grupo_2.setChecked(False)

        self.tabela_despesas()
        self.valores_sistema()
        self.atualizar_graficos()

    def inserir_investimento(self):
        categoria = self.cb_cat_investimento.currentText()
        descricao = self.txt_desc_investimento.text()
        data = self.calendar_investimento.selectedDate().toString("dd-MM-yyyy")
        valor = float(self.txt_valor_investimento.text().replace(',', '.'))
        tipo = 'Fixo' if self.rb_tipo_investimento_1.isChecked() else 'Variável'

        db = DataBase()
        db.conectar()
        db.inserir_investimento(categoria, descricao, data, valor, tipo)
        db.desconectar()

        msg = QMessageBox()
        msg.setWindowTitle('Lançamento de Investimento')
        msg.setText('Invesitmento inserido com sucesso')
        msg.exec()

        self.txt_valor_investimento.setText('')
        self.txt_desc_investimento.setText('')

        self.tabela_investimentos()
        self.valores_sistema()
        self.atualizar_graficos()

    # Função para povoar tabelas
    def tabela_receitas(self):
        db = DataBase()
        db.conectar()
        receitas = db.select_receitas()
        
        self.tw_receita_1.clearContents()
        self.tw_receita_1.setRowCount(len(receitas))

        for linha, texto in enumerate(receitas):
            for coluna, dado in enumerate(texto):
                self.tw_receita_1.setItem(linha, coluna, QTableWidgetItem(str(dado)))
        
        db.desconectar()

        # Ordenar por coluna
        self.tw_receita_1.setSortingEnabled(True)
        # Largura da coluna automática
        for i in range(1, 6):
            self.tw_receita_1.resizeColumnToContents(i)
    
    def tabela_despesas(self):
        db = DataBase()
        db.conectar()
        despesas = db.select_despesas()

        self.tw_despesa_1.clearContents()
        self.tw_despesa_1.setRowCount(len(despesas))

        for linha, texto in enumerate(despesas):
            for coluna, dado in enumerate(texto):
                self.tw_despesa_1.setItem(linha, coluna, QTableWidgetItem(str(dado)))
        
        db.desconectar()

        # Ordenar por coluna
        self.tw_despesa_1.setSortingEnabled(True)
        # Largura da coluna automática
        for i in range(1, 7):
            self.tw_despesa_1.resizeColumnToContents(i)

    def tabela_investimentos(self):
        db = DataBase()
        db.conectar()
        investimentos = db.select_investimentos()

        self.tw_investimento_1.clearContents()
        self.tw_investimento_1.setRowCount(len(investimentos))

        for linha, texto in enumerate(investimentos):
            for coluna, dado in enumerate(texto):
                self.tw_investimento_1.setItem(linha, coluna, QTableWidgetItem(str(dado)))
        
        db.desconectar()

        # Ordenar por coluna
        self.tw_investimento_1.setSortingEnabled(True)
        # Largura da coluna automática
        for i in range(1, 6):
            self.tw_investimento_1.resizeColumnToContents(i)

    # Função para editar lançamentos
    def editar_receitas(self):
        dados = []
        atualizar_dados = []    

        for linha in range(self.tw_receita_1.rowCount()):
            for coluna in range(self.tw_receita_1.columnCount()):
                dados.append(self.tw_receita_1.item(linha, coluna).text())
            atualizar_dados.append(dados)
            dados = []
        
        db = DataBase()
        db.conectar()
        for receita in atualizar_dados:
            db.editar_receitas(tuple(receita))
        db.desconectar()

        msg = QMessageBox()
        msg.setWindowTitle('Atualização de Dados')
        msg.setText('Dados atualizados com sucesso')
        msg.exec()

        self.valores_sistema()
        self.atualizar_graficos()

    def editar_despesas(self):
        dados = []
        atualizar_dados = []    

        for linha in range(self.tw_despesa_1.rowCount()):
            for coluna in range(self.tw_despesa_1.columnCount()):
                dados.append(self.tw_despesa_1.item(linha, coluna).text())
            atualizar_dados.append(dados)
            dados = []
        
        db = DataBase()
        db.conectar()
        for despesa in atualizar_dados:
            db.editar_despesas(tuple(despesa))
        db.desconectar()

        msg = QMessageBox()
        msg.setWindowTitle('Atualização de Dados')
        msg.setText('Dados atualizados com sucesso')
        msg.exec()

        self.valores_sistema()
        self.atualizar_graficos()

    def editar_investimentos(self):
        dados = []
        atualizar_dados = []    

        for linha in range(self.tw_investimento_1.rowCount()):
            for coluna in range(self.tw_investimento_1.columnCount()):
                dados.append(self.tw_investimento_1.item(linha, coluna).text())
            atualizar_dados.append(dados)
            dados = []
        
        db = DataBase()
        db.conectar()
        for investimento in atualizar_dados:
            db.editar_investimentos(tuple(investimento))
        db.desconectar()

        msg = QMessageBox()
        msg.setWindowTitle('Atualização de Dados')
        msg.setText('Dados atualizados com sucesso')
        msg.exec()

        self.valores_sistema()
        self.atualizar_graficos()

    # Função para deletar lançamentos
    def deletar_receita(self):
        db = DataBase()
        db.conectar()

        msg = QMessageBox()
        msg.setWindowTitle('Excluir')
        msg.setText('Este registro será excluído')
        msg.setInformativeText('Você tem certeza que deseja excluir esse lançamento?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()

        if resp == QMessageBox.Yes:
            id = self.tw_receita_1.selectionModel().currentIndex().siblingAtColumn(0).data()
            resultado = db.delete_receitas(id)
            self.tabela_receitas()

            msg = QMessageBox()
            msg.setWindowTitle('Receitas')
            msg.setText(resultado)
            msg.exec()

        db.desconectar()

        self.valores_sistema()
        self.atualizar_graficos()
   
    def deletar_despesa(self):
        db = DataBase()
        db.conectar()

        msg = QMessageBox()
        msg.setWindowTitle('Excluir')
        msg.setText('Este registro será excluído')
        msg.setInformativeText('Você tem certeza que deseja excluir esse lançamento?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()

        if resp == QMessageBox.Yes:
            id = self.tw_despesa_1.selectionModel().currentIndex().siblingAtColumn(0).data()
            resultado = db.delete_despesas(id)
            self.tabela_despesas()

            msg = QMessageBox()
            msg.setWindowTitle('Despesas')
            msg.setText(resultado)
            msg.exec()

        db.desconectar()

        self.valores_sistema()
        self.atualizar_graficos()

    def deletar_investimento(self):
        db = DataBase()
        db.conectar()

        msg = QMessageBox()
        msg.setWindowTitle('Excluir')
        msg.setText('Este registro será excluído')
        msg.setInformativeText('Você tem certeza que deseja excluir esse lançamento?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()

        if resp == QMessageBox.Yes:
            id = self.tw_investimento_1.selectionModel().currentIndex().siblingAtColumn(0).data()
            resultado = db.delete_investimentos(id)
            self.tabela_investimentos()

            msg = QMessageBox()
            msg.setWindowTitle('Investimentos')
            msg.setText(resultado)
            msg.exec()

        db.desconectar()

        self.valores_sistema()
        self.atualizar_graficos()

    # Função para gerar relátorio Excel
    def excel_receitas(self):
        cnx = sqlite3.connect('database.db')
        receitas = pd.read_sql_query("SELECT * FROM Receitas", cnx)
        caminho_arquivo = os.path.expanduser('~/Desktop/Receitas.xlsx')
        receitas.to_excel(caminho_arquivo, sheet_name='Receitas', index=False)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Excel')
        msg.setText('Relatório excel gerado com sucesso!')
        msg.exec()

    def excel_despesas(self):
        cnx = sqlite3.connect('database.db')
        despesas = pd.read_sql_query("SELECT * FROM Despesas", cnx)
        caminho_arquivo = os.path.expanduser('~/Desktop/Despesas.xlsx')
        despesas.to_excel(caminho_arquivo, sheet_name='Despesas', index=False)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Excel')
        msg.setText('Relatório excel gerado com sucesso!')
        msg.exec()

    def excel_investimentos(self):
        cnx = sqlite3.connect('database.db')
        investimentos = pd.read_sql_query("SELECT * FROM Investimentos", cnx)
        caminho_arquivo = os.path.expanduser('~/Desktop/Investimentos.xlsx')
        investimentos.to_excel(caminho_arquivo, sheet_name='Investimentos', index=False)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Excel')
        msg.setText('Relatório excel gerado com sucesso!')
        msg.exec()

    # Função para inserir valores no dashboard
    def valor_total_receita(self):
        lista_valor_receita = db.ver_receita()

        total_receita = sum(float(i[4]) for i in lista_valor_receita)
        
        locale.setlocale(locale.LC_ALL, 'pt_BR')
        total_formatado_receita = locale.currency(total_receita, grouping=True)

        return total_formatado_receita
    
    def valor_total_despesa(self):
        lista_valor_despesa = db.ver_despesa()

        total_despesa = sum(float(i[4]) for i in lista_valor_despesa)

        locale.setlocale(locale.LC_ALL, 'pt_BR')
        total_formatado_despesa = locale.currency(total_despesa, grouping=True)

        return total_formatado_despesa

    def valor_total_investimento(self):
        lista_valor_investimento = db.ver_investimento()

        total_investimento = sum(float(i[4]) for i in lista_valor_investimento)
        
        locale.setlocale(locale.LC_ALL, 'pt_BR')
        total_formatado_investimento = locale.currency(total_investimento, grouping=True)

        return total_formatado_investimento
    
    def valor_saldo(self):
        lista_valor_receita = db.ver_receita()
        lista_valor_despesa = db.ver_despesa()
        lista_valor_investimento = db.ver_investimento()

        total_receita = sum(float(i[4]) for i in lista_valor_receita)
        total_despesa = sum(float(i[4]) for i in lista_valor_despesa)
        total_investimento = sum(float(i[4]) for i in lista_valor_investimento)
        
        saldo = total_receita - total_despesa - total_investimento

        locale.setlocale(locale.LC_ALL, 'pt_BR')
        saldo_formatado = locale.currency(saldo, grouping=True)

        return saldo_formatado

    # Função barra de percentagem dash
    def percentagem_receita_dash(self):
        lista_valor_receita = db.ver_receita()
        lista_valor_despesa = db.ver_despesa()

        total_receita = sum(float(i[4]) for i in lista_valor_receita)
        total_despesa = sum(float(i[4]) for i in lista_valor_despesa)

        if total_receita != 0:
            porcentagem_despesa = (total_despesa / total_receita) * 100
            self.receita_gasta_dash.setValue(int(porcentagem_despesa))
        else:
            self.receita_gasta_dash.setValue(0)
    
    def percentagem_despesa_essencial(self):
        lista_valor_receita = db.ver_receita()
        lista_despesa_essencial = db.ver_despesa_essencial()

        total_receita = sum(float(i[4]) for i in lista_valor_receita)
        total_despesa = sum(float(i[4]) for i in lista_despesa_essencial)

        if total_receita != 0:
            porcentagem_despesa = (total_despesa / total_receita) * 100
            self.despesas_essenciais_dash.setValue(int(porcentagem_despesa))
        else:
            self.despesas_essenciais_dash.setValue(0)

    def percentagem_despesa_n_essencial(self):
        lista_valor_receita = db.ver_receita()
        lista_despesa_n_essencial = db.ver_despesa_n_essencial()

        total_receita = sum(float(i[4]) for i in lista_valor_receita)
        total_despesa = sum(float(i[4]) for i in lista_despesa_n_essencial)

        if total_receita != 0:
            porcentagem_despesa = (total_despesa / total_receita) * 100
            self.despesas_n_essenciais_dash.setValue(int(porcentagem_despesa))
        else:
            self.despesas_n_essenciais_dash.setValue(0)

    def percentagem_investimento(self):
        lista_valor_receita = db.ver_receita()
        lista_valor_investimento = db.ver_investimento()
        
        total_receita = sum(float(i[4]) for i in lista_valor_receita)
        total_investimento = sum(float(i[4]) for i in lista_valor_investimento)

        if total_receita != 0:
            porcentagem_invesitmento = (total_investimento / total_receita) * 100
            self.investimentos_dash.setValue(int(porcentagem_invesitmento))
        else:
            self.investimentos_dash.setValue(0)

    # Atualizador de funções
    def atualizar_funcoes(self):
        self.atualizar_cb_cat_receita()
        self.atualizar_cb_cat_despesa()
        self.atualizar_cb_cat_investimento()
        self.tabela_receitas()
        self.tabela_despesas()
        self.tabela_investimentos()

    def valores_sistema(self):
        total_receita = self.valor_total_receita()
        total_despesa = self.valor_total_despesa()
        total_investimento = self.valor_total_investimento()
        saldo = self.valor_saldo()

        self.lbl_total_receita_1.setText(str(total_receita))
        self.lbl_total_receita_2.setText(str(total_receita))
        self.lbl_total_despesa_1.setText(str(total_despesa))
        self.lbl_total_despesa_2.setText(str(total_despesa))
        self.lbl_saldo.setText(str(saldo))
        self.lbl_total_investimento_1.setText(str(total_investimento))
        self.lbl_total_investimento_2.setText(str(total_investimento))

        self.percentagem_receita_dash()
        self.percentagem_despesa_essencial()
        self.percentagem_despesa_n_essencial()
        self.percentagem_investimento()

    def atualizar_graficos(self):
        self.gr_linha_dash_.atualizar_linha_dash()
        self.gr_bar_comparativo_dash_.atualizar_bar_dash()
        self.gr_pie_rec_dash_.atualizar_grafico_pizza_receita_dash()
        self.gr_pie_desp_dash_.atualizar_grafico_pizza_despesa_dash()
        self.gr_bar_rec_.atualizar_barra_receitas()
        self.gr_pie_rec_.atualizar_grafico_pizza_receita()
        self.gr_bar_desp_.atualizar_barra_despesas()
        self.gr_pie_desp_tp_.atualizar_grafico_pizza_despesa_tp()
        self.gr_pie_desp_gr_.atualizar_grafico_pizza_despesa_gr()
        self.gr_bar_inves_.atualizar_barra_investimentos()
        self.gr_pie_inves_.atualizar_grafico_pizza_investimento()

# Graficos transações receitas/despesas/investimentos
class grafico_barra_receitas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(6, 6), sharey=True, facecolor='white')
        super().__init__(self.fig)
        
        lista_receitas = db.ver_receita()

        if lista_receitas:
            soma_valores_categoria = defaultdict(float)

            for item in lista_receitas:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em receitas: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            self.ax.bar(categorias, valores, zorder=2)

            self.ax.grid(True, axis='y')
            self.fig.suptitle('Categoria Receita')

            self.fig.tight_layout()
            self.draw()

        self.atualizar_barra_receitas()

    def atualizar_barra_receitas(self):
        lista_receitas = db.ver_receita()

        if lista_receitas:
            soma_valores_categoria = defaultdict(float)

            for item in lista_receitas:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em receitas: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            self.ax.clear()

            self.ax.bar(categorias, valores, zorder=2)

            self.fig.suptitle('Categoria Receita')
            self.ax.grid(True, axis='y')
            self.fig.tight_layout()
            self.draw()

class grafico_pizza_receitas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(4, 4), sharey=True, facecolor='white')
        super().__init__(self.fig)

        lista_receitas = db.ver_receita()

        if lista_receitas:
            soma_valores_tipo = defaultdict(float)

            for item in lista_receitas:
                tipo = item[5]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em receitas: {valor_str}')
                    continue

                soma_valores_tipo[tipo] += valor

            dados_grafico = list(soma_valores_tipo.items())
            
            tipos, valores = zip(*dados_grafico)

            explode = [0.03] * len(tipos)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=tipos, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.axis('equal')

            self.ax.set_title('Classificação Receita')

            self.fig.tight_layout()
            self.draw()
        
        self.atualizar_grafico_pizza_receita()

    def atualizar_grafico_pizza_receita(self):
        lista_receitas = db.ver_receita()

        if lista_receitas:
            soma_valores_tipo = defaultdict(float)

            for item in lista_receitas:
                tipo = item[5]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em receitas: {valor_str}')
                    continue

                soma_valores_tipo[tipo] += valor

            dados_grafico = list(soma_valores_tipo.items())
            
            tipos, valores = zip(*dados_grafico)

            self.ax.clear()

            explode = [0.03] * len(tipos)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=tipos, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.axis('equal')

            self.ax.set_title('Classificação Receita')

            self.fig.tight_layout()
            self.draw()

class grafico_barra_despesas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(6, 6), sharey=True, facecolor='white')
        super().__init__(self.fig)
        
        lista_despesas = db.ver_despesa()

        if lista_despesas:
            soma_valores_categoria = defaultdict(float)

            for item in lista_despesas:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em despesas: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            self.ax.bar(categorias, valores, zorder=2)

            self.fig.suptitle('Categoria Despesa')
            self.ax.grid(True, axis='y')
            self.fig.tight_layout()
            self.draw()

        self.atualizar_barra_despesas()

    def atualizar_barra_despesas(self):
        lista_despesas = db.ver_despesa()

        if lista_despesas:
            soma_valores_categoria = defaultdict(float)

            for item in lista_despesas:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em despesas: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            self.ax.clear()

            self.ax.bar(categorias, valores, zorder=2)

            self.fig.suptitle('Categoria Despesa')
            self.ax.grid(True, axis='y')
            self.fig.tight_layout()
            self.draw()

class grafico_pizza_despesas_tp(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(4, 4), sharey=True, facecolor='white')
        super().__init__(self.fig)

        lista_despesas = db.ver_despesa()

        if lista_despesas:
            soma_valores_tipo = defaultdict(float)

            for item in lista_despesas:
                tipo = item[5]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em despesas: {valor_str}')
                    continue

                soma_valores_tipo[tipo] += valor

            dados_grafico = list(soma_valores_tipo.items())
            
            tipos, valores = zip(*dados_grafico)

            explode = [0.03] * len(tipos)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=tipos, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.axis('equal')

            self.ax.set_title('Classificação Despesa')

            self.fig.tight_layout()
            self.draw()
        
        self.atualizar_grafico_pizza_despesa_tp()

    def atualizar_grafico_pizza_despesa_tp(self):
        lista_despesas = db.ver_despesa()

        if lista_despesas:
            soma_valores_tipo = defaultdict(float)

            for item in lista_despesas:
                tipo = item[5]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em despesas: {valor_str}')
                    continue

                soma_valores_tipo[tipo] += valor

            dados_grafico = list(soma_valores_tipo.items())
            
            tipos, valores = zip(*dados_grafico)

            self.ax.clear()

            explode = [0.03] * len(tipos)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=tipos, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.axis('equal')

            self.ax.set_title('Classificação Despesa')

            self.fig.tight_layout()
            self.draw()

class grafico_pizza_despesas_gr(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(4, 4), sharey=True, facecolor='white')
        super().__init__(self.fig)

        lista_despesas = db.ver_despesa()

        if lista_despesas:
            soma_valores_grupo = defaultdict(float)

            for item in lista_despesas:
                grupo = item[6]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em despesas: {valor_str}')
                    continue

                soma_valores_grupo[grupo] += valor

            dados_grafico = list(soma_valores_grupo.items())
            
            grupos, valores = zip(*dados_grafico)

            explode = [0.03] * len(grupos)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=grupos, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.axis('equal')

            self.ax.set_title('Grupo Despesa')

            self.fig.tight_layout()
            self.draw()
        
        self.atualizar_grafico_pizza_despesa_gr()

    def atualizar_grafico_pizza_despesa_gr(self):
        lista_despesas = db.ver_despesa()

        if lista_despesas:
            soma_valores_grupo = defaultdict(float)

            for item in lista_despesas:
                grupo = item[6]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em despesas: {valor_str}')
                    continue

                soma_valores_grupo[grupo] += valor

            dados_grafico = list(soma_valores_grupo.items())
            
            grupos, valores = zip(*dados_grafico)

            self.ax.clear()

            explode = [0.03] * len(grupos)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=grupos, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.axis('equal')

            self.ax.set_title('Grupo Despesa')

            self.fig.tight_layout()
            self.draw()

class grafico_barra_investimentos(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(6, 6), sharey=True, facecolor='white')
        super().__init__(self.fig)
        
        lista_investimentos = db.ver_investimento()

        if lista_investimentos:
            soma_valores_categoria = defaultdict(float)

            for item in lista_investimentos:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em investimentos: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            self.ax.bar(categorias, valores, zorder=2)

            self.fig.suptitle('Categoria Investimento')
            self.ax.grid(True, axis='y')
            self.fig.tight_layout()
            self.draw()

        self.atualizar_barra_investimentos()

    def atualizar_barra_investimentos(self):
        lista_investimentos = db.ver_investimento()

        if lista_investimentos:
            soma_valores_categoria = defaultdict(float)

            for item in lista_investimentos:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em investimentos: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            self.ax.clear()

            self.ax.bar(categorias, valores, zorder=2)

            self.fig.suptitle('Categoria Investimento')
            self.ax.grid(True, axis='y')
            self.fig.tight_layout()
            self.draw()

class grafico_pizza_investimentos(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(4, 4), sharey=True, facecolor='white')
        super().__init__(self.fig)

        lista_investimentos = db.ver_investimento()

        if lista_investimentos:
            soma_valores_tipo = defaultdict(float)

            for item in lista_investimentos:
                tipo = item[5]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em investimentos: {valor_str}')
                    continue

                soma_valores_tipo[tipo] += valor

            dados_grafico = list(soma_valores_tipo.items())
            
            tipos, valores = zip(*dados_grafico)

            explode = [0.03] * len(tipos)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=tipos, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.axis('equal')

            self.ax.set_title('Classificação Invesitmento')

            self.fig.tight_layout()
            self.draw()
        
        self.atualizar_grafico_pizza_investimento()

    def atualizar_grafico_pizza_investimento(self):
        lista_investimentos = db.ver_investimento()

        if lista_investimentos:
            soma_valores_tipo = defaultdict(float)

            for item in lista_investimentos:
                tipo = item[5]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em investimentos: {valor_str}')
                    continue

                soma_valores_tipo[tipo] += valor

            dados_grafico = list(soma_valores_tipo.items())
            
            tipos, valores = zip(*dados_grafico)

            self.ax.clear()

            explode = [0.03] * len(tipos)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=tipos, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.axis('equal')

            self.ax.set_title('Classificação Investimento')

            self.fig.tight_layout()
            self.draw()

# Gráficos Dashboard
class grafico_linha_dash(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(7, 6), sharey=True, facecolor='white')
        super().__init__(self.fig)

        lista_invesitmentos = db.ver_investimento()
        if lista_invesitmentos:
            soma_valores_periodo = defaultdict(float)

            for item in lista_invesitmentos:
                periodo = item[3]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em despesas: {valor_str}')
                    continue

                soma_valores_periodo[periodo] += valor

            dados_grafico = list(soma_valores_periodo.items())

            dados_formatados = [(datetime.strptime(periodo, "%d-%m-%Y"), valor) for periodo, valor in dados_grafico]
            dados_formatados.sort()

            data_formatada = DateFormatter("%d-%m-%Y")
            self.ax.xaxis.set_major_formatter(data_formatada)
            
            periodos, valores = zip(*dados_formatados)

            self.ax.plot(periodos, valores)

            self.fig.suptitle('Evolução Investimento')
            self.ax.set_xlabel('Período')
            self.ax.set_ylabel('Valor R$')

            for i, txt in enumerate(valores):
                self.ax.text(periodos[i], valores[i], f'{txt:.2f}'.replace(".", ","), ha='center', va='top')


            self.ax.grid(True, axis='y')
            self.fig.tight_layout()
            self.draw()

    def atualizar_linha_dash(self, parent=None):

        lista_invesitmentos = db.ver_investimento()
        if lista_invesitmentos:
            soma_valores_periodo = defaultdict(float)

            for item in lista_invesitmentos:
                periodo = item[3]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em despesas: {valor_str}')
                    continue

                soma_valores_periodo[periodo] += valor

            dados_grafico = list(soma_valores_periodo.items())

            dados_formatados = [(datetime.strptime(periodo, "%d-%m-%Y"), valor) for periodo, valor in dados_grafico]
            dados_formatados.sort()

            data_formatada = DateFormatter("%d-%m-%Y")
            self.ax.xaxis.set_major_formatter(data_formatada)

            self.ax.clear()
            
            periodos, valores = zip(*dados_formatados)

            self.ax.plot(periodos, valores)

            self.fig.suptitle('Evolução Investimento')
            self.ax.set_xlabel('Período')
            self.ax.set_ylabel('Valor')

            for i, txt in enumerate(valores):
                self.ax.text(periodos[i], valores[i], f'{txt:.2f}'.replace(".", ","), ha='center', va='top')
            
            self.ax.grid(True, axis='y')
            self.fig.tight_layout()
            self.draw()

class grafico_barra_dash(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(5, 5), sharey=True, facecolor='white')
        super().__init__(self.fig)
        
        lista_receitas = db.ver_receita()
        lista_despesas = db.ver_despesa()
        lista_investimentos = db.ver_investimento()

        totRec = sum(float(item[4]) for item in lista_receitas)
        totDesp = sum(float(item[4]) for item in lista_despesas)
        totInv = sum(float(item[4]) for item in lista_investimentos)
        
        lista_categorias = ['Receitas', 'Despesas', 'Investimentos']
        lista_valores = [totRec, totDesp, totInv]
        
        bars = self.ax.bar(lista_categorias, lista_valores, zorder=2)

        self.ax.set_ylabel('Valor R$')
        self.ax.grid(True, axis='y')
        self.fig.suptitle('Comparativo')

        for bar in bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}'.replace(".", ","), ha='center', va='bottom')

        self.fig.tight_layout()
        self.draw()
    
    def atualizar_bar_dash(self):
        lista_receitas = db.ver_receita()
        lista_despesas = db.ver_despesa()
        lista_investimentos = db.ver_investimento()

        totRec = sum(float(item[4]) for item in lista_receitas)
        totDesp = sum(float(item[4]) for item in lista_despesas)
        totInv = sum(float(item[4]) for item in lista_investimentos)
        
        lista_categorias = ['Receitas', 'Despesas', 'Invesitmentos']
        lista_valores = [totRec, totDesp, totInv]

        self.ax.clear()
        
        bars = self.ax.bar(lista_categorias, lista_valores, zorder=2)

        self.ax.set_ylabel('Valor R$')
        self.ax.grid(True, axis='y')
        self.fig.suptitle('Comparativo')

        for bar in bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}'.replace(".", ","), ha='center', va='bottom')
        
        self.fig.tight_layout()
        self.draw()

class grafico_pizza_receitas_dash(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(4, 4), sharey=True, facecolor='white')
        super().__init__(self.fig)

        lista_receitas = db.ver_receita()

        if lista_receitas:
            soma_valores_categoria = defaultdict(float)

            for item in lista_receitas:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em receitas: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            explode = [0.03] * len(categorias)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=categorias, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.set_title('Receitas')
            self.ax.axis('equal')

            self.fig.tight_layout()
            self.draw()

        self.atualizar_grafico_pizza_receita_dash()

    def atualizar_grafico_pizza_receita_dash(self):
        lista_receitas = db.ver_receita()

        if lista_receitas:
            soma_valores_categoria = defaultdict(float)

            for item in lista_receitas:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em receitas: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            self.ax.clear()

            explode = [0.03] * len(categorias)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=categorias, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.set_title('Receitas')
            self.ax.axis('equal')

            self.fig.tight_layout()
            self.draw()

class grafico_pizza_despesas_dash(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(4, 4), sharey=True, facecolor='white')
        super().__init__(self.fig)

        lista_despesas = db.ver_despesa()
        if lista_despesas:
            soma_valores_categoria = defaultdict(float)

            for item in lista_despesas:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em despesas: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            explode = [0.03] * len(categorias)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=categorias, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.set_title('Despesas')
            self.ax.axis('equal')

            self.fig.tight_layout()
            self.draw()
    
    def atualizar_grafico_pizza_despesa_dash(self):
        lista_despesas = db.ver_despesa()
        if lista_despesas:
            soma_valores_categoria = defaultdict(float)

            for item in lista_despesas:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em despesas: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            self.ax.clear()

            explode = [0.03] * len(categorias)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=categorias, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.set_title('Despesas')
            self.ax.axis('equal')

            self.fig.tight_layout()
            self.draw()


# Em desenvolvimento...
class grafico_pizza_receitas_periodo(FigureCanvas):
    def __init__(self, parent=None, dt_inicial=None, dt_final=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(4, 4), sharey=True, facecolor='white')
        super().__init__(self.fig)

        self.dt_inicial = dt_inicial.strftime("%d-%m-%Y")
        self.dt_final = dt_final.strftime("%d-%m-%Y")

        print(dt_inicial, dt_final)
        
        lista_receitas = db.ver_receita_periodo(dt_inicial=self.dt_inicial, dt_final=self.dt_final)

        if lista_receitas:
            soma_valores_categoria = defaultdict(float)

            for item in lista_receitas:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em receitas: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            explode = [0.03] * len(categorias)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=categorias, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.set_title('Receitas')
            self.ax.axis('equal')

            self.fig.tight_layout()
            self.draw()

    def atualizar(self, dt_inicial, dt_final):
        self.dt_inicial = dt_inicial.strftime("%d-%m-%Y")
        self.dt_final = dt_final.strftime("%d-%m-%Y")

        print(dt_inicial, dt_final)

        self.ax.clear()

        lista_receitas = db.ver_receita_periodo(dt_inicial=self.dt_inicial, dt_final=self.dt_final)

        if lista_receitas:
            soma_valores_categoria = defaultdict(float)

            for item in lista_receitas:
                categoria = item[1]
                valor_str = item[4]

                try:
                    valor = float(valor_str)
                except ValueError:
                    print(f'Erro: Valor incorreto encontrado em receitas: {valor_str}')
                    continue

                soma_valores_categoria[categoria] += valor

            dados_grafico = list(soma_valores_categoria.items())
            
            categorias, valores = zip(*dados_grafico)

            explode = [0.03] * len(categorias)

            self.ax.pie(valores, explode=explode, wedgeprops=dict(width=0.2), labels=categorias, autopct='%1.1f%%', pctdistance=0.5, shadow=True, startangle=60, radius=1.0, labeldistance=1.1)
            self.ax.set_title('Receitas')
            self.ax.axis('equal')

            self.fig.tight_layout()
            self.draw()


if __name__ == '__main__':
    db = DataBase()
    db.conectar()
    db.tabCatReceita()
    db.tabCatDespesa()
    db.tabCatInvestimento()
    db.tabReceitas()
    db.tabDespesas()
    db.tabInvestimentos()
    db.desconectar()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
