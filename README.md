# Portal Hands 🌀

Um projetinho muito massa que fiz para brincar com Realidade Aumentada e Visão Computacional no Python. 

A ideia é simples: a câmera lê o movimento das suas mãos, você faz um "L" com os dedos e o código abre um portal geométrico entre eles. O mais da hora é que apliquei uma lógica de máscara para rodar uns filtros malucos apenas dentro desse portal.

## O que tem de legal aqui?
* **Vários Filtros:** Tem câmera térmica, visão do Predador, Matrix, Minecraft (8-bits), Glitch, Cartoon, Invertido e Sépia. Dá pra viajar legal nos efeitos.
* **Geometria dinâmica:** Se você segurar as duas mãos normais, ele abre um polígono de 4 lados. Se você virar uma mão de cabeça para baixo, as linhas se cruzam e ele forma uma ampulheta perfeita.
* **Clique duplo no ar:** Para trocar de filtro, você não encosta no teclado. É só fazer um "beliscão" (juntar a ponta do indicador com a ponta do dedão) nas **duas mãos ao mesmo tempo**.

## Como rodar aí na sua máquina

**1. Instale as dependências**
Você vai precisar do Python (testado e rodando liso no 3.12). Abre o terminal e manda:
```bash
pip install opencv-python mediapipe==0.9.0.1 numpy
