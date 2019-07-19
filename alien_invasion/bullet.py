import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	'''一个对飞船发射的子弹进行管理的类'''

	def __init__(self, ai_settings, screen, ship):
		super().__init__()

		self.screen = screen
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		self.y = float(self.rect.y)
		self.color = ai_settings.bullet_color
		self.bullet_speed = ai_settings.bullet_speed

	def update(self):
		self.y -= self.bullet_speed
		self.rect.y = self.y

	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)

