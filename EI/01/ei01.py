"""EI 01 - Biblioteca matemática básica para computação gráfica.

Conteúdo:
- Ponto2D e Ponto3D
- Multiplicação de matrizes 2x2, 3x3 e 4x4
- Comprimento de segmentos de reta (2D e 3D)
- Verificação de interseção entre dois segmentos de reta em 2D
"""

from dataclasses import dataclass
from math import isclose, sqrt
from typing import List, Optional

EPSILON = 1e-9


@dataclass(frozen=True)
class Ponto2D:
    x: float
    y: float


@dataclass(frozen=True)
class Ponto3D:
    x: float
    y: float
    z: float


def _validar_matriz_quadrada(matriz: List[List[float]], ordem: int) -> None:
    if len(matriz) != ordem or any(len(linha) != ordem for linha in matriz):
        raise ValueError(f"A matriz deve ser {ordem}x{ordem}.")


def _multiplicar_matrizes(a: List[List[float]], b: List[List[float]], ordem: int) -> List[List[float]]:
    _validar_matriz_quadrada(a, ordem)
    _validar_matriz_quadrada(b, ordem)

    resultado = [[0.0 for _ in range(ordem)] for _ in range(ordem)]
    for i in range(ordem):
        for j in range(ordem):
            resultado[i][j] = sum(a[i][k] * b[k][j] for k in range(ordem))
    return resultado


def multiplicar_matriz_2x2(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    return _multiplicar_matrizes(a, b, 2)


def multiplicar_matriz_3x3(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    return _multiplicar_matrizes(a, b, 3)


def multiplicar_matriz_4x4(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    return _multiplicar_matrizes(a, b, 4)


def comprimento_segmento_2d(p1: Ponto2D, p2: Ponto2D) -> float:
    return sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)


def comprimento_segmento_3d(p1: Ponto3D, p2: Ponto3D) -> float:
    return sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 + (p2.z - p1.z) ** 2)


def _orientacao(a: Ponto2D, b: Ponto2D, c: Ponto2D) -> int:
    valor = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)

    if isclose(valor, 0.0, abs_tol=EPSILON):
        return 0
    return 1 if valor > 0 else 2


def _ponto_no_segmento(a: Ponto2D, b: Ponto2D, p: Ponto2D) -> bool:
    return (
        min(a.x, b.x) - EPSILON <= p.x <= max(a.x, b.x) + EPSILON
        and min(a.y, b.y) - EPSILON <= p.y <= max(a.y, b.y) + EPSILON
    )


def segmentos_intersectam(p1: Ponto2D, p2: Ponto2D, p3: Ponto2D, p4: Ponto2D) -> bool:
    o1 = _orientacao(p1, p2, p3)
    o2 = _orientacao(p1, p2, p4)
    o3 = _orientacao(p3, p4, p1)
    o4 = _orientacao(p3, p4, p2)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and _ponto_no_segmento(p1, p2, p3):
        return True
    if o2 == 0 and _ponto_no_segmento(p1, p2, p4):
        return True
    if o3 == 0 and _ponto_no_segmento(p3, p4, p1):
        return True
    if o4 == 0 and _ponto_no_segmento(p3, p4, p2):
        return True

    return False


def ponto_interseccao_segmentos(
    p1: Ponto2D,
    p2: Ponto2D,
    p3: Ponto2D,
    p4: Ponto2D,
) -> Optional[Ponto2D]:
    if not segmentos_intersectam(p1, p2, p3, p4):
        return None

    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y
    x4, y4 = p4.x, p4.y

    denominador = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if isclose(denominador, 0.0, abs_tol=EPSILON):
        for ponto in (p1, p2, p3, p4):
            if _ponto_no_segmento(p1, p2, ponto) and _ponto_no_segmento(p3, p4, ponto):
                return ponto
        return None

    numerador_x = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    numerador_y = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)

    return Ponto2D(numerador_x / denominador, numerador_y / denominador)


__all__ = [
    "Ponto2D",
    "Ponto3D",
    "multiplicar_matriz_2x2",
    "multiplicar_matriz_3x3",
    "multiplicar_matriz_4x4",
    "comprimento_segmento_2d",
    "comprimento_segmento_3d",
    "segmentos_intersectam",
    "ponto_interseccao_segmentos",
]
