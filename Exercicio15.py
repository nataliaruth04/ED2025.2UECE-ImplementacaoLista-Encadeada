"""Exercício 15
Algoritmo recursivo para contar quantos nós existem
em uma lista encadeada simples.
"""

class Node:
    def __init__(self, valor):
        self.data = valor
        self.next = None


class LinkedList:
    def __init__(self):
        self._head = None
    
    def is_empty(self):
        return self._head is None
    
    def add(self, item):
        # adiciona no final da lista só pra facilitar os testes
        novo = Node(item)
        if self.is_empty():
            self._head = novo
        else:
            atual = self._head
            # anda até o último nó
            while atual.next is not None:
                atual = atual.next
            atual.next = novo
    
    def __str__(self):
        if self.is_empty():
            return "[]"
        elementos = []
        atual = self._head
        while atual:
            elementos.append(str(atual.data))
            atual = atual.next
        return "[" + " -> ".join(elementos) + "]"


def conta_nos_rec(node):
    # caso base: chegou no final (None), não tem mais nada pra contar
    if node is None:
        return 0
    # conta esse nó + continua contando o restante
    return 1 + conta_nos_rec(node.next)


def conta_nos(lista):
    # chama a recursão começando do primeiro nó
    return conta_nos_rec(lista._head)


# pequena demonstração
print("=" * 50)
print("CONTAGEM RECURSIVA DE NÓS NA LISTA")
print("=" * 50)

while True:
    entrada = input("\nDigite valores separados por espaço (ou 'sair'): ")

    if entrada.lower() == "sair":
        print("Encerrando...")
        break

    lista = LinkedList()

    if entrada.strip():
        for x in entrada.split():
            try:
                lista.add(int(x))
            except:
                lista.add(x)

    print(f"Lista: {lista}")
    print(f"Quantidade de nós: {conta_nos(lista)}")
    print("-" * 50)
