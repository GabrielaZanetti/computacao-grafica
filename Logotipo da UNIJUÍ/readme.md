Disciplina: Computação Gráfica
Atividade:  Aula 12 — Modelagem CSG no POV-Ray

-----------------------------------------------------------
DECISÕES DE PROJETO
-----------------------------------------------------------

1. CÂMERA ORTOGRÁFICA
   Optei por câmera orthographic para eliminar distorção de
   perspectiva, já que o logotipo é um símbolo 2D/plano. Isso
   garante fidelidade visual às proporções reais.

2. OVAL PRINCIPAL (corpo externo)
   Construída com sphere { scale <OvalLargura, OvalAltura, ...> }
   A esfera escalada de forma não-uniforme gera o elipsoide.

3. LUA CRESCENTE — operação CSG: difference
   É a subtração de um segundo oval (maior, deslocado para
   cima e para a direita) do oval principal. Esse é o núcleo
   da atividade CSG.

4. CÍRCULO INTERNO — operação CSG: difference
   Disco (esfera achatada) posicionado no recorte da lua.
   Duas faixas horizontais são subtraídas dele para criar
   as listras visíveis no logotipo original.

5. FAIXAS INFERIORES — operação CSG: intersection
   As duas faixas horizontais da base foram obtidas pela
   INTERSEÇÃO de caixas (box) com o oval externo, garantindo
   que as faixas só apareçam dentro do contorno do logo.

6. PARÂMETROS DECLARADOS (#declare)
   Todas as dimensões relevantes estão em variáveis no topo
   do arquivo para facilitar ajuste fino sem alterar a lógica.

7. ILUMINAÇÃO
   Duas fontes de luz shadowless:
   - Principal: frontal-esquerda-superior (luz branca)
   - Preenchimento: direita-inferior (luz suave azulada)
   Isso cria um leve gradiente que dá volume ao objeto.

-----------------------------------------------------------
COMO RENDERIZAR
-----------------------------------------------------------

Linha de comando:
  povray +I logo_unijui.pov +O logo_unijui.png +W1200 +H1400 +A

Ou via interface gráfica do POV-Ray:
  Abra logo_unijui.pov > Run > aguarde a renderização.

Resolução sugerida: 1200 x 1400 pixels (proporção do logo).

-----------------------------------------------------------
DIFICULDADES ENCONTRADAS
-----------------------------------------------------------

- Ajuste fino das posições da lua crescente: exigiu várias
  iterações para alinhar o oval de corte ao visual original.

- Posicionamento das faixas horizontais: a distância entre
  elas e a espessura de cada faixa foram calibradas visualmente
  comparando com o logotipo de referência.

- Uso de intersection nas faixas inferiores: inicialmente usei
  box simples, mas as faixas "vazavam" além do contorno do logo,
  necessitando a operação de interseção com o oval externo.
