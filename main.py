from models.produto import Produto, BoloDeFesta, DoceDeFesta
from models.pedido import Pedido
from models.estoque import Estoque

cardapio = [
        Produto("Bolo de chocolate", 90, "Bolo"),
        Produto("Torta cookie", 15, "Torta"),
        Produto("Bolo gelado", 10, "Bolo")
]

for produto in cardapio:
    produto.exibir_info()


cliente01 = Pedido("Gessika Darico")
cliente01.adicionar_item(cardapio[0])
cliente01.adicionar_item(cardapio[1])
cliente01.adicionar_item(cardapio[2])

cliente01.salvar_pedido()

def exibir_pedidos_salvos():
    try:
        with open("pedidos.txt", "r", encoding="utf-8") as f:
            for indice, linha in enumerate(f, start=1):
                print(f"{indice}: {linha.strip()}")
    except FileNotFoundError:
        print("Nenhum pedido salvo ainda.")


estoque = Estoque("Brigadeiro")
estoque.adicionar(-10)  
estoque.adicionar(100) # - adiciona quantidades
estoque.remover(200)   # - remove quantidades
estoque.remover(30)
estoque.set_quantidade(10)  # - muda certeirtamente a quantidade
estoque.set_produto("BEIJINHO")  # - muda o nome do produto  
print(f"{estoque.get_produto()}: {estoque.get_quantidade()} unidades")


exibir_pedidos_salvos()