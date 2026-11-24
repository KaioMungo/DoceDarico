class Estoque:
    def __init__(self, produto):
        self.__produto = produto
        self.__quantidade = 0

    def adicionar(self, quantidade):
        if quantidade > 0:
            self.__quantidade += quantidade
        else:
            print("Quantidade invalida! Tente um valor positivo")

    def remover(self, quantidade):
        if quantidade > self.__quantidade:
            print("Não é possivel remover mais do que existe em estoque")
        else:
            self.__quantidade -= quantidade

    def get_quantidade(self):
        return self.__quantidade
    
    def get_produto(self):
        return self.__produto
    
    def set_quantidade(self, quantidade):
        if quantidade >=0 :
            self.__quantidade = quantidade
        else:
            print("Quantidade invalida!")

    def set_produto(self, produto):
        if produto == "":
            print("Nome de produto invalido!")
        else:
            self.__produto = produto