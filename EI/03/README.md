# EI 03 - Visualização e Manipulação de Objetos 3D

---

# 📋 Sumário Executivo

Este documento descreve a implementação de um sistema de visualização e manipulação de objetos tridimensionais em Python utilizando:

- **OpenGL** para renderização gráfica 3D
- **Pygame** para gerenciamento da janela e entrada do usuário
- **Projeção perspectiva 3D → 2D**
- **Transformações geométricas tridimensionais**
- **Leitura de arquivos `.OBJ`**
- **Interação em tempo real via teclado**

O projeto implementa conceitos fundamentais de Computação Gráfica relacionados à representação tridimensional, pipeline gráfico, projeção e manipulação geométrica.

---

# 1️⃣ Como Cada Funcionalidade Foi Implementada

## 1.1 Renderização de Objetos 3D

### Descrição

A renderização consiste na exibição de objetos tridimensionais em uma janela gráfica utilizando OpenGL.

Inicialmente foi implementado um cubo 3D utilizando:
- vértices
- arestas
- desenho em modo wireframe

### Estrutura do Cubo

```python
vertices_cubo = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
)
````

Cada vértice representa um ponto no espaço tridimensional:

$$(x, y, z)$$

### Renderização das Arestas

```python
glBegin(GL_LINES)

for aresta in arestas_cubo:
    for vertice in aresta:
        glVertex3fv(vertices_cubo[vertice])

glEnd()
```

O OpenGL interpreta os pares de vértices como segmentos de reta.

---

# 1.2 Projeção 3D para 2D

## Descrição

A projeção transforma coordenadas tridimensionais em coordenadas visíveis na tela 2D.

Foi utilizada projeção perspectiva através da função:

```python
gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
```

### Parâmetros

* **45** → campo de visão (FOV)
* **aspect ratio** → proporção da tela
* **0.1** → plano próximo
* **100.0** → plano distante

### Funcionamento

Objetos mais distantes aparentam menores dimensões, simulando visão humana.

---

# 1.3 Transformações Geométricas 3D

O sistema implementa:

* Rotação
* Translação
* Escala

Todas aplicadas em tempo real.

---

## Rotação

### Descrição

A rotação altera a orientação do objeto em torno de um eixo.

### Implementação

```python
glRotatef(rot_x, 1, 0, 0)
glRotatef(rot_y, 0, 1, 0)
glRotatef(rot_z, 0, 0, 1)
```

### Eixos

* X → inclinação vertical
* Y → rotação lateral
* Z → rotação frontal

### Fórmula Matemática

Rotação em torno do eixo X:

$$
R_x(\theta) =
\begin{bmatrix}
1 & 0 & 0 \
0 & \cos\theta & -\sin\theta \
0 & \sin\theta & \cos\theta
\end{bmatrix}
$$

---

## Translação

### Descrição

Move o objeto no espaço tridimensional.

### Implementação

```python
glTranslatef(pos_x, pos_y, pos_z)
```

### Exemplo

* eixo X → esquerda/direita
* eixo Y → cima/baixo
* eixo Z → profundidade

---

## Escala

### Descrição

Altera o tamanho do objeto.

### Implementação

```python
glScalef(escala, escala, escala)
```

### Efeito

* valores maiores → objeto aumenta
* valores menores → objeto reduz

---

# 1.4 Leitura de Arquivos `.OBJ`

## Descrição

O formato `.OBJ` é utilizado para representar modelos tridimensionais.

O programa interpreta:

* vértices (`v`)
* faces (`f`)

---

## Leitura dos Vértices

```python
if line.startswith("v "):
    values = line.strip().split()[1:]
    vertex = tuple(map(float, values))
    self.vertices.append(vertex)
```

Exemplo no arquivo OBJ:

```obj
v 1.0 0.0 0.0
```

Representa:

$$(1.0,\ 0.0,\ 0.0)$$

---

## Leitura das Faces

```python
elif line.startswith("f "):
```

As faces conectam vértices formando polígonos.

Exemplo:

```obj
f 1 2 3
```

Representa um triângulo.

---

## Renderização do OBJ

```python
for face in self.faces:
    for i in range(len(face)):
        v1 = self.vertices[face[i]]
        v2 = self.vertices[face[(i + 1) % len(face)]]

        glVertex3fv(v1)
        glVertex3fv(v2)
