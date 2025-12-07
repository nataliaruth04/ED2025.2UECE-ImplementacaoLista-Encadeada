"""
Exercício 5.
Implementar uma função que inverte uma lista usando uma pilha.
A ideia é jogar cada elemento na pilha (onde a ordem se "inverte" por causa do LIFO)
e depois colocar tudo de volta na lista, porém agora já no sentido contrário.
"""

class ArrayStack:
    
    def __init__(self):
        self._data = []  # lista que vai guardar os elementos
    
    def is_empty(self):
        return len(self._data) == 0
    
    def push(self, item):
        # adiciona no final da lista, que representa o topo da pilha
        self._data.append(item)
    
    def pop(self):
        # remove sempre do final (topo)
        if self.is_empty():
            raise IndexError("não dá pra remover de uma pilha vazia")
        return self._data.pop()


def reverse_list(lst):
    """
    Inverte os elementos de uma lista usando uma pilha.
    A lógica é: empilhar tudo, depois desempilhar devolvendo para a lista.
    """
    stack = ArrayStack()

    # Primeiro empilho todos os elementos
    for element in lst:
        stack.push(element)

    # Agora vou desempilhando e sobrescrevendo a lista
    for i in range(len(lst)):
        lst[i] = stack.pop()


# ===============================
# Testes para ver se funciona
# ===============================

print("FUNÇÃO PARA INVERTER LISTA USANDO PILHA\n")
print("=" * 50)

# teste 1: lista de números
lista1 = [1, 2, 3, 4, 5]
print(f"Lista original: {lista1}")
reverse_list(lista1)
print(f"Lista invertida: {lista1}")

print("\n" + "=" * 50)

# teste 2: strings
lista2 = ["Python", "Java", "C++", "JavaScript"]
print(f"Lista original: {lista2}")
reverse_list(lista2)
print(f"Lista invertida: {lista2}")

print("\n" + "=" * 50)

# teste 3: caracteres
lista3 = list("ESTRUTURA")
print(f"Lista original: {lista3}")
reverse_list(lista3)
print(f"Lista invertida: {lista3}")
print(f"String invertida: {''.join(lista3)}")

print("\n" + "=" * 50)

# teste 4: lista vazia
lista4 = []
print(f"Lista vazia: {lista4}")
reverse_list(lista4)
print(f"Depois da inversão: {lista4}")

print("\n" + "=" * 50)

# teste 5: lista com um elemento
lista5 = [42]
print(f"Lista com 1 elemento: {lista5}")
reverse_list(lista5)
print(f"Depois da inversão: {lista5}")

print("\n" + "=" * 50)
