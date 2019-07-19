import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
	if len(bullets) < ai_settings.bullet_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False

def start_game(ai_settings, screen, ship, aliens, bullets, stats, scoreboard):
	#飞船数量减少1
	stats.ships_left -= 1
	print(stats.ships_left)

	ai_settings.initialize_dynamic_settings()
	stats.game_active = True

	scoreboard.prep_score()
	scoreboard.prep_high_score()
	scoreboard.prep_level()
	scoreboard.prep_ships()

	aliens.empty()
	bullets.empty()

	create_fleet(ai_settings, screen, ship, aliens)
	ship.center_ship()

	#隐藏光标
	pygame.mouse.set_visible(False)


def check_play_button(stats, play_button, mouse_x, mouse_y, ship, aliens, bullets, ai_settings, screen, scoreboard):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		stats.reset_all()
		start_game(ai_settings, screen, ship, aliens, bullets, stats, scoreboard)


def check_events(ai_settings, screen, ship, bullets, play_button, stats, aliens, scoreboard):
	'''响应按键和鼠标事件'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)

		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(stats, play_button, mouse_x, mouse_y, ship, aliens, bullets, ai_settings, screen, scoreboard)



def update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, scoreboard):
	'''更新屏幕上的图像，并切换到新屏幕'''
	#每次循环时都重绘屏幕
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	scoreboard.show_socre()
	aliens.draw(screen)

	if not stats.game_active :
		play_button.draw_button()

	for bullet in bullets.sprites():
		bullet.draw_bullet()

	#让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, scoreboard):
	bullets.update()
	#删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, scoreboard)
	
	#print(len(bullets))

def check_high_score(stats, scoreboard):
	if stats.high_socre < stats.score:
		stats.high_socre = stats.score
		scoreboard.prep_high_score()
	
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, scoreboard):
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			scoreboard.prep_score()

		check_high_score(stats, scoreboard)

	if len(aliens) == 0:
		bullets.empty()

		stats.level += 1
		scoreboard.prep_level()

		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, scoreboard):
	'''检查是否有外星人到达屏幕底端'''
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)
			break
	
def update_aliens(ai_settings, aliens, ship, screen, bullets, stats, scoreboard):
	check_fleet_edges(ai_settings, aliens)
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)
	aliens.update()

	if pygame.sprite.spritecollideany(ship, aliens):
		print("Ship hit !!!")
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)


def create_fleet(ai_settings, screen, ship, aliens):
	'''创建外星人群'''
	alien = Alien(screen, ai_settings)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	for row_number in range(number_rows):
		for alien_num in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_num, row_number)

def get_number_aliens_x(ai_settings, alien_width):
	'''计算每行可容纳多少个外星人'''
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))

	return number_aliens_x

def get_number_rows(ai_settings, ship_height,alien_height):
	'''计算可容纳多少行外星人'''
	available_space_y = ai_settings.screen_height - 3*alien_height - ship_height
	number_aliens_y = int(available_space_y / (2 * alien_height))

	return number_aliens_y

def create_alien(ai_settings, screen, aliens, alien_num, row_number):
	'''创建一个外星人并将其放在当前行'''
	alien = Alien(screen, ai_settings)
	alien.x = alien.rect.width + 2 * alien.rect.width * alien_num
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * row_number * alien.rect.height
	aliens.add(alien)

def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edges() :
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	ai_settings.fleet_direction *= -1

	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, scoreboard):
	'''响应外星人撞到的飞船'''
	if stats.ships_left <= 0:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	else:
		start_game(ai_settings, screen, ship, aliens, bullets, stats, scoreboard)

		#暂停
		sleep(1.5)
