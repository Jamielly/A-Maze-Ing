```
import time
import sys
from typing import List, Tuple

def render_animation_frame(grid: List[List[int]], head: Tuple[int, int], delay: float = 0.02) -&gt; None:
    """Desenha um quadro da animação no terminal com reposicionamento ANSI."""
    # Reposiciona o cursor no topo da tela sem piscar (ANSI \033[H)
    sys.stdout.write("\033[H")
    
    # Renderiza o labirinto no terminal pintando a célula 'head' de destaque (ex: amarelo)
    draw_maze_terminal(grid, current_head=head)
    sys.stdout.flush()
    time.sleep(delay)

def generate_animated_maze(generator, config) -&gt; None:
    """Prepara a tela e chama o gerador com a animação ativa."""
    # Oculta o cursor do terminal
    sys.stdout.write("\033[?25l")
    try:
        generator.generate(
            step_callback=lambda grid, head: render_animation_frame(grid, head, delay=0.015)
        )
    finally:
        # Garante que o cursor volte a aparecer mesmo em caso de erro
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

```