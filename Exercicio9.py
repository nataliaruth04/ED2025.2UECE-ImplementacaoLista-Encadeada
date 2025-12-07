"""
Exercício 9.
Escreva um programa para converter uma expressão aritmética na forma prefixada
para as formas infixa e pós-fixada equivalentes.
"""

from typing import List


class SimpleStack:
    """Pilha para manipular strings"""
    def __init__(self) -> None:
        self._items: List[str] = []

    def push(self, x: str) -> None:
        # empilha sem drama
        self._items.append(x)

    def pop(self) -> str:
        # assume que o chamador checou is_empty; se não, lança IndexError
        return self._items.pop()

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __repr__(self) -> str:
        return f"Stack({self._items})"


def _is_operator(token: str) -> bool:
    """Define quais símbolos consideramos operadores (simples)."""
    return token in {"+", "-", "*", "/", "^"}


def _tokenize(expr: str) -> List[str]:
    """
    Se a expressão vier com espaços, usa os tokens
    Caso contrário, quebra caractere a caractere
    """
    expr = expr.strip()
    if not expr:
        return []
    if " " in expr:
        # já está tokenizada pelo usuário
        return expr.split()
    # sem espaços: cada caractere é um token 
    return list(expr)


def prefix_to_infix(prefix: str) -> str:
    """
    Converte notação prefixada para infixa.
    Ex.: "*+ABC"  -> "((A+B)*C)"
          "+ A B" -> "(A+B)"
    """
    tokens = _tokenize(prefix)
    if not tokens:
        raise ValueError("Expressão vazia")

    st = SimpleStack()

    # lemos da direita para a esquerda
    for tok in reversed(tokens):
        if _is_operator(tok):
            # operador: precisa ter pelo menos dois operandos na pilha
            if st.is_empty():
                raise ValueError("Expressão prefixada inválida (operandos insuficientes)")
            op1 = st.pop()
            if st.is_empty():
                raise ValueError("Expressão prefixada inválida (operandos insuficientes)")
            op2 = st.pop()
            # monto a expressão infixa com parênteses para preservar precedência
            new_expr = f"({op1}{tok}{op2})"
            st.push(new_expr)
        else:
            # operando: só empilha (pode ser número, variável, etc.)
            st.push(tok)

    if st.is_empty():
        raise ValueError("Erro interno: pilha vazia após processamento")
    result = st.pop()
    if not st.is_empty():
        # se sobrou coisa na pilha, a expressão de entrada pode ser inválida (tokens a mais)
        raise ValueError("Expressão prefixada inválida (sobraram tokens)")
    return result


def prefix_to_postfix(prefix: str) -> str:
    """
    Converte notação prefixada para pos-fixada (postfix).
    Ex.: "*+ABC" -> "AB+C*"
    """
    tokens = _tokenize(prefix)
    if not tokens:
        raise ValueError("Expressão vazia")

    st = SimpleStack()

    for tok in reversed(tokens):
        if _is_operator(tok):
            if st.is_empty():
                raise ValueError("Expressão prefixada inválida (operandos insuficientes)")
            op1 = st.pop()
            if st.is_empty():
                raise ValueError("Expressão prefixada inválida (operandos insuficientes)")
            op2 = st.pop()
            new_expr = f"{op1}{op2}{tok}"
            st.push(new_expr)
        else:
            st.push(tok)

    if st.is_empty():
        raise ValueError("Erro interno: pilha vazia após processamento")
    result = st.pop()
    if not st.is_empty():
        raise ValueError("Expressão prefixada inválida (sobraram tokens)")
    return result


# --- exemplo simples de uso ---
if __name__ == "__main__":
    print("=" * 60)
    print("CONVERSOR: prefixada -> infixa / pos-fixada")
    print("Digite 'sair' para encerrar.")
    print("=" * 60)

    while True:
        s = input("\nExpressão prefixada: ").strip()
        if s.lower() == "sair":
            print("Falou! Encerrando.")
            break
        if not s:
            print("Ops — expressão vazia. Tente de novo.")
            continue

        try:
            inf = prefix_to_infix(s)
            pos = prefix_to_postfix(s)
            # Mostramos o que foi pedido
            print(f"  Prefixada : {s}")
            print(f"  Infixa    : {inf}")
            print(f"  Pos-fixada: {pos}")
        except Exception as e:
            print(f"  Erro ao converter: {e}")
