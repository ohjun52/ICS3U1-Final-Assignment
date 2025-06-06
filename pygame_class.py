import math
import tool
import pygame

class ImageObject:
	def __init__(self, path, initial_pos = (0, 0), scale = 1.0):
		self.object = pygame.image.load(path).convert_alpha()
		self.object = pygame.transform.scale(self.object, (self.object.get_width() * scale, self.object.get_height() * scale))
		self.object_rect = self.object.get_rect(center = initial_pos)

	def update(self, screen):
		screen.blit(self.object, self.object_rect)

class Bullet(ImageObject):
	BULLET_INFO = tool.read_json("data/bullet_data.json")

	def __init__(self, bullet_number, initial_pos, target_pos):
		self.info = self.BULLET_INFO[bullet_number]
		self.now_pos = initial_pos
		self.target_pos = target_pos
		super().__init__(self.info["bullet_image"], initial_pos)
		self.object = tool.rotate_to_target(self.object, initial_pos, target_pos)
		self.object_rect = self.object.get_rect(center = initial_pos)
		x_len = abs(target_pos[0] - initial_pos[0])
		y_len = abs(target_pos[1] - initial_pos[1])
		self.remain_times = math.sqrt(x_len ** 2 + y_len ** 2) / self.info["speed"]
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
			self.object_rect.center = self.target_pos

	def update(self, screen):
		self.move()
		super().update(screen)

class FrontSight(ImageObject):
	def __init__(self):
		super().__init__("images/front_sight.png", tool.MOUSE_POS, 0.1)

	def front_sight_track(self):
		self.object_rect.center = tool.MOUSE_POS

	def update(self, screen):
		self.front_sight_track()
		super().update(screen)

class PlayerShip(ImageObject):
	SHIP_INFO = tool.read_json("data/player_setup.json")

	def __init__(self, initial_pos):
		super().__init__(self.SHIP_INFO["ship_image"], initial_pos)
		self.pos = initial_pos
		self.original_ship = self.object
		self.bullet_cnt = 0
		self.bullet_list = {}
		self.attack_cooldown = 0

	def rotate(self):
		self.object = tool.rotate_to_target(self.original_ship, self.pos, tool.MOUSE_POS, 1)
		self.object_rect = self.object.get_rect(center = self.pos)

	def operate(self):
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[pygame.K_w]:
			self.object_rect.y -= self.SHIP_INFO["speed"]
		if pressed_keys[pygame.K_s]:
			self.object_rect.y += self.SHIP_INFO["speed"]
		if pressed_keys[pygame.K_a]:
			self.object_rect.x -= self.SHIP_INFO["speed"]
		if pressed_keys[pygame.K_d]:
			self.object_rect.x += self.SHIP_INFO["speed"]
		tool.correct_in_range(self.object_rect)
		self.pos = self.object_rect.center
		if pygame.mouse.get_pressed()[0] and not self.attack_cooldown:
			self.bullet_list[self.bullet_cnt] = Bullet("1", self.pos, tool.MOUSE_POS)
			self.bullet_cnt += 1
			self.attack_cooldown = 10
		elif self.attack_cooldown:
			self.attack_cooldown -= 1

	def attack(self, screen):
		delete_list = []
		for key, value in self.bullet_list.items():
			value.move()
			value.update(screen)
			if not value.remain_times:
				delete_list.append(key)
		for delete_key in delete_list:
			del self.bullet_list[delete_key]

	def update(self, screen):
		self.operate()
		self.rotate()
		self.attack(screen)
		super().update(screen)