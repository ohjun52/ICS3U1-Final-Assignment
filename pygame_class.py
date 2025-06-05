import math
import tool
import pygame
from main import screen

class ImageObject:
	def __init__(self, path, initial_pos = (0, 0), x = 100, y = 100):
		self.object = pygame.image.load(path).convert_alpha()
		self.object = pygame.transform.scale(self.object, (x, y))
		self.object_rect = self.object.get_rect(center = initial_pos)

class FrontSight(ImageObject):
	def __init__(self):
		super().__init__("images/front_sight.png", pygame.mouse.get_pos())
		self.pos = pygame.mouse.get_pos()

	def front_sight_track(self):
		self.pos = pygame.mouse.get_pos()
		self.object_rect.center = self.pos

	def update(self):
		screen.blit(self.object, self.object_rect)

class PlayerShip(ImageObject):
	SHIP_INFO = tool.read_json("player_setup.json")

	def __init__(self, initial_pos):
		super().__init__(self.SHIP_INFO["ship_image"], initial_pos)
		self.pos = pygame.mouse.get_pos()
		self.original_ship = pygame.image.load(self.SHIP_INFO["ship_image"])

	def update(self):
		screen.blit(self.object, self.object_rect)

	def rotate(self, rotate_pos):
		ship_pos = self.object_rect.center
		rotate_angle = math.degrees(math.atan2(ship_pos[1] - rotate_pos[1], rotate_pos[0] - ship_pos[0])) - 90
		self.object = pygame.transform.rotate(self.original_ship, rotate_angle)
		self.object_rect = self.object.get_rect(center = ship_pos)

	def move(self):
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[pygame.K_w]:
			self.object_rect.y -= 10
		if pressed_keys[pygame.K_s]:
			self.object_rect.y += 10
		if pressed_keys[pygame.K_a]:
			self.object_rect.x -= 10
		if pressed_keys[pygame.K_d]:
			self.object_rect.x += 10
		tool.correct_in_range(self.object_rect)