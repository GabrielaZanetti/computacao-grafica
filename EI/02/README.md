# EI 02 - Implementação de Transformações 2D
---

## 📋 Sumário Executivo

Este documento descreve a implementação de transformações geométricas 2D fundamentais em Python, utilizando:
- **Coordenadas homogêneas** para representação unificada de transformações afins
- **Matrizes 3×3** para aplicação eficiente de operações lineares
- **Matplotlib** para visualização antes/depois de cada transformação

As transformações implementadas são: **translação**, **escala** e **rotação**, com suporte a pivot points (centro de rotação/escala arbitrário).

---

## 1️⃣ Como Cada Transformação Foi Implementada

### 1.1 Translação

**Descrição:** Move um objeto de forma linear no plano 2D, alterando suas coordenadas por um deslocamento $(t_x, t_y)$.

**Matriz 3×3:**
$$T(t_x, t_y) = \begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{bmatrix}$$

**Implementação no código:**
```python
def translation_matrix(tx: float, ty: float) -> np.ndarray:
    """Retorna a matriz de translação 3x3 para deslocamento (tx, ty)."""
    M = np.array([[1.0, 0.0, tx], 
                  [0.0, 1.0, ty], 
                  [0.0, 0.0, 1.0]], dtype=float)
    return M
```

**Exemplo de uso:**
- Original: ponto $(0, 0)$
- Com $T(1.5, 0.5)$: ponto $(1.5, 0.5)$

---

### 1.2 Escala

**Descrição:** Modifica o tamanho de um objeto multiplicando cada coordenada por um fator de escala $(s_x, s_y)$ em relação à origem $(0, 0)$.

**Matriz 3×3:**
$$S(s_x, s_y) = \begin{bmatrix} s_x & 0 & 0 \\ 0 & s_y & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

**Implementação no código:**
```python
def scale_matrix(sx: float, sy: float) -> np.ndarray:
    """Retorna a matriz de escala 3x3 em relação à origem."""
    M = np.array([[sx, 0.0, 0.0], 
                  [0.0, sy, 0.0], 
                  [0.0, 0.0, 1.0]], dtype=float)
    return M
```

**Exemplos:**
- $S(1.5, 0.5)$: expande 1.5× na horizontal, comprime a 0.5× na vertical
- $S(0.5, 2.0)$: comprime à metade na horizontal, expande 2× na vertical

**Escala em torno de um ponto arbitrário:**
Para escalar em torno de um ponto $(c_x, c_y)$, usamos a composição:
$$M_{\text{escala}} = T(c_x, c_y) \cdot S(s_x, s_y) \cdot T(-c_x, -c_y)$$

---

### 1.3 Rotação

**Descrição:** Gira um objeto em torno da origem $(0, 0)$ por um ângulo $\theta$ (em graus, convertido para radianos).

**Matriz 3×3:**
$$R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

**Implementação no código:**
```python
def rotation_matrix(theta_degrees: float) -> np.ndarray:
    """Retorna a matriz de rotação 3x3 em torno da origem (ângulo em graus)."""
    t = math.radians(theta_degrees)
    c = math.cos(t)
    s = math.sin(t)
    M = np.array([[c, -s, 0.0], 
                  [s, c, 0.0], 
                  [0.0, 0.0, 1.0]], dtype=float)
    return M
```

**Rotação em torno de um ponto arbitrário:**
Para rotacionar em torno de $(c_x, c_y)$:
$$M_{\text{rotação}} = T(c_x, c_y) \cdot R(\theta) \cdot T(-c_x, -c_y)$$

---

## 2️⃣ Base Matemática Utilizada

### 2.1 Coordenadas Homogêneas

Em computação gráfica, representamos pontos 2D usando **coordenadas homogêneas**:
- Ponto 2D: $(x, y)$
- Representação homogênea: $(x, y, 1)$

**Vantagem:** Transformações afins (translação, escala, rotação) podem ser expressas como multiplicação matricial 3×3, permitindo composição eficiente de múltiplas transformações.

### 2.2 Multiplicação Matricial e Composição

Para aplicar uma transformação $M$ a um ponto $p = [x, y, 1]$ (vetor linha):
$$p' = p \cdot M^T$$

Para composição de múltiplas transformações (ex: rotacionar em torno de um ponto):
$$M_{\text{final}} = M_1 \cdot M_2 \cdot M_3$$

**Ordem importa!** A multiplicação matricial não é comutativa.

### 2.3 Conversão Homogênea

**De 2D para homogêneo:**
```python
def to_homogeneous(points: np.ndarray) -> np.ndarray:
    """Converte um array Nx2 em coordenadas homogêneas Nx3."""
    points = np.asarray(points, dtype=float)
    ones = np.ones((points.shape[0], 1), dtype=float)
    return np.hstack([points, ones])
```

**De homogêneo para 2D:**
```python
def from_homogeneous(points_h: np.ndarray) -> np.ndarray:
    """Converte um array homogêneo Nx3 de volta para Nx2 (divide por w)."""
    pts = np.asarray(points_h, dtype=float)
    w = pts[:, 2:3]
    w[w == 0] = 1.0
    return pts[:, :2] / w
```

---

## 3️⃣ Como As Matrizes Foram Aplicadas Nas Transformações

### 3.1 Fluxo Geral de Transformação

```
Pontos 2D (Nx2)
    ↓
[to_homogeneous]  →  Pontos homogêneos (Nx3)
    ↓
[Multiplicação por M.T]  →  Pontos transformados (Nx3)
    ↓
[from_homogeneous]  →  Pontos 2D (Nx2)
```

### 3.2 Função Principal: `apply_transform`

