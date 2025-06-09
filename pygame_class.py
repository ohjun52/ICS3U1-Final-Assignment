import math
import tool
import pygame

class ImageObject(pygame.sprite.Sprite):
	def __init__(self, path, initial_pos = (0, 0), scale = 1.0):
		super().__init__()
		self.object = pygame.image.load(path).convert_alpha()
		self.object = pygame.transform.scale(self.object, (self.object.get_width() * scale, self.object.get_height() * scale))
		self.object_rect = self.object.get_rect(center = initial_pos)

	def update(self, screen):
		screen.blit(self.object, self.object_rect)

class Bullet(ImageObject):
	BULLET_INFO = tool.read_json("data/bullet_data.json")

	@staticmethod
	def bullet_range(bullet_type):
		return Bullet.BULLET_INFO[bullet_type]["range"]

	@staticmethod
	def bullet_cooldown(bullet_type):
		return Bullet.BULLET_INFO[bullet_type]["cooldown"]

	@staticmethod
	def bullet_backswing(bullet_type):
		return Bullet.BULLET_INFO[bullet_type]["backswing"]

	def __init__(self, bullet_number, initial_pos, target_pos):
		self.now_pos = initial_pos
		self.target_pos = target_pos
		super().__init__(self.BULLET_INFO[bullet_number]["bullet_image"], initial_pos, self.BULLET_INFO[bullet_number]["scale"])
		self.object = tool.rotate_to_target(self.object, initial_pos, target_pos)
		self.object_rect = self.object.get_rect(center = initial_pos)
		x_len = abs(target_pos[0] - initial_pos[0])
		y_len = abs(target_pos[1] - initial_pos[1])
		self.remain_times = math.sqrt(x_len ** 2 + y_len ** 2) / self.BULLET_INFO[bullet_number]["speed"]
		self.x_speed = x_len / self.remain_times
		if initial_pos[0] > target_pos[0]:
			self.x_speed *= -1
		self.y_speed = y_len / self.remain_times
		if initial_pos[1] > target_pos[1]:
			self.y_speed *= -1
		self.remain_times = int(self.remain_times)

	def move(self):
		if self.remain_times > 0:
			self.now_pos = (self.now_pos[0] + self.x_speed, self.now_pos[1] + self.y_speed)
			self.object_rect.center = self.now_pos
			self.remain_times -= 1
		else:
			self.kill()

	def update(self, screen):
		self.move()
		super().update(screen)

class BulletList:
	def __init__(self):
		self.bullet_group = pygame.sprite.Group()

	def add(self, bullet_number, initial_pos, target_pos):
		self.bullet_group.add(Bullet(bullet_number, initial_pos, target_pos))

	def update(self, screen):
		self.bullet_group.update(screen)

class FrontSight(ImageObject):
	def __init__(self, path):
		super().__init__(path, tool.MOUSE_POS, 0.1)

	def front_sight_track(self):
		self.object_rect.center = tool.MOUSE_POS

	def update(self, screen):
		self.front_sight_track()
		super().update(screen)

class Ship(ImageObject):

	def __init__(self, path, initial_pos):
		self.ship_info = tool.read_json(path)
		super().__init__(self.ship_info["ship_image"], initial_pos)
		self.original_ship = self.object
		self.hp = self.ship_info["initial_hp"]
		self.bullet_list = BulletList()
		self.attack_backswing = 0
		self.current_bullet_index = 0
		self.cooldown_list = [0] * len(self.ship_info["bullet_type"])
		curren_range = Bullet.bullet_range(self.ship_info["bullet_type"][self.current_bullet_index])
		self.bullet_range_rect = pygame.Rect(self.object_rect.x, self.object_rect.y, curren_range, curren_range)

	def switch_bullet(self, index):
		self.current_bullet_index = index
		curren_range = Bullet.bullet_range(self.ship_info["bullet_type"][self.current_bullet_index])
		self.bullet_range_rect = pygame.Rect(self.object_rect.x, self.object_rect.y, curren_range, curren_range)

	def rotate(self, target_pos):
		now_pos = self.object_rect.center
		self.object = tool.rotate_to_target(self.original_ship, now_pos, target_pos, 1)
		self.object_rect = self.object.get_rect(center = now_pos)

	def attack(self, attack_pos):
		if not self.cooldown_list[self.current_bullet_index] and not self.attack_backswing and self.bullet_range_rect.collidepoint(attack_pos):
			self.bullet_list.add(self.ship_info["bullet_type"][self.current_bullet_index], self.object_rect.center, tool.MOUSE_POS)
			self.attack_backswing = Bullet.bullet_backswing(self.ship_info["bullet_type"][self.current_bullet_index])
			self.cooldown_list[self.current_bullet_index] = Bullet.bullet_cooldown(self.ship_info["bullet_type"][self.current_bullet_index])
		else:
			if self.attack_backswing > 0:
				self.attack_backswing -= 1
			for i in range(len(self.cooldown_list)):
				if self.cooldown_list[i] > 0:
					self.cooldown_list[i] -= 1

	def update(self, screen):
		self.bullet_list.update(screen)
		super().update(screen)

class PlayerShip(Ship):

	def __init__(self, initial_pos):
		super().__init__("data/player_ship.json", initial_pos)

	def operate(self):
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[pygame.K_w]:
			self.object_rect.y -= self.ship_info["speed"]
		if pressed_keys[pygame.K_s]:
			self.object_rect.y += self.ship_info["speed"]
		if pressed_keys[pygame.K_a]:
			self.object_rect.x -= self.ship_info["speed"]
		if pressed_keys[pygame.K_d]:
			self.object_rect.x += self.ship_info["speed"]
		tool.correct_in_range(self.object_rect)
		self.bullet_range_rect.center = self.object_rect.center
		if pygame.mouse.get_pressed()[0]:
			self.attack(tool.MOUSE_POS)


	def update(self, screen):
		self.rotate(tool.MOUSE_POS)
		self.operate()
		super().update(screen)

class BotShip(Ship):

	@staticmethod
	def in_range(range_rect, player_rect):
		if range_rect.colliderect(player_rect):
			return True
		return False

	def __init__(self, path, initial_pos):
		super().__init__(path, initial_pos)
		self.warning_range_rect = pygame.Rect(self.object_rect.x, self.object_rect.y, self.ship_info["warning_range"], self.ship_info["warning_range"])
		self.player_rect = None

	def get_player_rect(self, player_rect):
		self.player_rect = player_rect

	def update(self, screen):
		if self.in_range(self.warning_range_rect, self.player_rect):
			self.rotate(self.player_rect.center)
		super().update(screen)