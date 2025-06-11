import tool
import pygame
import battle

def main():
	pygame.init()
	screen_info = pygame.display.Info()
	tool.SCREEN_SIZE = (screen_info.current_w, screen_info.current_h)
	screen = pygame.display.set_mode(tool.SCREEN_SIZE, pygame.FULLSCREEN)
	battle.main(screen, "data/battle_setup/1.json")

if __name__ == '__main__':
	main()
