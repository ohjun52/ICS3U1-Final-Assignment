import tool
import pygame
import pygame_class
from main import screen

def main():
	clock = pygame.time.Clock()
	pygame.mouse.set_visible(False)
	mouse = pygame_class.FrontSight()
	player_ship = pygame_class.PlayerShip((0, 0))
	while True:
		tool.quit_game()
		screen.fill((0, 0, 0))
		mouse.front_sight_track()
		player_ship.move()
		player_ship.rotate(mouse.pos)
		player_ship.update()
		mouse.update()
		pygame.display.flip()
		clock.tick(60)