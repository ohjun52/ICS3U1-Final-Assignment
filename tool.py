import json
import math
import pygame

MOUSE_POS = (0, 0)
SCREEN_SIZE = (0, 0)
CLOCK = pygame.time.Clock()

def read_json(file_name):  # open json and return
	with open(file_name, "r") as f:
		return json.load(f)

def save_json(file_name, data):  # save json
	with open(file_name, "w") as f:
		json.dump(data, f, indent = 4)

def rotate_to_target(original_image, origin_pos, target_pos, head = 0):
	rotate_angle = math.degrees(math.atan2(origin_pos[1] - target_pos[1], target_pos[0] - origin_pos[0])) - head * 90
	return pygame.transform.rotate(original_image, rotate_angle)

def calculate_xy_spead(origin_pos, target_pos, speed):
	x_len = abs(target_pos[0] - origin_pos[0])
	y_len = abs(target_pos[1] - origin_pos[1])
	remain_times = math.sqrt(x_len ** 2 + y_len ** 2) / speed
	if remain_times < 1:
		return 0, 0, 0
	x_speed = x_len / remain_times
	if origin_pos[0] > target_pos[0]:
		x_speed *= -1
	y_speed = y_len / remain_times
	if origin_pos[1] > target_pos[1]:
		y_speed *= -1
	return x_speed, y_speed, int(remain_times)

def get_square(center_pos, length):
	rect = pygame.Rect(0, 0, length, length)
	rect.center = center_pos
	return rect

def correct_in_range(rect):
	if rect.left < 0:
		rect.left = 0
	if rect.right > SCREEN_SIZE[0]:
		rect.right = SCREEN_SIZE[0]
	if rect.top < 0:
		rect.top = 0
	if rect.bottom > SCREEN_SIZE[1]:
		rect.bottom = SCREEN_SIZE[1]

def update_mouse_pos():
	global MOUSE_POS
	MOUSE_POS = pygame.mouse.get_pos()
