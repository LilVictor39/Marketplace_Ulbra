from abc import ABC, abstractmethod

# Classe Observável (Marketplace)
class Marketplace:
    def __init__(self):
        self.produtos = []
        self.pedidos = []
        self.vendedores = []

    def adicionar_vendedor(self, vendedor):
        """Adiciona um vendedor à lista de observadores"""
        self.vendedores.append(vendedor)

    def adicionar_produto(self, produto):
        """Adiciona um produto ao marketplace e informa os vendedores"""
        self.produtos.append(produto)
        self.notificar_vendedores(f"Novo produto adicionado: {produto['nome']} - R${produto['preco']:.2f}")

    def remover_produto(self, produto_nome):
        """Remove um produto do marketplace e informa os vendedores"""
        self.produtos = [p for p in self.produtos if p["nome"] != produto_nome]
        self.notificar_vendedores(f"Produto removido: {produto_nome}")

    def realizar_pedido(self, produto_nome, comprador):
        """Registra um pedido e informa os vendedores"""
        produto = next((p for p in self.produtos if p["nome"] == produto_nome), None)
        if produto:
            pedido = {"produto": produto_nome, "comprador": comprador}
            self.pedidos.append(pedido)
            self.notificar_vendedores(f"Novo pedido realizado para: {produto_nome} por {comprador}")
        else:
            print(f"Produto '{produto_nome}' não encontrado.")

    def cancelar_pedido(self, produto_nome, comprador):
        """Cancela um pedido existente"""
        self.pedidos = [p for p in self.pedidos if not (p["produto"] == produto_nome and p["comprador"] == comprador)]
        self.notificar_vendedores(f"Pedido cancelado: {produto_nome} por {comprador}")

    def listar_pedidos(self):
        """Lista todos os pedidos realizados"""
        if not self.pedidos:
            print("Nenhum pedido realizado ainda.")
            return
        for pedido in self.pedidos:
            print(f"Pedido: {pedido['produto']} - Comprador: {pedido['comprador']}")

    def consultar_pedidos_comprador(self, comprador):
        """Lista os pedidos de um comprador específico"""
        pedidos = [p for p in self.pedidos if p["comprador"] == comprador]
        if not pedidos:
            print(f"{comprador} não realizou pedidos ainda.")
        else:
            print(f"Pedidos de {comprador}:")
            for pedido in pedidos:
                print(f" - {pedido['produto']}")

    def listar_produtos(self):
        """Lista os produtos disponíveis"""
        if not self.produtos:
            print("Nenhum produto disponível no momento.")
        else:
            print("Produtos disponíveis:")
            for p in self.produtos:
                print(f" - {p['nome']} (R${p['preco']:.2f})")

    def iniciar_chat(self, comprador, vendedor):
        """Simula um chat entre um comprador e um vendedor"""
        print(f"[Chat iniciado entre {comprador} e {vendedor.nome}]")
        while True:
            mensagem = input(f"{comprador}: ")
            if mensagem.lower() == "sair":
                print("Chat encerrado.")
                break
            vendedor.responder_chat(mensagem)

    def notificar_vendedores(self, mensagem):
        """Notifica todos os vendedores sobre um evento"""
        for vendedor in self.vendedores:
            vendedor.atualizar(mensagem)


# Interface Observer (Vendedor)
class Vendedor(ABC):
    @abstractmethod
    def atualizar(self, mensagem):
        pass

    @abstractmethod
    def responder_chat(self, mensagem):
        pass


# Implementação de um Vendedor
class VendedorConcreto(Vendedor):
    def __init__(self, nome):
        self.nome = nome

    def atualizar(self, mensagem):
        """Recebe notificações do marketplace"""
        print(f"[{self.nome} recebeu notificação]: {mensagem}")

    def responder_chat(self, mensagem):
        """Responde ao chat do comprador"""
        print(f"[{self.nome}]: Entendi sua mensagem. Podemos te ajudar com algo mais?")


# Teste do Sistema
if __name__ == "__main__":
    # Criando marketplace
    marketplace = Marketplace()

    # Criando vendedores
    vendedor1 = VendedorConcreto("Loja A")
    vendedor2 = VendedorConcreto("Loja B")

    # Registrando vendedores no Marketplace
    marketplace.adicionar_vendedor(vendedor1)
    marketplace.adicionar_vendedor(vendedor2)

    # Adicionando produtos
    marketplace.adicionar_produto({"nome": "Notebook", "preco": 3500})
    marketplace.adicionar_produto({"nome": "Smartphone", "preco": 2000})
    marketplace.adicionar_produto({"nome": "Fone Bluetooth", "preco": 250})

    # Listando produtos
    marketplace.listar_produtos()

    # Realizando pedidos
    marketplace.realizar_pedido("Notebook", "Cliente João")
    marketplace.realizar_pedido("Smartphone", "Cliente Maria")

    # Listando pedidos
    marketplace.listar_pedidos()

    # Consultando pedidos de um comprador específico
    marketplace.consultar_pedidos_comprador("Cliente João")

    # Cancelando um pedido
    marketplace.cancelar_pedido("Notebook", "Cliente João")
    marketplace.listar_pedidos()

    # Removendo um produto
    marketplace.remover_produto("Fone Bluetooth")
    marketplace.listar_produtos()

    # Simulando um chat entre um comprador e um vendedor
    marketplace.iniciar_chat("Cliente João", vendedor1)
