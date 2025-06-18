import tool
import pygame
import random

class ImageObject(pygame.sprite.Sprite):
	def __init__(self, path, initial_pos = (0, 0), scale = 1.0):
		super().__init__()
		self.object = pygame.image.load(path).convert_alpha()
		self.object = pygame.transform.scale(self.object, (self.object.get_width() * scale, self.object.get_height() * scale))
		self.object_rect = self.object.get_rect(center = initial_pos)
		self.rect = self.object_rect.copy()

	def update(self, screen):
		self.rect = self.object_rect.copy()
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

	@staticmethod
	def bullet_hit_effect(bullet_type):
		return Bullet.BULLET_INFO[bullet_type]["hit_effect"]

	def __init__(self, bullet_name, initial_pos, target_pos):
		self.bullet_name = bullet_name
		super().__init__(self.BULLET_INFO[bullet_name]["bullet_image"], initial_pos, self.BULLET_INFO[bullet_name]["scale"])
		self.object = tool.rotate_to_target(self.object, initial_pos, target_pos)
		self.object_rect = self.object.get_rect(center = initial_pos)
		self.x_speed, self.y_speed, self.remain_times = tool.calculate_xy_spead(initial_pos, target_pos, self.BULLET_INFO[bullet_name]["speed"])

	def move(self):
		if self.remain_times > 0:
			self.object_rect.x += self.x_speed
			self.object_rect.y += self.y_speed
			self.remain_times -= 1
		else:
			self.kill()

	def update(self, screen):
		self.move()
		super().update(screen)

class FrontSight(ImageObject):
	def __init__(self, path):
		super().__init__(path, tool.MOUSE_POS, 0.1)

	def update(self, screen):
		self.object_rect.center = tool.MOUSE_POS
		super().update(screen)

class Ship(ImageObject):

	def __init__(self, path, initial_pos):
		self.ship_info = tool.read_json(path)
		super().__init__(self.ship_info["ship_image"], initial_pos)
		self.original_ship = self.object
		self.hp = self.ship_info["initial_hp"]
		self.attack_backswing = 0
		self.current_bullet_index = 0
		self.cooldown_list = [0] * len(self.ship_info["bullet_type"])
		self.bullet_range_rect = tool.get_square(initial_pos, Bullet.bullet_range(self.ship_info["bullet_type"][self.current_bullet_index]))

	def switch_bullet(self, index):
		if index < len(self.ship_info["bullet_type"]):
			self.current_bullet_index = index
			self.bullet_range_rect = tool.get_square(self.object_rect.center, Bullet.bullet_range(self.ship_info["bullet_type"][self.current_bullet_index]))

	def rotate(self, target_pos):
		now_pos = self.object_rect.center
		self.object = tool.rotate_to_target(self.original_ship, now_pos, target_pos, 1)
		self.object_rect = self.object.get_rect(center = now_pos)

	def attack(self, bullet_list, attack_pos):
		bullet_list.add(Bullet(self.ship_info["bullet_type"][self.current_bullet_index], self.object_rect.center, attack_pos))
		self.attack_backswing = Bullet.bullet_backswing(self.ship_info["bullet_type"][self.current_bullet_index])
		self.cooldown_list[self.current_bullet_index] = Bullet.bullet_cooldown(self.ship_info["bullet_type"][self.current_bullet_index])

	def scale_collision_box(self, scale):
		self.rect.width //= scale
		self.rect.height //= scale
		self.rect.center = self.object_rect.center

	def update(self, screen):
		if self.attack_backswing > 0:
			self.attack_backswing -= 1
		for i in range(len(self.cooldown_list)):
			if self.cooldown_list[i] > 0:
				self.cooldown_list[i] -= 1
		super().update(screen)
		self.scale_collision_box(self.ship_info["collision_box_scale"])

