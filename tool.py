import sys
import json
import pygame

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

def correct_in_range(rect):
	if rect.left < 0:
		rect.left = 0
	if rect.right > 1200:
		rect.right = 1200
	if rect.top < 0:
		rect.top = 0
	if rect.bottom > 700:
		rect.bottom = 700

def quit_game():
	if pygame.event.get(pygame.QUIT):
		sys.exit()