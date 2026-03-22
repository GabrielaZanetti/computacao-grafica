# Relatorio Curto - Relogio Analogico (PyGame)

## Objetivo da implementacao
A proposta foi criar um relogio analogico 2D sincronizado com o horario do sistema, com foco em leitura visual clara e interacao simples para ajuste de alarme.

## Escolhas principais de implementacao
1. Biblioteca
- Foi usado PyGame por ser direto para desenhar formas 2D (circulos, linhas e texto) e manter o loop em tempo real com FPS controlado.

2. Estrutura visual
- O mostrador principal fica na area direita da janela.
- No canto superior esquerdo foi criado um painel de alarme com:
  - instrucoes de uso,
  - horario configurado,
  - um mini relogio analogico mostrando o alarme.
- Essa separacao evita poluicao visual e facilita a leitura do que e hora atual e do que e configuracao de alarme.

3. Paleta de cores
- Foi adotada uma paleta em tons de preto, roxo e azul para manter identidade visual consistente.
- Os ponteiros principais usam cores diferentes para reforcar a leitura:
  - horas,
  - minutos,
  - segundos.

4. Geometria e variacao
- Foram usados valores com pequenas variacoes aleatorias (raio, posicao, espessuras e tamanhos dos ponteiros) para o resultado nao ficar sempre identico.
- Mesmo com variacao, o codigo limita o tamanho do relogio principal para nao invadir a area de legenda/painel.

5. Sincronizacao com o sistema
- A hora vem de time.localtime().
- Os angulos dos ponteiros sao calculados com trigonometria:
  - segundos: 6 graus por segundo,
  - minutos: 6 graus por minuto com ajuste fino por segundo,
  - horas: 30 graus por hora com ajuste fino por minutos e segundos.

6. Interacao do alarme
- O horario do alarme e ajustado por teclado:
  - cima/baixo alteram hora,
  - esquerda/direita alteram minuto.
- O alarme aparece em dois lugares:
  - texto no painel,
  - ponteiro dedicado no mostrador principal.

## Decisao de organizacao do codigo
- Funcoes separadas para cada parte visual (ponteiros, marcas, numeros e painel).
- Essa divisao deixa manutencao mais simples e ajuda na explicacao do codigo em apresentacao.

## Resultado
A implementacao atende a proposta de um relogio analogico funcional, com visual personalizado, sincronizacao em tempo real e recurso extra de alarme com interface clara para ajuste.

## Arquivo
- Codigo-fonte: relogio-analogico.py