class PlayerShip(Ship):

	BULLET_LIST = None

	def __init__(self, initial_pos):
		super().__init__("data/player_ship.json", initial_pos)
		self.can_attack = None

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
		if pressed_keys[pygame.K_1] and self.current_bullet_index != 0:
			self.switch_bullet(0)
		elif pressed_keys[pygame.K_2] and self.current_bullet_index != 1:
			self.switch_bullet(1)
		elif pressed_keys[pygame.K_3] and self.current_bullet_index != 2:
			self.switch_bullet(2)
		tool.correct_in_range(self.object_rect)
		self.bullet_range_rect.center = self.object_rect.center
		self.can_attack = self.bullet_range_rect.collidepoint(tool.MOUSE_POS) and not self.attack_backswing
		if pygame.mouse.get_pressed()[0] and self.can_attack and not self.cooldown_list[self.current_bullet_index]:
			self.attack(PlayerShip.BULLET_LIST, tool.MOUSE_POS)

	def update(self, screen):
		self.rotate(tool.MOUSE_POS)
		self.operate()
		super().update(screen)

class BotShip(Ship):

	BULLET_LIST = None
	PLAYER_RECT = None

	@staticmethod
	def in_range(range_rect, player_rect):
		if range_rect.colliderect(player_rect):
			return True
		return False

	def __init__(self, path, initial_pos):
		super().__init__(path, initial_pos)
		self.warning_range_rect = tool.get_square(initial_pos, self.ship_info["warning_range"])
		self.stop_tracking_range_rect = tool.get_square(initial_pos, self.ship_info["stop_tracking_range"])
		self.running_range = tool.get_square(initial_pos, self.ship_info["running_range"])
		self.wander_x_speed = None
		self.wander_y_speed = None
		self.wander_remain_times = None

	def get_player_rect(self, player_rect):
		self.PLAYER_RECT = player_rect

	def move(self, target_pos, reverse = False):
		x_speed, y_speed, temp = tool.calculate_xy_spead(self.object_rect.center, target_pos, self.ship_info["speed"])
		if reverse:
			x_speed *= -1
			y_speed *= -1
		self.object_rect.x += x_speed
		self.object_rect.y += y_speed

	def wander(self):
		if not self.wander_remain_times:
			wander_pos = random.randint(0, tool.SCREEN_SIZE[0]), random.randint(0, tool.SCREEN_SIZE[1])
			self.wander_x_speed, self.wander_y_speed, self.wander_remain_times = tool.calculate_xy_spead(self.object_rect.center, wander_pos, self.ship_info["speed"])
			self.rotate(wander_pos)
		self.object_rect.x += self.wander_x_speed
		self.object_rect.y += self.wander_y_speed
		self.wander_remain_times -= 1

	def try_attack(self):
		in_range_bullet = []
		for bullet_index in range(len(self.ship_info["bullet_type"])):
			self.switch_bullet(bullet_index)
			if not self.cooldown_list[self.current_bullet_index] and not self.attack_backswing and self.in_range(self.bullet_range_rect, self.PLAYER_RECT):
				in_range_bullet.append(bullet_index)
		if in_range_bullet:
			self.switch_bullet(random.choice(in_range_bullet))
			self.attack(BotShip.BULLET_LIST, self.PLAYER_RECT.center)

	def update(self, screen):
		if self.in_range(self.warning_range_rect, self.PLAYER_RECT):
			self.wander_remain_times = 0
			self.rotate(self.PLAYER_RECT.center)
			if self.in_range(self.running_range, self.PLAYER_RECT):
				self.move(self.PLAYER_RECT.center, True)
			elif not self.in_range(self.stop_tracking_range_rect, self.PLAYER_RECT):
				self.move(self.PLAYER_RECT.center)
		else:
			self.wander()
		tool.correct_in_range(self.object_rect)
		self.warning_range_rect.center = self.object_rect.center
		self.stop_tracking_range_rect.center = self.object_rect.center
		self.running_range.center = self.object_rect.center
		self.try_attack()
		super().update(screen)

class HitEffect:
	info = tool.read_json("data/hit_effect.json")

	def __init__(self, name, pos):
		self.images_list = []
		self.images_cnt = self.info[name][0]
		self.delay = self.info[name][1]
		for i in range(self.images_cnt):
			self.images_list.append(ImageObject(f"images/hit_effect/{name}/{i}.png", pos, 0.6))
		self.now_index = 0
		self.remain = self.delay

	def update(self, screen):
		self.images_list[self.now_index].update(screen)
		self.remain -= 1
		if self.remain <= 0:
			self.now_index = self.now_index + 1
			self.remain = self.delay
