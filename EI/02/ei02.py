
"""
EI 02 - Implementação de Transformações 2D

Este script implementa transformações geométricas 2D (translação, escala,
rotação) usando coordenadas homogêneas e matrizes 3x3. Inclui uma demonstração
visual usando matplotlib que mostra o objeto antes e depois da transformação.

Resumo das implementações:
- Translação: matriz T(tx,ty)
- Escala: matriz S(sx,sy) aplicada sobre a origem ou sobre um ponto de referência
- Rotação: matriz R(theta) aplicada sobre a origem ou sobre um ponto de referência

Base matemática:
- Usamos coordenadas homogêneas (x, y, 1) e matrizes 3x3 para representar
  transformações afins. Para aplicar uma transformação a pontos representados
  como vetores linha p = [x, y, 1], calculamos p' = p @ M.T.

Entregáveis e respostas (resumido):
- Como cada transformação foi implementada?
  Usando matrizes 3x3 em coordenadas homogêneas; composições para pivot.
- Qual foi a base matemática utilizada?
  Álgebra linear: multiplicação matricial e coordenadas homogêneas.
- Como as matrizes foram aplicadas nas transformações?
  Pontos (Nx2) -> homogenizados -> multiplicados por M.T -> convertidos de volta.
- Dificuldades e soluções:
  Dependência de bibliotecas (`numpy`, `matplotlib`). Se faltarem, instalar via
  `pip install -r requirements.txt`.

Uso: execute o arquivo e verá janelas com as visualizações.
"""

from __future__ import annotations

import math
from typing import Tuple

import numpy as np

try:
	import matplotlib.pyplot as plt
except Exception:
	raise


def to_homogeneous(points: np.ndarray) -> np.ndarray:
	"""Converte um array Nx2 em coordenadas homogêneas Nx3."""
	points = np.asarray(points, dtype=float)
	ones = np.ones((points.shape[0], 1), dtype=float)
	return np.hstack([points, ones])


def from_homogeneous(points_h: np.ndarray) -> np.ndarray:
	"""Converte um array homogêneo Nx3 de volta para Nx2 (divide por w)."""
	pts = np.asarray(points_h, dtype=float)
	w = pts[:, 2:3]
	w[w == 0] = 1.0
	return pts[:, :2] / w


def translation_matrix(tx: float, ty: float) -> np.ndarray:
	"""Retorna a matriz de translação 3x3 para deslocamento (tx, ty)."""
	M = np.array([[1.0, 0.0, tx], [0.0, 1.0, ty], [0.0, 0.0, 1.0]], dtype=float)
	return M


def scale_matrix(sx: float, sy: float) -> np.ndarray:
	"""Retorna a matriz de escala 3x3 em relação à origem."""
	M = np.array([[sx, 0.0, 0.0], [0.0, sy, 0.0], [0.0, 0.0, 1.0]], dtype=float)
	return M


def rotation_matrix(theta_degrees: float) -> np.ndarray:
	"""Retorna a matriz de rotação 3x3 em torno da origem (ângulo em graus)."""
	t = math.radians(theta_degrees)
	c = math.cos(t)
	s = math.sin(t)
	M = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]], dtype=float)
	return M


def transform_about_point(M: np.ndarray, center: Tuple[float, float]) -> np.ndarray:
	"""Retorna a matriz equivalente a aplicar M com pivot em `center`.

	Efetivamente: T(cx,cy) * M * T(-cx,-cy)
	"""
	cx, cy = center
	return translation_matrix(cx, cy) @ M @ translation_matrix(-cx, -cy)


def apply_transform(points: np.ndarray, M: np.ndarray) -> np.ndarray:
	"""Aplica matriz 3x3 a um conjunto de pontos Nx2 e retorna Nx2 transformado."""
	P = to_homogeneous(points)
	P_t = P @ M.T
	return from_homogeneous(P_t)


def plot_polygon(ax, pts: np.ndarray, label: str = None, color: str = "C0"):
	pts = np.asarray(pts)
	closed = np.vstack([pts, pts[0]])
	ax.plot(closed[:, 0], closed[:, 1], marker="o", color=color, label=label)


def demo():
	# Polígono de exemplo (quadrado)
	square = np.array([[0.0, 0.0], [2.0, 0.0], [2.0, 1.0], [0.0, 1.0]])

	# --- Translação ---
	T = translation_matrix(1.5, 0.5)
	square_T = apply_transform(square, T)

	fig, ax = plt.subplots()
	plot_polygon(ax, square, label="Original", color="tab:blue")
	plot_polygon(ax, square_T, label="Translada (1.5,0.5)", color="tab:orange")
	ax.set_title("Translação")
	ax.set_aspect("equal")
	ax.legend()

	# --- Rotação em torno da origem ---
	R = rotation_matrix(30)
	square_R = apply_transform(square, R)

	fig2, ax2 = plt.subplots()
	plot_polygon(ax2, square, label="Original", color="tab:blue")
	plot_polygon(ax2, square_R, label="Rotated 30° (orig)", color="tab:green")
	ax2.set_title("Rotação em torno da origem")
	ax2.set_aspect("equal")
	ax2.legend()

	# --- Rotação em torno do centro do quadrado ---
	center = np.mean(square, axis=0)
	R_center = transform_about_point(rotation_matrix(45), tuple(center))
	square_Rc = apply_transform(square, R_center)

	fig3, ax3 = plt.subplots()
	plot_polygon(ax3, square, label="Original", color="tab:blue")
	plot_polygon(ax3, square_Rc, label="Rotated 45° (centro)", color="tab:red")
	ax3.set_title("Rotação em torno do centro do objeto")
	ax3.set_aspect("equal")
	ax3.legend()

	# --- Escala em relação à origem ---
	S = scale_matrix(1.5, 0.5)
	square_S = apply_transform(square, S)

	fig4, ax4 = plt.subplots()
	plot_polygon(ax4, square, label="Original", color="tab:blue")
	plot_polygon(ax4, square_S, label="Escala (1.5,0.5) orig", color="tab:purple")
	ax4.set_title("Escala em relação à origem")
	ax4.set_aspect("equal")
	ax4.legend()

	# --- Escala em relação ao centro ---
	S_center = transform_about_point(scale_matrix(0.5, 2.0), tuple(center))
	square_Sc = apply_transform(square, S_center)

	fig5, ax5 = plt.subplots()
	plot_polygon(ax5, square, label="Original", color="tab:blue")
	plot_polygon(ax5, square_Sc, label="Escala (0.5,2) centro", color="tab:brown")
	ax5.set_title("Escala em torno do centro do objeto")
	ax5.set_aspect("equal")
	ax5.legend()

	plt.show()


def main():
	demo()


if __name__ == "__main__":
	main()

