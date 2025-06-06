import tool
import pygame
import pygame_class

def main(screen):
	clock = pygame.time.Clock()
	pygame.mouse.set_visible(False)
	mouse = pygame_class.FrontSight()
	player_ship = pygame_class.PlayerShip((0, 0))
	while True:
		tool.quit_game()
		tool.update_mouse_pos()
		screen.fill((0, 0, 0))
		player_ship.update(screen)
		mouse.update(screen)
		pygame.display.flip()
		clock.tick(60)