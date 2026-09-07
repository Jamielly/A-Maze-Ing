from mazegen import MazeGenerator

generator = MazeGenerator(width=20, height=15)
maze = generator.generate(perfect=True)

COLORS = {
    "GREEN": "\033[1;32m",
    "CYAN": "\033[1;36m",
    "RED": "\033[1;31m",
    "YELLOW": "\033[1;33m",
    "PURPLE": "\033[1;35m",
    "WHITE": "\033[1;37m",
    "RESET": "\033[0m"
}

print(f"{COLORS['GREEN']}██{COLORS['RESET']}", end="")

import  os

def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')

show_solution = True
wall_color = "GREEN"

while True:
  clear_screen()
  draw_maze(maze, show_solution, wall_color)

  print("\n=== A-Maze-Ing Menu ====")
  print("1. Regerenerar novo labirinto")
  print("2. Mostrar/Ocultar o menor caminho (Toggle)")
  print("3. Rotacionar a cor das paredes")
  print("4. Sair")

  choice = input("Escolha uma opção (1-4): ")
  if choice == "1":
    maze = generate_new_maze()
  elif choice == "2":
    show_solution = not show_solution
  elif choice == "3":
    wall_color = rotate_color(wall_color)
  elif choice == "4":
    break
