
# Minimalist Platformer

Um jogo de plataforma minimalista desenvolvido em Python utilizando a biblioteca [PgZero](https://pygame-zero.readthedocs.io/en/stable/).

## Visão Geral

Este projeto é um jogo de plataforma simples onde o jogador controla um herói que pode se mover para a esquerda, direita e pular entre plataformas. O objetivo é navegar pelo ambiente evitando inimigos e obstáculos.

## Funcionalidades

- **Movimentação do Herói**: Controle o herói usando as setas do teclado para mover-se para a esquerda e direita, e a tecla de espaço para pular.
- **Animações de Sprite**: O herói possui animações para caminhar e pular, proporcionando uma experiência visual agradável.
- **Plataformas**: Diferentes plataformas estão posicionadas no ambiente para o herói pular e se movimentar.
- **Música e Sons**: O jogo inclui música de fundo e efeitos sonoros para uma experiência imersiva.

## Estrutura do Projeto

- `run.py`: Arquivo principal que inicia o jogo.
- `espelha.py`: Script auxiliar para manipulação de imagens.
- `images/`: Diretório contendo as imagens e sprites utilizados no jogo.
- `sounds/`: Diretório contendo os efeitos sonoros do jogo.
- `music/`: Diretório contendo as músicas de fundo do jogo.
- `requirements.txt`: Lista de dependências necessárias para executar o projeto.

## Instalação e Execução

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/willianferrari/gamepgzero.git
   ```

2. **Navegue até o diretório do projeto**:

   ```bash
   cd gamepgzero
   ```

3. **Crie um ambiente virtual** (recomendado):

   ```bash
   python -m venv venv
   ```

4. **Ative o ambiente virtual**:

   - No Windows:

     ```bash
     venv\Scripts\activate
     ```

   - No macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

5. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

6. **Execute o jogo**:

   ```bash
   pgzrun run.py
   ```

## Controles

- **Seta Esquerda**: Move o herói para a esquerda.
- **Seta Direita**: Move o herói para a direita.
- **Barra de Espaço**: Faz o herói pular.
- **Tecla M**: Liga/Desliga a música de fundo.
- **Tecla ESC**: Sai do jogo.

## Requisitos

- Python 3.x
- PgZero

## Observações

Certifique-se de que as imagens e sons necessários estão presentes nos diretórios `images/`, `sounds/` e `music/` para o funcionamento correto do jogo.