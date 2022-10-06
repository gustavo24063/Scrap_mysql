import sqlite3 as sq

class CRUD:
    def __init__(self, nomeBanco, nomeTabela):
        self.nomeBanco = nomeBanco
        self.con = sq.connect(f'{nomeBanco}')
        self.cur = self.con.cursor()
        self.nomeTabela = nomeTabela
        #tabelas: clientes(nome, cpf, cep, nmr), produtos(nome, familia, codigobarra) e
        #vendas(data, cdgbarra, cpf_cliente, qntd, valor_unidade, valor total)

    #********************************************************************** CREATE **********************************************************************
    def createTable(self):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {self.nomeTabela}("
                         " ID_PRODUTO INTEGER PRIMARY KEY AUTOINCREMENT, "
                         " MERCADO TEXT,"
                         " CATEGORIA TEXT,"
                         " NOME_PRODUTO TEXT, "
                         " PESO_PRODUTO REAL, "
                         " PRECO_PRODUTO REAL,"
                         " IMAGEM_PRODUTO TEXT,"
                         " LINK_PRODUTO TEXT,"
                         " LINK_LOGO TEXT,"
                         " DATA_PRODUTO TEXT)")


    #********************************************************************** INSERT **********************************************************************
    def insert(self, mercado, categoria, nomeProduto, precoProduto, pesoProduto, imagemProduto, linkProduto, linkLogo, dataProduto, ):
        self.cur.execute(f' INSERT INTO {self.nomeTabela} (MERCADO, CATEGORIA, NOME_PRODUTO, PESO_PRODUTO, PRECO_PRODUTO, IMAGEM_PRODUTO, LINK_PRODUTO, LINK_LOGO, DATA_PRODUTO) '
                         f' VALUES ("{mercado}", "{categoria}", "{nomeProduto}", {pesoProduto}, {precoProduto}, "{imagemProduto}", "{linkProduto}", "{linkLogo}", "{dataProduto}")')
        self.con.commit()

    #********************************************************************** READ **********************************************************************

    def read(self):
        self.cur.execute(f"SELECT * FROM {self.nomeTabela}")
        for linha in self.cur.fetchall():
            print(f'{linha[0]} - {linha[1]} - {linha[2]} - {linha[3]} - {linha[4]} - {linha[5]} - {linha[6]} - {linha[7]} - {linha[8]} - {linha[9]}')

    #********************************************************************** UPDATE **********************************************************************
    def update(self, nomeProduto, id):
        self.cur.execute(
            f'UPDATE {self.nomeTabela} SET NOME_PRODUTO="{nomeProduto}" WHERE ID_PRODUTO = {id}'
        )
        self.con.commit()

   #********************************************************************** DELETE **********************************************************************
    def delete(self, id):
        self.cur.execute(
            f'DELETE FROM {self.nomeTabela} WHERE ID_PRODUTO = {id}'
        )
        self.con.commit()

    def save(self):
        self.con.commit()
        self.con.close()

