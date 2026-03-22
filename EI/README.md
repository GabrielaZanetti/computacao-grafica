# EI 01 - Biblioteca Matemática para Computação Gráfica

Este diretório contém a implementação da atividade **EI 01**, com funções matemáticas básicas para computação gráfica.

## Arquivos

- `ei01.py`: biblioteca principal com classes e funções matemáticas.
- `exemplo_ei01.py`: script de demonstração com exemplos prontos de uso.

## Funcionalidades implementadas

- Estruturas de dados:
  - `Ponto2D`
  - `Ponto3D`
- Multiplicação de matrizes quadradas:
  - `multiplicar_matriz_2x2`
  - `multiplicar_matriz_3x3`
  - `multiplicar_matriz_4x4`
- Geometria:
  - `comprimento_segmento_2d`
  - `comprimento_segmento_3d`
  - `segmentos_intersectam`
  - `ponto_interseccao_segmentos`

## Pré-requisitos

- Python 3.10+ (recomendado Python 3.12)
- Terminal no Linux (ou equivalente no Windows/Mac)

## Como executar (passo a passo detalhado)

### 1. Abrir a pasta do projeto

No terminal, entre na raiz do repositório:

```bash
cd /home/gabi/Documentos/GitHub/computacao-grafica
```

### 2. Executar o exemplo completo

Rode o script de demonstração:

```bash
python3 EI/exemplo_ei01.py
```

Saída esperada (resumo):

- Mostra criação de pontos 2D e 3D
- Calcula comprimento de segmentos
- Multiplica matrizes 2x2, 3x3 e 4x4
- Verifica interseção entre segmentos e imprime o ponto de interseção

### 3. Testar no Python interativo (opcional)

Se quiser testar funções isoladas:

```bash
python3
```

No prompt do Python:

```python
from EI.ei01 import Ponto2D, comprimento_segmento_2d
p1 = Ponto2D(0, 0)
p2 = Ponto2D(3, 4)
print(comprimento_segmento_2d(p1, p2))
```

Resultado esperado:

```text
5.0
```

## Como usar no seu próprio código

Exemplo mínimo:

```python
from EI.ei01 import Ponto2D, segmentos_intersectam

a = Ponto2D(0, 0)
b = Ponto2D(4, 4)
c = Ponto2D(0, 4)
d = Ponto2D(4, 0)

print(segmentos_intersectam(a, b, c, d))
```

## Observações

- As funções de matriz validam o tamanho e geram `ValueError` para dimensões inválidas.
- A interseção de segmentos considera casos colineares e pontos de extremidade.


## Roteiro de vídeo (apresentação curta)

Tempo sugerido: 2 a 3 minutos.

### 1. Abertura (20 a 30 segundos)

Fala sugerida:

"Olá, eu sou Gabriela Zanetti e este é o trabalho EI 01 de Computação Gráfica. Neste projeto, desenvolvi uma biblioteca matemática com operações básicas usadas em gráficos computacionais."

### 2. Mostrar estrutura do projeto (20 a 30 segundos)

Fala sugerida:

"Aqui na pasta EI eu tenho dois arquivos principais: o `ei01.py`, que é a biblioteca, e o `exemplo_ei01.py`, que demonstra todas as funcionalidades implementadas."

### 3. Explicar implementações (50 a 70 segundos)

Fala sugerida:

"Na biblioteca, implementei as classes `Ponto2D` e `Ponto3D` para representar coordenadas. Também implementei multiplicação de matrizes 2x2, 3x3 e 4x4 com validação de tamanho. Na parte geométrica, implementei o cálculo do comprimento de segmentos em 2D e 3D. Por fim, implementei a verificação de interseção entre dois segmentos de reta e uma função que retorna o ponto de interseção quando ele existe."

### 4. Executar o exemplo (30 a 40 segundos)

No terminal, executar:

```bash
python3 EI/exemplo_ei01.py
```

Fala sugerida:

"Ao executar o exemplo, o programa mostra os resultados das distâncias, das multiplicações de matrizes e da interseção entre segmentos. Neste caso, os segmentos se cruzam no ponto (2, 2)."

### 5. Encerramento (15 a 20 segundos)

Fala sugerida:

"Com isso, a biblioteca atende os requisitos solicitados para a atividade EI 01. Obrigado."
