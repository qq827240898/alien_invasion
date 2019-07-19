
import pygame
from settings import Settting
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	#初始化游戏并创建一个满屏对象
	pygame.init()
	ai_settings = Settting()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")

	stats = GameStats(ai_settings)

	play_button = Button(ai_settings, screen, "Play")
	scoreboard = Scoreboard(ai_settings, screen, stats)
	#设置背景色
	bg_color = ai_settings.bg_color

	ship = Ship(screen, ai_settings)

	bullets = Group()
	aliens = Group()

	#alien = Alien(screen, ai_settings)
	gf.create_fleet(ai_settings, screen, ship, aliens)

	#开始游戏的主循环
	while True:
		#监视键盘和鼠标事件
		gf.check_events(ai_settings, screen, ship, bullets, play_button, stats, aliens, scoreboard)

		if stats.game_active :
			ship.update()
			gf.update_bullets(bullets, aliens, ai_settings, screen, ship, stats, scoreboard)
			gf.update_aliens(ai_settings, aliens, ship, screen, bullets, stats, scoreboard)

		gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, scoreboard)

run_game()