```

As faces são desenhadas em wireframe.

---

# 1.5 Interação com o Usuário

## Controles Implementados

| Tecla | Ação           |
| ----- | -------------- |
| W / S | Rotação eixo X |
| A / D | Rotação eixo Y |
| Q / E | Rotação eixo Z |
| Setas | Movimentação   |
| Z / X | Zoom           |
| + / - | Escala         |
| O     | Carregar OBJ   |
| ESC   | Sair           |

---

# 2️⃣ Base Matemática Utilizada

---

# 2.1 Coordenadas Tridimensionais

Os objetos são representados por pontos no espaço:

$$(x, y, z)$$

Cada vértice possui:

* largura
* altura
* profundidade

---

# 2.2 Matrizes de Transformação

As transformações geométricas em 3D utilizam matrizes.

## Exemplo Geral

$$
P' = M \cdot P
$$

Onde:

* $P$ → ponto original
* $M$ → matriz transformação
* $P'$ → ponto transformado

---

# 2.3 Pipeline Gráfico

Fluxo simplificado:

```text
Modelo 3D
    ↓
Transformações
    ↓
Projeção
    ↓
Rasterização
    ↓
Tela 2D
```

---

# 3️⃣ Como As Transformações Foram Aplicadas

## Fluxo Geral

```python
glLoadIdentity()

gluPerspective(...)

glTranslatef(...)

glScalef(...)

glRotatef(...)

desenhar_objeto()
```

---

## Ordem das Transformações

A ordem é importante:

1. Projeção
2. Translação
3. Escala
4. Rotação
5. Renderização

A multiplicação matricial não é comutativa.

---

# 4️⃣ Dificuldades Encontradas e Soluções

---

## 4.1 Manipulação do Espaço 3D

### Dificuldade

Entender posicionamento e orientação em três dimensões.

### Solução

Separação clara dos eixos:

* X
* Y
* Z

E testes individuais para cada transformação.

---

## 4.2 Projeção Perspectiva

### Dificuldade

Configurar corretamente a câmera e profundidade.

### Solução

Uso de:

```python
gluPerspective()
```

Com parâmetros ajustados para evitar distorções.

---

## 4.3 Arquivos OBJ

### Dificuldade

Interpretar corretamente índices das faces.

### Solução

Conversão:

```python
int(index) - 1
```

Porque arquivos `.OBJ` começam em índice 1, enquanto Python inicia em 0.

---

## 4.4 Ordem das Transformações

### Dificuldade

Transformações aplicadas em ordem incorreta geravam comportamentos inesperados.

### Solução

Organização correta do pipeline:

* translação
* escala
* rotação

---

# 5️⃣ Estrutura do Código

```text
03.py
├── Classe OBJ
│   ├── load()
│   └── draw()
├── Estrutura do cubo
│   ├── vertices_cubo
│   └── arestas_cubo
├── Renderização
│   └── desenhar_cubo()
├── Inicialização OpenGL
│   └── inicializar()
├── Loop principal
│   └── main()
└── Interação teclado
```

---

# 6️⃣ Funcionalidades Demonstradas

O programa demonstra:

* Renderização 3D
* Projeção perspectiva
* Rotação em múltiplos eixos
* Escala dinâmica
* Translação
* Carregamento de modelos OBJ
* Interação em tempo real

---

# 7️⃣ Como Executar

---

## Instalação das Dependências

```bash
pip install -r requirements.txt
```

---

## Dependências Utilizadas

```txt
pygame
PyOpenGL
PyOpenGL_accelerate
```

---

## Execução

```bash
python 03.py
```

---

# 8️⃣ Exemplo de Uso do OBJ

Ao pressionar:

```text
O
```

O sistema solicitará:

```text
Digite o caminho do arquivo OBJ:
```

Exemplo:

```text
modelo.obj
```

---

# 9️⃣ Conceitos de Computação Gráfica Aplicados

O projeto utiliza:

* representação vetorial 3D
* pipeline gráfico
* projeção perspectiva
* transformações geométricas
* renderização wireframe
* leitura de modelos 3D
* manipulação interativa

---

# 🔟 Referências Bibliográficas

* **CONCI, A.; AZEVEDO, E.; LETA, F. R.**
  *Computação Gráfica: Teoria e Prática*. 2. ed. Rio de Janeiro: Elsevier, 2008.

* **DE VRIES, Joey.**
  *LearnOpenGL*. 2020.
  Disponível em:
  [https://learnopengl.com](https://learnopengl.com)

* **OpenGL Documentation**
  [https://www.opengl.org/documentation/](https://www.opengl.org/documentation/)

* **Wavefront OBJ File Format**
  [https://en.wikipedia.org/wiki/Wavefront_.obj_file](https://en.wikipedia.org/wiki/Wavefront_.obj_file)

---
