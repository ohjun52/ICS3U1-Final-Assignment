import tool
import pygame
import pygame_class

class Battle:

	def __init__(self, path):
		battle_info = tool.read_json(path)
		self.mouse_in_range = pygame_class.FrontSight("images/front_sight_blue.png")
		self.mouse_out_range = pygame_class.FrontSight("images/front_sight_red.png")
		self.player_ship = pygame_class.PlayerShip(battle_info["player_ship_initial_pos"])
		self.bot_ship_group = pygame.sprite.Group()
		for bot_ship in battle_info["bot_ships"]:
			self.bot_ship_group.add(pygame_class.BotShip(f"data/bot_ship/{bot_ship[0]}.json", bot_ship[1]))
		self.player_bullet_list = pygame.sprite.Group()
		pygame_class.PlayerShip.BULLET_LIST = self.player_bullet_list
		self.bot_bullet_list = pygame.sprite.Group()
		pygame_class.BotShip.BULLET_LIST = self.bot_bullet_list

	def hit_detection(self):
		hit_list = pygame.sprite.spritecollide(self.player_ship, self.bot_bullet_list, True)
		for hit_ship in hit_list:
			self.player_ship.hp -= pygame_class.Bullet.BULLET_INFO[hit_ship.bullet_name]["damage"]
		hit_list = pygame.sprite.groupcollide(self.player_bullet_list, self.bot_ship_group, True, False)
		for bullet, hit_ships in hit_list.items():
			for hit_ship in hit_ships:
				hit_ship.hp -= pygame_class.Bullet.BULLET_INFO[bullet.bullet_name]["damage"]
				if hit_ship.hp <= 0:
					hit_ship.kill()

	def run(self, screen):
		clock = pygame.time.Clock()
		pygame.mouse.set_visible(False)
		while self.player_ship.hp > 0:
			if pygame.event.get(pygame.QUIT): break
			tool.update_mouse_pos()
			screen.fill((0, 0, 0))
			self.player_ship.update(screen)
			pygame_class.BotShip.PLAYER_RECT = self.player_ship.rect
			self.bot_ship_group.update(screen)
			self.player_bullet_list.update(screen)
			self.bot_bullet_list.update(screen)
			if self.player_ship.in_attack_range: self.mouse_in_range.update(screen)
			else: self.mouse_out_range.update(screen)
			self.hit_detection()
			pygame.display.flip()
			clock.tick(120)

def main(screen, path):
	battle = Battle(path)
	battle.run(screen)