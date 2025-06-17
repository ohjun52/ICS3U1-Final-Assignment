import UI
import tool
import pygame
from battle import Battle

def main():
	pygame.init()
	screen_info = pygame.display.Info()
	tool.SCREEN_SIZE = (screen_info.current_w, screen_info.current_h)
	screen = pygame.display.set_mode(tool.SCREEN_SIZE, pygame.NOFRAME)
	state = ["menu", "main"]
	while True:
		if state[0] == "menu":
			state = UI.Menu(state[1]).run(screen)
		elif state[0] == "plot":
			state = UI.Plot(state[1]).run(screen)
		elif state[0] == "battle":
			state = Battle(state[1]).run(screen)
		else:
			break

if __name__ == '__main__':
	main()