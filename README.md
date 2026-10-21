# Visualizador 3D - Atividade Parcial (Módulo 4)

Aplicação desenvolvida em Python (PyOpenGL / GLFW) para a atividade de Computação Gráfica, focando na implementação do modelo de iluminação de Phong, atenuação por distância e iluminação de estúdio de 3 pontos.

## Execução

1. Instalar as dependências:
   pip install -r requirements.txt

2. Executar a aplicação:
   python main.py

Nota: A aplicação carrega os arquivos de modelo 3D, material e textura localizados na pasta assets/.

## Controles

- W, A, S, D: Movimentação da câmera (frente, trás, esquerda, direita)
- E / Q: Elevação da câmera (subir, descer)
- Botão Direito do Mouse: Girar a visualização
- Tecla 1: Liga / Desliga a Luz Principal (Key Light)
- Tecla 2: Liga / Desliga a Luz de Preenchimento (Fill Light)
- Tecla 3: Liga / Desliga a Contra-Luz (Back Light)
- Tecla X: Alterna entre o uso da textura e o material Phong puro (.mtl)
- ESC: Encerra a aplicação

## Estrutura dos Arquivos

- main.py: Loop principal, configuração da janela, callbacks e posicionamento automático das luzes.
- camera.py: Navegação da câmera no espaço 3D (matrizes View e Projection).
- obj_loader.py: Carregamento dos arquivos .obj, .mtl e textura.
- shader.py: Compilação dos programas shader GLSL.
- shaders/vertex_shader.glsl: Vertex Shader com cálculo de transformação e normais.
- shaders/fragment_shader.glsl: Fragment Shader com equação de Phong e atenuação quadrática por distância.
