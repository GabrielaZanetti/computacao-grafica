"""Demonstração da biblioteca do EI 01.

Execute com:
python3 EI/exemplo_ei01.py
"""

try:
    from EI.ei01 import (
        Ponto2D,
        Ponto3D,
        comprimento_segmento_2d,
        comprimento_segmento_3d,
        multiplicar_matriz_2x2,
        multiplicar_matriz_3x3,
        multiplicar_matriz_4x4,
        ponto_interseccao_segmentos,
        segmentos_intersectam,
    )
except ModuleNotFoundError:
    from ei01 import (
        Ponto2D,
        Ponto3D,
        comprimento_segmento_2d,
        comprimento_segmento_3d,
        multiplicar_matriz_2x2,
        multiplicar_matriz_3x3,
        multiplicar_matriz_4x4,
        ponto_interseccao_segmentos,
        segmentos_intersectam,
    )


def main() -> None:
    print("=== EI 01 - Biblioteca Matemática ===")

    p1 = Ponto2D(0, 0)
    p2 = Ponto2D(3, 4)
    print(f"Ponto2D: {p1} e {p2}")
    print(f"Comprimento 2D: {comprimento_segmento_2d(p1, p2):.2f}")

    p3 = Ponto3D(1, 2, 3)
    p4 = Ponto3D(4, 6, 3)
    print(f"Ponto3D: {p3} e {p4}")
    print(f"Comprimento 3D: {comprimento_segmento_3d(p3, p4):.2f}")

    a2 = [[1, 2], [3, 4]]
    b2 = [[2, 0], [1, 2]]
    print(f"Multiplicação 2x2: {multiplicar_matriz_2x2(a2, b2)}")

    a3 = [[1, 0, 2], [0, 1, 3], [4, 0, 1]]
    b3 = [[2, 1, 0], [1, 0, 2], [3, 4, 1]]
    print(f"Multiplicação 3x3: {multiplicar_matriz_3x3(a3, b3)}")

    a4 = [
        [1, 0, 0, 1],
        [0, 1, 0, 2],
        [0, 0, 1, 3],
        [0, 0, 0, 1],
    ]
    b4 = [
        [2, 0, 0, 0],
        [0, 2, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 1],
    ]
    print(f"Multiplicação 4x4: {multiplicar_matriz_4x4(a4, b4)}")

    s1_a = Ponto2D(0, 0)
    s1_b = Ponto2D(4, 4)
    s2_a = Ponto2D(0, 4)
    s2_b = Ponto2D(4, 0)

    intersectam = segmentos_intersectam(s1_a, s1_b, s2_a, s2_b)
    ponto = ponto_interseccao_segmentos(s1_a, s1_b, s2_a, s2_b)

    print(f"Segmentos intersectam? {intersectam}")
    print(f"Ponto de interseção: {ponto}")


if __name__ == "__main__":
    main()
