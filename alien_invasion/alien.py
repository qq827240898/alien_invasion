import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	'''单个外星人类'''
	def __init__(self, screen, ai_settings):
		'''初始化外星人并设置其起始位置'''
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		self.x = float(self.rect.x)

	def blitme(self):
		'''指定位置绘制外星人'''
		self.screen.blit(self.image, self.rect)

	def update(self):
		'''左右移动外星人'''
		self.x += self.ai_settings.alien_speed * self.ai_settings.fleet_direction
		self.rect.x = self.x

	def check_edges(self):
		'''如果外星人位于屏幕边缘，就返回True'''
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right :
			return True
		elif self.rect.left <= 0:
			return True
		

