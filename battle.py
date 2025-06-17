import sys
import tool
import pygame
import pygame_class

class Battle:

	def __init__(self, name):
		battle_info = tool.read_json(f"data/battle_setup/{name}.json")
		self.mouse_in_range = pygame_class.FrontSight("images/front_sight/front_sight_blue.png")
		self.mouse_out_range = pygame_class.FrontSight("images/front_sight/front_sight_red.png")
		self.player_ship = pygame_class.PlayerShip(battle_info["player_ship_initial_pos"])
		self.bot_ship_group = pygame.sprite.Group()
		for bot_ship in battle_info["bot_ships"]:
			self.bot_ship_group.add(pygame_class.BotShip(f"data/bot_ship/{bot_ship[0]}.json", bot_ship[1]))
		self.player_bullet_list = pygame.sprite.Group()
		pygame_class.PlayerShip.BULLET_LIST = self.player_bullet_list
		self.bot_bullet_list = pygame.sprite.Group()
		pygame_class.BotShip.BULLET_LIST = self.bot_bullet_list
		self.hit_effect_cnt = 0
		self.hit_effect_list = {}
		self.hp_font = pygame.font.Font("font/airstrikebold.ttf", 50)
		self.background = pygame.image.load(battle_info["background_image"]).convert()
		self.background = pygame.transform.scale(self.background, tool.SCREEN_SIZE)

	def hit_detection(self):
		hit_list = pygame.sprite.spritecollide(self.player_ship, self.bot_bullet_list, True)
		for hit_bullet in hit_list:
			self.hit_effect_list[self.hit_effect_cnt] = pygame_class.HitEffect("1", hit_bullet.object_rect.center)
			self.hit_effect_cnt += 1
			self.player_ship.hp -= pygame_class.Bullet.BULLET_INFO[hit_bullet.bullet_name]["damage"]
		hit_list = pygame.sprite.groupcollide(self.player_bullet_list, self.bot_ship_group, True, False)
		for bullet, hit_ships in hit_list.items():
			for hit_ship in hit_ships:
				hit_ship.hp -= pygame_class.Bullet.BULLET_INFO[bullet.bullet_name]["damage"]
				self.hit_effect_list[self.hit_effect_cnt] = pygame_class.HitEffect("1", bullet.object_rect.center)
				self.hit_effect_cnt += 1
				if hit_ship.hp <= 0:
					hit_ship.kill()

	def update_hit_effect(self, screen):
		delete_list = []
		for key, value in self.hit_effect_list.items():
			if value.now_index >= value.images_cnt:
				delete_list.append(key)
			else:
				value.update(screen)
		for delete_key in delete_list:
			del self.hit_effect_list[delete_key]

	def run(self, screen):
		pygame.mouse.set_visible(False)
		while self.player_ship.hp > 0:
			for event in pygame.event.get():
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_ESCAPE:
						break
				elif event.type == pygame.QUIT:
					sys.exit()
			tool.update_mouse_pos()
			screen.fill((0, 0, 0))
			screen.blit(self.background, (0, 0))
			self.player_ship.update(screen)
			pygame_class.BotShip.PLAYER_RECT = self.player_ship.object_rect
			self.bot_ship_group.update(screen)
			self.player_bullet_list.update(screen)
			self.bot_bullet_list.update(screen)
			self.hit_detection()
			self.update_hit_effect(screen)
			now_hp = self.hp_font.render(f"HP: {self.player_ship.hp}", True, (0, 221, 225))
			screen.blit(now_hp, (0, 0))
			if self.player_ship.can_attack: self.mouse_in_range.update(screen)
			else: self.mouse_out_range.update(screen)
			pygame.display.flip()
			tool.CLOCK.tick(120)
		pygame.mouse.set_visible(True)