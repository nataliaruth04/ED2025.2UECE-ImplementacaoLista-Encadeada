
# Exercício 10 — calculadora aritmética de inteiros usando pilhas

from typing import List


class SimpleStack:

    def __init__(self) -> None:
        self._items: List[int | str] = []

    def push(self, v) -> None:
        self._items.append(v)

    def pop(self):
        return self._items.pop()

    def top(self):
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


# ---------- utilitários ----------
def is_op(tok: str) -> bool:
    return tok in "+-*/^"


def prec(op: str) -> int:
    # precedência: ^ mais forte, depois * /, depois + -
    if op == '^':
        return 3
    if op in '*/':
        return 2
    if op in '+-':
        return 1
    return 0


def apply_op(a: int, b: int, op: str) -> int:
    # aplica operador binário; comportamento de divisão: truncar toward zero
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError("divisão por zero")
        # em Python int(a / b) faz truncamento em direção a zero
        return int(a / b)
    if op == '^':
        return a ** b
    raise ValueError(f"operador desconhecido: {op}")


# ---------- tokenizador ----------
def tokenize(expr: str) -> List[str]:
    """
    Quebra a string em tokens: inteiros (podendo ter sinal) e operadores/parenteses.
    Tratamos o '-' como unário quando:
      - é o primeiro token, ou
      - vem logo após '(' ou outro operador.
    """
    s = expr.replace(" ", "")
    tokens: List[str] = []
    i = 0
    n = len(s)

    while i < n:
        ch = s[i]

        # números (sequência de dígitos possivelmente com sinal unário)
        if ch.isdigit():
            j = i
            while j < n and s[j].isdigit():
                j += 1
            tokens.append(s[i:j])
            i = j
            continue

        # sinal de menos pode ser parte do número (unário)
        if ch == '-':
            # se é unário?
            if not tokens or tokens[-1] in "(+-*/^":
                # é parte do número: pega os dígitos após o '-'
                j = i + 1
                if j < n and s[j].isdigit():
                    k = j
                    while k < n and s[k].isdigit():
                        k += 1
                    tokens.append(s[i:k])  # ex: "-5"
                    i = k
                    continue
                else:
                    # se não tem dígito depois, isso é inválido (ex: "-(")
                    # vamos tratar '-' isolado (vai gerar erro depois)
                    tokens.append('-')
                    i += 1
                    continue
            else:
                tokens.append('-')
                i += 1
                continue

        # parênteses e operadores simples
        if ch in "+*/^()":
            tokens.append(ch)
            i += 1
            continue

        # caractere inválido
        raise ValueError(f"caractere inválido na expressão: '{ch}'")

    return tokens


# ---------- conversão infixa  ----------
def infix_to_postfix(tokens: List[str]) -> List[str]:
    """
    Usa uma pilha de operadores. Resultado é lista de tokens em notação pós-fixa.
    Observação: tokens contendo '-5' já são números no tokenizador.
    """
    out: List[str] = []
    ops = SimpleStack()

    for tok in tokens:
        if tok.lstrip('-').isdigit():  # número (pode ser negativo)
            out.append(tok)
        elif tok == '(':
            ops.push(tok)
        elif tok == ')':
            # desempilha até '('
            while not ops.is_empty() and ops.top() != '(':
                out.append(ops.pop())
            if ops.is_empty():
                raise ValueError("parênteses desbalanceados: falta '('")
            ops.pop()  # remove '('
        elif is_op(tok):
            # operador: desempilha enquanto topo tem operador de maior/equal precedência
            # nota: ^ é geralmente associativo à direita; vamos implementar isso:
            while (not ops.is_empty() and is_op(str(ops.top())) and
                   ((prec(str(ops.top())) > prec(tok)) or
                    (prec(str(ops.top())) == prec(tok) and tok != '^'))):
                out.append(ops.pop())
            ops.push(tok)
        else:
            raise ValueError(f"token inesperado: {tok}")

    while not ops.is_empty():
        top = ops.pop()
        if top in '()':
            raise ValueError("parênteses desbalanceados")
        out.append(top)

    return out


# ---------- avaliação de pós-fixa ----------
def eval_postfix(postfix: List[str]) -> int:
    st = SimpleStack()

    for tok in postfix:
        if tok.lstrip('-').isdigit():
            st.push(int(tok))
        elif is_op(tok):
            if len(st) < 2:
                raise ValueError("expressão inválida: operando faltando")
            b = st.pop()
            a = st.pop()
            res = apply_op(a, b, tok)
            st.push(res)
        else:
            raise ValueError(f"token inválido na pós-fixa: {tok}")

    if len(st) != 1:
        raise ValueError("expressão inválida: sobrou valor na pilha")
    return st.pop()


# ---------- função principal que junta tudo ----------
def calcular(expressao: str) -> tuple[int, List[str]]:
    """
    Recebe uma expressão infixa (string), retorna (resultado_int, postfix_tokens).
    Lança exceções se a expressão for inválida.
    """
    if not expressao or not expressao.strip():
        raise ValueError("expressão vazia")

    tokens = tokenize(expressao)
    postfix = infix_to_postfix(tokens)
    resultado = eval_postfix(postfix)
    return resultado, postfix


# ---------- modo interativo / exemplos ----------
if __name__ == "__main__":
    exemplos = [
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "-5 + 3 * (2 + 1)",
        "10 / 3",         # deve truncar para 3 -> int(10/3) = 3
        "2 ^ 3 ^ 2",      # 2^(3^2) = 2^9 = 512 (associação à direita)
        " ( 7 - 3 ) * -2"
    ]

    print(">>> TESTES RÁPIDOS")
    for ex in exemplos:
        try:
            res, pf = calcular(ex)
            print(f"{ex}  -> pós-fixa: {' '.join(pf)}  => {res}")
        except Exception as e:
            print(f"{ex}  -> erro: {e}")

    print("\nDigite expressões para calcular. 'sair' para terminar.")
    while True:
        linha = input(">>> ").strip()
        if linha.lower() == "sair":
            break
        if not linha:
            continue
        try:
            valor, posf = calcular(linha)
            print("Pós-fixa:", " ".join(posf))
            print("Resultado:", valor)
        except Exception as e:
            print("Erro ao calcular:", e)
