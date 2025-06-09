import tool
import pygame
import pygame_class

def main(screen):
	clock = pygame.time.Clock()
	pygame.mouse.set_visible(False)
	mouse_in_range = pygame_class.FrontSight("images/front_sight_blue.png")
	mouse_out_range = pygame_class.FrontSight("images/front_sight_red.png")
	player_ship = pygame_class.PlayerShip((0, 0))
	bot_ship = pygame_class.BotShip("data/bot_ship/1.json",(1000, 600))
	while True:
		if pygame.event.get(pygame.QUIT): break
		tool.update_mouse_pos()
		screen.fill((0, 0, 0))
		player_ship.update(screen)
		bot_ship.get_player_rect(player_ship.object_rect)
		bot_ship.update(screen)
		if player_ship.bullet_range_rect.collidepoint(tool.MOUSE_POS):
			mouse_in_range.update(screen)
		else:
			mouse_out_range.update(screen)
		pygame.draw.rect(screen, (255, 0, 0), player_ship.bullet_range_rect)
		pygame.display.flip()
		clock.tick(60)
	print("done")