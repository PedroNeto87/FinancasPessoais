import sqlite3


class DataBase:
    # funções inicializar, conectar e desconectar o banco de dados
    def __init__(self, name = 'database.db') -> None:
        self.name = name

    def conectar(self):
        self.conexao = sqlite3.connect(self.name)
    
    def desconectar(self):
        try:
            self.connection.close()
        except:
            pass

    # função para criar as tabelas do sistema
    def tabCatReceita(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS catReceitas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Descricao TEXT NOT NULL
                );
            """)
        except AttributeError:
            print('Não foi possível criar a tabela de categorias da receita.')

    def tabCatDespesa(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS catDespesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Descricao TEXT NOT NULL
                );
            """)
        except AttributeError:
            print('Não foi possível criar a tabela de categorias da despesa.')

    def tabCatInvestimento(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS catInvestimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Descricao TEXT NOT NULL
                );
            """)
        except AttributeError:
            print('Não foi possível criar a tabela de categorias de investimentos.')

    def tabReceitas(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Receitas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Categoria TEXT NOT NULL,
                Descricao TEXT NOT NULL,
                Data DATE NOT NULL,
                Valor DECIMAL NOT NULL,
                Tipo TEXT CHECK(Tipo IN('Fixo', 'Variável')) NOT NULL                
                );
            """)
        except AttributeError:
            print('Não foi possível criar a tabela de receitas.')

    def tabDespesas(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Categoria TEXT NOT NULL,
                Descricao TEXT NOT NULL,
                Data DATE NOT NULL,
                Valor DECIMAL NOT NULL,
                Tipo TEXT CHECK(Tipo IN('Fixo', 'Variável')) NOT NULL,
                Grupo TEXT CHECK(Grupo IN('Essencial', 'Não Essencial')) NOT NULL
                );
            """)
        except AttributeError:
            print('Não foi possível criar a tabela de despesas.')

    def tabInvestimentos(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Investimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Categoria TEXT NOT NULL,
                Descricao TEXT NOT NULL,
                Data DATE NOT NULL,
                Valor DECIMAL NOT NULL,
                Tipo TEXT CHECK(Tipo IN('Fixo', 'Variável')) NOT NULL
                );
            """)
        except AttributeError:
            print('Não foi possível criar a tabela de Investimentos.')

    # função para inserir os dados nas tabelas do sistema
    def inserir_cat_receita(self, Descricao):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""INSERT INTO catReceitas (Descricao) VALUES (?)""", (Descricao,))
            self.conexao.commit()
        except Exception as ex:
            print(f'Erro: {ex}')

    def inserir_cat_despesa(self, Descricao):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""INSERT INTO catDespesas (Descricao) VALUES (?)""", (Descricao,))
            self.conexao.commit()
        except Exception as ex:
            print(f'Erro: {ex}')
    
    def inserir_cat_investimento(self, Descricao):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""INSERT INTO catInvestimentos (Descricao) VALUES (?)""", (Descricao,))
            self.conexao.commit()
        except Exception as ex:
            print(f'Erro: {ex}')

    def inserir_receita(self, Categoria, Descricao, Data, Valor, Tipo):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""INSERT INTO Receitas (Categoria, Descricao, Data, Valor, Tipo) VALUES (?,?,?,?,?)""", (Categoria, Descricao, Data, Valor, Tipo))
            self.conexao.commit()
        except Exception as ex:
            print(f'Erro: {ex}')

    def inserir_despesa(self, Categoria, Descricao, Data, Valor, Tipo, Grupo):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""INSERT INTO Despesas (Categoria, Descricao, Data, Valor, Tipo, Grupo) VALUES (?,?,?,?,?,?)""", (Categoria, Descricao, Data, Valor, Tipo, Grupo))
            self.conexao.commit()
        except Exception as ex:
            print(f'Erro: {ex}')

    def inserir_investimento(self, Categoria, Descricao, Data, Valor, Tipo):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""INSERT INTO Investimentos (Categoria, Descricao, Data, Valor, Tipo) VALUES (?,?,?,?,?)""", (Categoria, Descricao, Data, Valor, Tipo))
            self.conexao.commit()
        except Exception as ex:
            print(f'Erro: {ex}')

    # função select tabelas
    def select_receitas(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("SELECT * FROM Receitas ORDER BY id")
            receitas = cursor.fetchall()
            return receitas
        except AttributeError:
            print('Faça a conexão')
    
    def select_despesas(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("SELECT * FROM Despesas ORDER BY id")
            despesas = cursor.fetchall()
            return despesas
        except AttributeError:
            print('Faça a conexão')

    def select_investimentos(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("SELECT * FROM Investimentos ORDER BY id")
            investimentos = cursor.fetchall()
            return investimentos
        except AttributeError:
            print('Faça a conexão')

    # Função para editar lançamentos
    def editar_receitas(self, fullDataSet):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(f"""UPDATE Receitas SET
                id = '{fullDataSet[0]}',
                Categoria = '{fullDataSet[1]}',
                Descricao = '{fullDataSet[2]}',
                Data = '{fullDataSet[3]}',
                Valor = '{fullDataSet[4]}',
                Tipo = '{fullDataSet[5]}'

                WHERE id = '{fullDataSet[0]}'
            """)
            self.conexao.commit()
        except AttributeError:
            print('Faça a conexão')

    def editar_despesas(self, fullDataSet):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(f"""UPDATE Despesas SET
                id = '{fullDataSet[0]}',
                Categoria = '{fullDataSet[1]}',
                Descricao = '{fullDataSet[2]}',
                Data = '{fullDataSet[3]}',
                Valor = '{fullDataSet[4]}',
                Tipo = '{fullDataSet[5]}',
                Grupo = '{fullDataSet[6]}'

                WHERE id = '{fullDataSet[0]}'
            """)
            self.conexao.commit()
        except AttributeError:
            print('Faça a conexão')

    def editar_investimentos(self, fullDataSet):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(f"""UPDATE Investimentos SET
                id = '{fullDataSet[0]}',
                Categoria = '{fullDataSet[1]}',
                Descricao = '{fullDataSet[2]}',
                Data = '{fullDataSet[3]}',
                Valor = '{fullDataSet[4]}',
                Tipo = '{fullDataSet[5]}'

                WHERE id = '{fullDataSet[0]}'
            """)
            self.conexao.commit()
        except AttributeError:
            print('Faça a conexão')        

    # Função para deletar lançamentos
    def delete_receitas(self, id):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(f"DELETE FROM Receitas WHERE id = {id}")
            self.conexao.commit()
            return ('Lançamento excluído com sucesso')
        except:
            return ('Erro ao excluir registro.')
        
    def delete_despesas(self, id):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(f"DELETE FROM Despesas WHERE id = {id}")
            self.conexao.commit()
            return ('Lançamento excluído com sucesso')
        except:
            return ('Erro ao excluir registro.')
    
    def delete_investimentos(self, id):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(f"DELETE FROM Investimentos WHERE id = {id}")
            self.conexao.commit()
            return ('Lançamento excluído com sucesso')
        except:
            return ('Erro ao excluir registro.')

    # função para visualização da categorias
    def ver_cat_receita(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT Descricao FROM catReceitas")
        categorias = cursor.fetchall()
        return [categoria[0] for categoria in categorias]

    def ver_cat_despesa(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT Descricao FROM catDespesas")
        categorias = cursor.fetchall()
        return [categoria[0] for categoria in categorias]
    
    def ver_cat_investimento(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT Descricao FROM catInvestimentos")
        categorias = cursor.fetchall()
        return [categoria[0] for categoria in categorias]

    def obter_id_ultima_inserida(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT last_insert_rowid()")
        return cursor.fetchone()[0] if cursor else None

    # função pegar valor receita/despesa/investimento
    def ver_receita(self):
        lista_valores = []
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM Receitas")
        linha = cursor.fetchall()

        for l in linha:
            lista_valores.append(l)
        
        return lista_valores
    
    def ver_despesa(self):
        lista_valores = []
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM Despesas")
        linha = cursor.fetchall()

        for l in linha:
            lista_valores.append(l)
        
        return lista_valores
    
    def ver_despesa_essencial(self):
        lista_valores = []
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM Despesas WHERE Grupo = 'Essencial'")
        linha = cursor.fetchall()

        for l in linha:
            lista_valores.append(l)
        
        return lista_valores
    
    def ver_despesa_n_essencial(self):
        lista_valores = []
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM Despesas WHERE Grupo = 'Não Essencial'")
        linha = cursor.fetchall()

        for l in linha:
            lista_valores.append(l)

        return lista_valores
    
    def ver_investimento(self):
        lista_valores = []
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM Investimentos")
        linha = cursor.fetchall()

        for l in linha:
            lista_valores.append(l)
        
        return lista_valores
