"""
Exercício 4.
Forneça um método recursivo para remover todos os elementos de uma pilha.
"""

class ArrayStack:
    def __init__(self):
        # guardo os itens dentro de uma lista normal mesmo
        self._data = []

    def is_empty(self):
        # checo se a pilha tá vazia olhando o tamanho da lista
        return len(self._data) == 0

    def push(self, item):
        # empilha no final da lista (que funciona como topo da pilha)
        self._data.append(item)

    def pop(self):
        # remove o último item, mas só se tiver algo lá
        if self.is_empty():
            raise IndexError("tentativa de pop em pilha vazia")
        return self._data.pop()

    def __str__(self):
        # só pra facilitar visualizar a pilha quando printar
        return f"{self._data}"

    def __len__(self):
        return len(self._data)


def recursive_clear(stack):
    """
    Função recursiva que esvazia a pilha inteira.
    A ideia é basicamente ir dando pop até ela ficar vazia,
    só que usando recursão no lugar de um while.
    """
    if not stack.is_empty():
        stack.pop()         # tira o item do topo
        recursive_clear(stack)  # chama de novo até acabar


# ============================
# Demonstração
# ============================

print("=== TESTANDO A FUNÇÃO RECURSIVA DE LIMPAR PILHA ===\n")

S = ArrayStack()

# colocando uns valores pra testar
for x in [10, 20, 30, 40, 50]:
    S.push(x)

print("Pilha antes:", S)
print("Tamanho antes:", len(S))

# chamando a função que limpa tudo
recursive_clear(S)

print("\nPilha depois de limpar:", S)
print("Tamanho depois:", len(S))
print("Está vazia?", S.is_empty())

print("\n" + "="*40)
print("Outro exemplo só pra confirmar")
print("="*40)

S2 = ArrayStack()
for letra in ["A", "B", "C", "D"]:
    S2.push(letra)

print("Antes:", S2)
recursive_clear(S2)
print("Depois:", S2)