```python
def apply_transform(points: np.ndarray, M: np.ndarray) -> np.ndarray:
    """Aplica matriz 3x3 a um conjunto de pontos Nx2 e retorna Nx2 transformado."""
    P = to_homogeneous(points)          # Nx2 → Nx3
    P_t = P @ M.T                       # Multiplicação por M transposta
    return from_homogeneous(P_t)        # Nx3 → Nx2
```

**Por que transpor M?**
- NumPy e a maioria das bibliotecas usam **vetores linha** por padrão
- A fórmula matemática tradicional usa $p' = M \cdot p$ (vetor coluna)
- Para vetores linha: $p' = p \cdot M^T$

### 3.3 Transformações Compostas: `transform_about_point`

```python
def transform_about_point(M: np.ndarray, center: Tuple[float, float]) -> np.ndarray:
    """Retorna a matriz equivalente a aplicar M com pivot em `center`."""
    cx, cy = center
    return translation_matrix(cx, cy) @ M @ translation_matrix(-cx, -cy)
```

**Lógica:**
1. **Transladar o ponto para a origem:** $T(-c_x, -c_y)$
2. **Aplicar a transformação (rotação ou escala):** $M$
3. **Transladar de volta:** $T(c_x, c_y)$

**Exemplo - Rotação em torno do centro:**
```python
center = np.mean(square, axis=0)  # Calcula o baricentro
R_center = transform_about_point(rotation_matrix(45), tuple(center))
square_rotated = apply_transform(square, R_center)
```

---

## 4️⃣ Dificuldades Encontradas e Soluções

### 4.1 Ordem de Multiplicação Matricial

**Dificuldade:** Inicialmente, tive dúvida se a ordem de composição deveria ser $T \cdot M \cdot T^{-1}$ ou $T^{-1} \cdot M \cdot T$.

**Solução:** 
- Verificação matemática: a ordem correta é $T(c) \cdot M \cdot T(-c)$ porque:
  1. Transladamos o ponto para a origem (deslocamento negativo)
  2. Aplicamos a transformação na origem
  3. Trazemos de volta (deslocamento positivo)
- Testei visualmente com matplotlib e confirmei que o ponto de pivot estava correto

### 4.2 Transposta da Matriz

**Dificuldade:** Por que usar $M^T$ ao invés de $M$ diretamente?

**Solução:**
- NumPy trabalha com **vetores linha** por padrão
- Fórmula tradicional de gráficos: $p' = M \cdot p$ (vetor coluna)
- Para vetores linha: $p' = p \cdot M^T$
- Testei ambas as formas e a transposição forneceu resultados corretos

### 4.3 Coordenadas Homogêneas e Divisão por W

**Dificuldade:** Qual valor usar para $w$ na coordenada homogênea?

**Solução:**
- Para transformações afins simples (translação, rotação, escala não-uniforme), $w$ permanece 1
- Proteção contra divisão por zero: `w[w == 0] = 1.0`
- Isso garante estabilidade numérica

### 4.4 Ângulos em Graus vs. Radianos

**Dificuldade:** Python usa radianos, mas usuários pensam em graus.

**Solução:**
```python
def rotation_matrix(theta_degrees: float) -> np.ndarray:
    t = math.radians(theta_degrees)  # Conversão explícita
    # ... resto da função
```

Isso melhora a usabilidade e evita erros de escala de ~57×.

### 4.5 Dependências Externas

**Dificuldade:** NumPy e Matplotlib precisam estar instalados.

**Solução:**
- Criei `requirements.txt` com as dependências
- Instruções claras de instalação: `pip install -r requirements.txt`
- Documentação explícita no cabeçalho do arquivo

---

## 5️⃣ Estrutura do Código

```
ei02.py
├── Funções de conversão
│   ├── to_homogeneous()
│   └── from_homogeneous()
├── Matrizes de transformação
│   ├── translation_matrix()
│   ├── scale_matrix()
│   └── rotation_matrix()
├── Composição de transformações
│   └── transform_about_point()
├── Aplicação de transformações
│   └── apply_transform()
├── Visualização
│   └── plot_polygon()
├── Demonstração
│   └── demo()
└── Entrada principal
    └── main() / __main__
```

---

## 6️⃣ Visualizações Geradas

O script `ei02.py` gera **5 gráficos matplotlib** demonstrando:

1. **Translação:** Deslocamento de (1.5, 0.5)
2. **Rotação (origem):** Rotação de 30° em torno da origem
3. **Rotação (centro):** Rotação de 45° em torno do centro do objeto
4. **Escala (origem):** Escala de (1.5, 0.5) em relação à origem
5. **Escala (centro):** Escala de (0.5, 2.0) em torno do centro do objeto

Cada gráfico mostra o polígono **original** (azul) e **transformado** (colorido) sobrepostos.

---

## 7️⃣ Como Executar

### Instalação de Dependências
```bash
pip install -r requirements.txt
```

### Execução
```bash
python ei02.py
```

Será aberta uma janela de matplotlib com as 5 visualizações interativas.

---

## 8️⃣ Referências Bibliográficas

- **CONCI, A.; AZEVEDO, E.; LETA, F. R.** (2008). *Computação Gráfica: Teoria e Prática*. 2. ed. Rio de Janeiro: Elsevier.
  - Capítulo 2, Seção 2.3: Aritmética de Vetores e Matrizes
  - Capítulo 3: Transformações Geométricas 2D

- **Foley, J. D., et al.** (1996). *Computer Graphics: Principles and Practice*. 2. ed. Boston: Addison-Wesley.
  - Capítulo 5: Geometric Transformations

- **Coordinate Geometry and Linear Algebra (Coordenadas Homogêneas):**
  - https://en.wikipedia.org/wiki/Homogeneous_coordinates
  - https://learnopengl.com/Getting-started/Transformations

---