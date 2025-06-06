import sys
import json
import math
import pygame

MOUSE_POS = (0, 0)
SCREEN_SIZE = (800, 600)

def get_int(intro):
	while True:
		val = input(intro)
		if val.isdigit():
			return int(val)
		print("Invalid input!")  # make sure the input is available

def get_int_in_range(intro, l, r):
	while True:
		val = input(intro)
		if val.isdigit() and l <= int(val) <= r:
			return int(val)
		print("Invalid input!")  # make sure the input is available

def read_json(file_name):  # open json and return
	with open(file_name, "r") as f:
		return json.load(f)

def save_json(file_name, data):  # save json
	with open(file_name, "w") as f:
		json.dump(data, f, indent = 4)

def read_txt(file_name):
	with open(file_name, "r") as f:
		return f.read()  # get all of txt

def read_txt_line(file_name):
	with open(file_name, "r") as f:
		return f.readlines()  # get txt in separate line

def save_txt(file_name, opr, data):
	with open(file_name, opr) as f:
		f.write(data)  # rewrite or add data to txt

def rotate_to_target(original_image, origin_pos, target_pos, head = 0):
	rotate_angle = math.degrees(math.atan2(origin_pos[1] - target_pos[1], target_pos[0] - origin_pos[0])) - head * 90
	return pygame.transform.rotate(original_image, rotate_angle)

def correct_in_range(rect):
	if rect.left < 0:
		rect.left = 0
	if rect.right > SCREEN_SIZE[0]:
		rect.right = SCREEN_SIZE[0]
	if rect.top < 0:
		rect.top = 0
	if rect.bottom > SCREEN_SIZE[1]:
		rect.bottom = SCREEN_SIZE[1]

def quit_game():
	if pygame.event.get(pygame.QUIT):
		sys.exit()

def update_mouse_pos():
	global MOUSE_POS
	MOUSE_POS = pygame.mouse.get_pos()