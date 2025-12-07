"""
Exercício 10.
Implemente uma calculadora aritmética de inteiros usando pilhas.
"""

from typing import List, Union, Optional


class Stack:
    
    def __init__(self) -> None:
        self._items: List[object] = []

    def push(self, x: object) -> None:
        self._items.append(x)

    def pop(self) -> object:
        return self._items.pop()

    def top(self) -> object:
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


def is_operator(tok: str) -> bool:
    return tok in {"+", "-", "*", "/", "^"}


def precedence(op: str) -> int:
    # prioridade: ^ > * / > + -
    if op == "^":
        return 3
    if op in ("*", "/"):
        return 2
    if op in ("+", "-"):
        return 1
    return 0


def tokenize(expression: str) -> List[str]:
    """Separa a expressão em tokens (números, operadores e parênteses).
    Lida com números multi-dígito e sinais de menos unários.
    Exemplo: '-3 + (12 * 5)' -> ['-3', '+', '(', '12', '*', '5', ')']
    """
    expr = expression.replace(" ", "")
    tokens: List[str] = []
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]

        if ch.isdigit():
            # le número completo
            j = i
            while j < n and expr[j].isdigit():
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue

        if ch in "+*/^()":
            tokens.append(ch)
            i += 1
            continue

        if ch == "-":
            # pode ser operador binário ou sinal unário
            # se é começo da string ou antecedido por outro operador/abertura, é unário
            if i == 0 or expr[i - 1] in "+-*/^(":
                # ler número negativo (se houver dígitos depois)
                j = i + 1
                if j < n and expr[j].isdigit():
                    while j < n and expr[j].isdigit():
                        j += 1
                    tokens.append(expr[i:j])  # inclui o '-'
                    i = j
                else:
                    # caso estranho: apenas '-' sem número -> tratar como operador
                    tokens.append("-")
                    i += 1
            else:
                tokens.append("-")
                i += 1
            continue

        raise ValueError(f"Token inválido na expressão: '{ch}'")

    return tokens


def infix_to_postfix(tokens: List[str]) -> List[str]:
    """Shunting-yard: converte lista de tokens infixa para pós-fixa."""
    out: List[str] = []
    opstack = Stack()

    for tok in tokens:
        if tok.lstrip("-").isdigit():  # número (pode ter sinal -)
            out.append(tok)
        elif tok == "(":
            opstack.push(tok)
        elif tok == ")":
            # desempilha até '('
            while not opstack.is_empty() and opstack.top() != "(":
                out.append(opstack.pop())  # type: ignore
            if opstack.is_empty():
                raise ValueError("Parênteses desbalanceados (faltou '(')")
            opstack.pop()  # remove '('
        elif is_operator(tok):
            # operadores com associatividade: '^' é **right-associative**
            while (not opstack.is_empty() and is_operator(opstack.top())):
                top_op = opstack.top()  # type: ignore
                if (precedence(top_op) > precedence(tok)
                        or (precedence(top_op) == precedence(tok) and tok != "^")):
                    out.append(opstack.pop())  # type: ignore
                else:
                    break
            opstack.push(tok)
        else:
            raise ValueError(f"Token desconhecido: {tok}")

    while not opstack.is_empty():
        top = opstack.pop()
        if top in ("(", ")"):
            raise ValueError("Parênteses desbalanceados")
        out.append(top)  # type: ignore

    return out


def eval_postfix(postfix: List[str]) -> int:
    """Avalia expressão em pós-fixa retornando inteiro."""
    st = Stack()

    for tok in postfix:
        if tok.lstrip("-").isdigit():
            st.push(int(tok))
        elif is_operator(tok):
            if len(st) < 2:
                raise ValueError("Expressão inválida (operando faltando)")
            b = int(st.pop())
            a = int(st.pop())

            if tok == "+":
                st.push(a + b)
            elif tok == "-":
                st.push(a - b)
            elif tok == "*":
                st.push(a * b)
            elif tok == "/":
                if b == 0:
                    raise ZeroDivisionError("Divisão por zero")
                st.push(int(a / b))
            elif tok == "^":
                st.push(a ** b)
        else:
            raise ValueError(f"Token inesperado na pós-fixa: {tok}")

    if len(st) != 1:
        raise ValueError("Expressão pós-fixa inválida (resultado não único)")

    return int(st.pop())


def calculate(expression: str) -> (int, List[str]):
    """Converte a expressão infixa para pós-fixa e avalia, retornando (resultado, posfixa)."""
    tokens = tokenize(expression)
    postfix = infix_to_postfix(tokens)
    result = eval_postfix(postfix)
    return result, postfix


# -------------------------
# Exemplo 
# -------------------------
if __name__ == "__main__":
    print("Calculadora inteira (digite 'sair' pra encerrar).")
    print("Suporta + - * / ^ e parênteses. Números inteiros (ex: -3, 42).")
    print("-" * 60)

    while True:
        try:
            line = input("expr> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaindo...")
            break

        if not line:
            continue
        if line.lower() in ("sair", "exit", "quit"):
            print("Tchau!")
            break

        try:
            value, postfix = calculate(line)
            print("Pós-fixa:", " ".join(postfix))
            print("Resultado:", value)
        except ZeroDivisionError as zde:
            print("Erro: divisão por zero.")
        except ValueError as ve:
            print("Erro: expressão inválida ->", ve)
        except Exception as e:
            print("Erro inesperado:", e)

        print("-" * 60)
