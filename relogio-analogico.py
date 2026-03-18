# Aula 05 - Criando um Relógio Analógico com PyGame ou PyOpenGL
# MARCOS RONALDO MELO CAVALHEIRO
# •
# 11 de mar. (editado: 13 de mar.)
# 1 ponto
# Data de entrega: 25 de mar., 19:20
# Data de entrega: Individual

# Objetivo: Desenvolver um relógio analógico sincronizado com o relógio do sistema, utilizando PyGame ou PyOpenGL.

# Requisitos da Atividade:
# O relógio deve ser desenhado em 2D, com os ponteiros ajustando-se em tempo real.
# Os ponteiros devem ter cores diferentes:
#                     * Vermelho para os segundos
#                     * Azul para os minutos
#                     * Verde para as horas
# O relógio deve ter um anel externo indicando a estrutura de um relógio real.
# Deve ser centralizado na tela.
# O acadêmico pode escolher entre PyGame ou PyOpenGL para sua implementação.

# Desafio Extra (Opcional)
# Adicionar os números de 1 a 12 ao redor do relógio.
# Criar um ponteiro de alarme ajustável via teclado.
# O que entregar?
# O código-fonte da implementação.
# Um print da execução do relógio.
# Um pequeno relatório explicando as escolhas feitas na implementação.
# Como Começar?
# Escolha entre PyGame ou PyOpenGL e utilize um dos exemplos disponíveis como referência.
# Opção 1: PyGame
# Usa renderização 2D com superfícies e linhas.
# Opção 2: PyOpenGL
# Usa gráficos vetoriais para desenhar as formas.
# Recursos e Dicas
# Para PyGame:  pip install pygame-ce
# Para PyOpenGL:  pip install PyOpenGL PyOpenGL_accelerate
# Sugestão: Utilize time.localtime() para obter a hora do sistema.
# Cálculo dos ponteiros: Utilize funções trigonométricas (math.sin(), math.cos()) para calcular os ângulos corretamente.
# Dúvidas? Poste nos comentários ou entre em contato com o professor.

# OBS.: 4 academicos escolhidos aletóriamente iram explicar o código