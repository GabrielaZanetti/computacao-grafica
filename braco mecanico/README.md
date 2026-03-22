# Braco Robotico 2D com foco em Computacao Grafica

Este projeto implementa uma simulacao 2D de um braco robotico com dois segmentos, usando Pygame para desenhar a cena em tempo real.

## Arquivo principal

- braco_robotico.py: logica de simulacao, entrada por teclado, atualizacao dos estados e renderizacao do braco.

## Objetivo grafico

A ideia aqui e simples: usar um exemplo visual para treinar conceitos importantes de Computacao Grafica 2D.
No projeto voce consegue ver na pratica:

- sistema de coordenadas de tela;
- transformacoes geometricas por rotacao;
- composicao hierarquica de segmentos articulados;
- atualizacao quadro a quadro (render loop) com controle de FPS.

## Estrutura do programa (explicado de forma direta)

1. Inicializacao
   - O Pygame e iniciado.
   - A janela principal e criada (930x620).
   - O `clock.tick(60)` segura a simulacao em 60 FPS.

2. Visual
   - O tema usa preto, roxo e azul.
   - Alguns tamanhos (espessura/raio) variam para nao ficar sempre identico.

3. Estado da simulacao
   - A base comeca perto do centro, com pequena variacao aleatoria.
   - Angulos e tamanhos dos dois segmentos tambem variam no inicio.
   - As velocidades ficam em constantes para facilitar ajuste.

4. Renderizacao
   - `draw_axes()` desenha os eixos passando na posicao atual da base.
   - `draw_arm()` calcula as juntas com trigonometria e desenha o braco na tela.

5. Interacao
   - O loop le teclado em tempo real.
   - Voce move a base com as setas e gira os segmentos com A/D/W/S.

## Cinematica direta no codigo

O braco usa uma cadeia articulada de 2 links. A posicao da ponta e obtida por soma vetorial dos dois segmentos:

- Junta 1:
  - `x1 = base_x + length1 * cos(angle1)`
  - `y1 = base_y - length1 * sin(angle1)`

- Junta 2 (extremidade):
  - `x2 = x1 + length2 * cos(angle1 + angle2)`
  - `y2 = y1 - length2 * sin(angle1 + angle2)`

Observacao rapida: na tela, o eixo Y cresce para baixo. Por isso o seno aparece subtraindo no calculo de `y`.

## Controles

- Seta esquerda: move a base para a esquerda.
- Seta direita: move a base para a direita.
- Seta para cima: move a base para cima.
- Seta para baixo: move a base para baixo.
- A: aumenta `angle1` (rotacao do primeiro segmento).
- D: diminui `angle1`.
- W: aumenta `angle2` (rotacao relativa do segundo segmento).
- S: diminui `angle2`.

## Pipeline de atualizacao por frame

A cada quadro, o programa executa este fluxo:

1. Limpa o fundo com a cor principal.
2. Processa eventos do sistema.
3. Le o estado do teclado e atualiza variaveis da simulacao.
4. Recalcula posicoes geometricas das juntas.
5. Desenha eixos e braco.
6. Atualiza o buffer da janela (`pygame.display.flip()`).
7. Aplica limite de FPS (`clock.tick(60)`).

## Como executar

1. Instale dependencia:
   - `pip install pygame`
2. Execute:
   - `python "braco mecanico/braco_robotico.py"`

