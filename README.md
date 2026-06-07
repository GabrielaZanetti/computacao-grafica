# Computação Gráfica — Repositório de estudos (UNIJUÍ)

Sobre este repositório
- Este é o meu repositório pessoal de estudos para a disciplina de Computação Gráfica do Bacharelado em Ciência da Computação (UNIJUÍ). Reúno exercícios, experimentos e projetos que faço enquanto aprendo os conceitos.

Objetivos de estudo
- Entender o pipeline gráfico e os algoritmos fundamentais.
- Praticar transformações 2D/3D, projeções, rasterização, iluminação e texturização.
- Construir pequenos projetos para aplicar e consolidar os conceitos.

Ementa (resumo)
- Conceitos básicos e pipeline gráfico
- Transformações geométricas 2D e 3D
- Projeções: perspectiva e paralela
- Modelagem de primitivas, curvas e superfícies
- Rasterização, clipping e algoritmos de desenho
- Iluminação, shading e texturização
- Técnicas de renderização: rasterização e ray tracing
- APIs e bibliotecas: OpenGL, WebGL, Pygame/Three.js (exemplos)
- Aplicações: visualização, simulação e jogos

Estrutura do repositório — meus projetos e exercícios
- [braco mecanico](braco%20mecanico/) — projeto de braço robótico (simulação/visualização)
- [EI](EI/) — exercícios de introdução (subpastas por atividade)
- [relogio analogico](relogio%20analogico/) — relógio analógico — prática de transformações e animação
- [tux-escape](tux-escape/) — jogo demonstrativo — aplicação de conceitos interativos
- [Logotipo da UNIJUÍ](Logotipo%20da%20UNIJU%C3%8D/) — exemplo de modelagem/arte em POV-Ray

Como executar os projetos
- Crie e ative um ambiente Python (quando aplicável):

```bash
python3 -m venv venv
source venv/bin/activate
```

- Instale dependências por pasta quando houver `requirements.txt`:

```bash
pip install -r caminho/para/requirements.txt
```

- Exemplos práticos:
  - Rodar o jogo `tux-escape`:

```bash
cd tux-escape
python main.py
```

  - Executar exercícios em `EI/01`:

```bash
cd EI/01
python ei01.py
```

Observações
- Cada pasta pode ter um `README.md` ou arquivos de exemplo com instruções específicas; verifique antes de executar.
- Recomendo usar Python 3.8+ e instalar dependências locais conforme indicado em cada subpasta.

Organização pessoal (sugestão)
- Documente seu aprendizado: adicione comentários, prints e pequenos relatórios em cada atividade.
- Priorize projetos práticos para consolidar conceitos (ex.: `tux-escape`, `braco mecanico`).

Referências e leitura recomendada
- Foley, van Dam, Feiner & Hughes — "Computer Graphics: Principles and Practice"
- Shirley & Marschner — "Fundamentals of Computer Graphics"
- Documentação OpenGL / WebGL / Three.js / Pygame
