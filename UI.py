import tool
import pygame

class InteractionBox:

	def __init__(self, text, pos_scale, size, color, next_state, font = None):
		now_font = pygame.font.Font(font, size)
		self.object = now_font.render(text, True, color)
		self.object_rect = self.object.get_rect()
		self.object_rect.center = tool.SCREEN_SIZE[0] * pos_scale[0], tool.SCREEN_SIZE[1] * pos_scale[1]
		self.rect = self.object_rect.copy()
		self.rect.width += size
		self.rect.height += size
		self.rect.center = self.object_rect.center
		self.next_state = next_state

	def update(self, screen):
		pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
		screen.blit(self.object, self.object_rect)

class Menu:

	TEXT_FONT = "font/Rolie Twily.otf"

	def __init__(self, name):
		info = tool.read_json(f"data/menu_setup/{name}.json")
		self.interaction_list = []
		self.background = pygame.image.load(info["background_image"]).convert()
		self.background = pygame.transform.scale(self.background, tool.SCREEN_SIZE)
		for info in info["interaction_box"]:
			self.interaction_list.append(InteractionBox(info[0], info[1], info[2], info[3], info[4], self.TEXT_FONT))
		self.return_val = None

	def interact(self):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					for interaction in self.interaction_list:
						if interaction.rect.collidepoint(tool.MOUSE_POS):
							self.return_val = interaction.next_state
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					self.return_val = ["menu", "main"]
			elif event.type == pygame.QUIT:
				self.return_val = ["", ""]


	def run(self, screen):
		while self.return_val is None:
			tool.update_mouse_pos()
			screen.fill((0, 0, 0))
			screen.blit(self.background, (0, 0))
			for interaction in self.interaction_list:
				interaction.update(screen)
			pygame.display.flip()
			tool.CLOCK.tick(120)
			self.interact()
		return self.return_val

class Plot:
	TEXT_FONT = "font/Emigrate.otf"
	TEXT_SIZE = 50
	TEXT_COLOR = (255, 255, 255)

	def __init__(self, name):
		info = tool.read_json(f"data/plot_text/{name}.json")
		self.background = pygame.image.load(info["background_image"]).convert()
		self.background = pygame.transform.scale(self.background, tool.SCREEN_SIZE)
		font = pygame.font.Font(self.TEXT_FONT, self.TEXT_SIZE)
		words = info["text"].split(" ")
		self.lines = []
		line = " "
		for word in words:
			test_line = line + word + " "
			if font.size(test_line)[0] > tool.SCREEN_SIZE[0]:
				self.lines.append(font.render(line.strip(), True, self.TEXT_COLOR))
				line = word + " "
			else:
				line = test_line
		if line:
			self.lines.append(font.render(line.strip(), True, self.TEXT_COLOR))
		self.dialog_box_height = len(self.lines) * self.TEXT_SIZE + self.TEXT_SIZE * 2
		self.dialog_box = pygame.Surface((tool.SCREEN_SIZE[0], self.dialog_box_height), pygame.SRCALPHA)
		self.dialog_box.fill((128, 128, 128, 64))
		self.next_state = info["next"]
		self.back_state = info["back"]
		self.return_val = None

	def interact(self):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.return_val = self.next_state
				elif event.button == 3:
					self.return_val = self.back_state
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					self.return_val = ["menu", "main"]
			elif event.type == pygame.QUIT:
				self.return_val = ["", ""]

	def run(self, screen):
		while self.return_val is None:
			screen.fill((0, 0, 0))
			screen.blit(self.background, (0, 0))
			screen.blit(self.dialog_box, (0, tool.SCREEN_SIZE[1] - self.dialog_box_height))
			blit_height = tool.SCREEN_SIZE[1] - self.TEXT_SIZE
			for i in range(len(self.lines) - 1, -1, -1):
				blit_height = blit_height - self.TEXT_SIZE
				screen.blit(self.lines[i], (0, blit_height))
			pygame.display.flip()
			tool.CLOCK.tick(120)
			self.interact()
		return self.return_val