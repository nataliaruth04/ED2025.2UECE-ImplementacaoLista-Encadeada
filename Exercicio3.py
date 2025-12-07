"""
Exercício 3.
Implementar uma função transfer(S, T) que mova todos os elementos da pilha S para T.
A ideia é que o topo de S seja o primeiro elemento inserido em T, e o elemento que está
no fundo de S acabe virando o topo de T. Ou seja: a função "inverte" a pilha enquanto
transfere.
"""

class ArrayStack:
    """Pilha usando array dinâmico. Modelo padrão LIFO."""

    def __init__(self, capacity=10):
        # criando o array interno com a capacidade inicial
        self._data = [None] * capacity
        self._size = 0
        self._capacity = capacity

    def __len__(self):
        return self._size

    def is_empty(self):
        # só checa se não tem nada dentro
        return self._size == 0

    def push(self, item):
        # se não tiver espaço, dobra o tamanho do array
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = item
        self._size += 1

    def pop(self):
        # remover do topo, o mais padrão possível
        if self.is_empty():
            raise IndexError("pop de pilha vazia")
        elem = self._data[self._size - 1]
        self._data[self._size - 1] = None
        self._size -= 1

        # diminuindo o array quando ele fica "espaçoso demais"
        if 0 < self._size < self._capacity // 4:
            self._resize(self._capacity // 2)

        return elem

    def top(self):
        # só olha o topo sem tirar
        if self.is_empty():
            raise IndexError("top de pilha vazia")
        return self._data[self._size - 1]

    def _resize(self, new_cap):
        # só copia tudo para um array maior/menor
        novo = [None] * new_cap
        for i in range(self._size):
            novo[i] = self._data[i]
        self._data = novo
        self._capacity = new_cap

    def get_elements(self):
        # devolve os elementos numa lista (base -> topo)
        return [self._data[i] for i in range(self._size)]

    def __str__(self):
        if self.is_empty():
            return "[]"
        return f"[{', '.join(str(self._data[i]) for i in range(self._size))}] <- topo"


# ---------------- FUNÇÃO TRANSFER ---------------- #

def transfer(S, T):
    """
    Transfere tudo da pilha S para a pilha T.

    Como o pop() de S pega sempre o topo, e T recebe via push(),
    a pilha T acaba ficando na "ordem invertida" da original.

    Depois da função:
        - S fica vazia
        - T guarda os elementos invertidos
    """
    # aqui é literalmente só ir popando a S e jogando na T
    while not S.is_empty():
        item = S.pop()
        T.push(item)


# ---------------- DEMONSTRAÇÃO ---------------- #

print("=" * 60)
print("DEMONSTRAÇÃO DA TRANSFERÊNCIA ENTRE PILHAS")
print("=" * 60)

# montando uma pilha S com alguns valores
S = ArrayStack()
valores = [10, 20, 30, 40, 50]
print("\nPreenchendo pilha S:")
for v in valores:
    S.push(v)
    print(f" push({v})")

print("\nEstado de S antes da transferência:")
print(" S =", S)

# pilha destino T
T = ArrayStack()
print("\nT começa vazia:", T)

# aplicando transfer
print("\nExecutando transfer(S, T)...")
transfer(S, T)

print("\nDepois da transferência:")
print(" S =", S)   # deve estar vazia
print(" T =", T)   # deve conter a ordem invertida

print("\nBase -> topo de T:", T.get_elements())
print("=" * 60)


# Exemplo extra só pra mostrar que funciona com strings também
print("\nOutro exemplo com palavras:")
S2 = ArrayStack()
for w in ["codar", "pilha", "estrutura", "dados"]:
    S2.push(w)

T2 = ArrayStack()
transfer(S2, T2)

print(" T2 =", T2)
print("=" * 60)
