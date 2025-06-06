import pygame
import battle
from tool import SCREEN_SIZE

def main():
	pygame.init()
	scren = pygame.display.set_mode(SCREEN_SIZE)
	battle.main(scren)

if __name__ == '__main__':
	main()
