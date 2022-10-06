import mysql.connector
class CRUD:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='findmarket',
        )
        self.cursor = self.conexao.cursor()
    def insert(self, mercado, categoria, nome_produto, peso_produto, preco_produto, imagem_produto, link_produto, link_logo, data_produto):
        # CRUD
        comando = f'INSERT INTO produtos (mercado, categoria, nome_produto, peso_produto, preco_produto, imagem_produto, link_produto, link_logo, data_produto) VALUES ("{mercado}", "{categoria}", "{nome_produto}", {peso_produto}, {preco_produto}, "{imagem_produto}", "{link_produto}", "{link_logo}", "{data_produto}")'
        self.cursor.execute(comando)
        self.conexao.commit() #confirmar edição do banco
        #resultado = self.cursor.fetchall() #ler o banco de dados
    
    def finaliza(self):
        self.cursor.close()
        self.conexao.close()