class Settting():
	'''存储外星人入侵的所有设置的类'''

	def __init__(self):
		'''初始化游戏的设置'''

		#屏幕设置
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		#飞船设置
		self.ship_speed = 1.5
		self.ship_limit = 3

		#子弹设置
		self.bullet_speed = 2
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullet_allowed = 10

		#敌人设置
		self.alien_speed = 1
		self.alien_points = 10
		self.fleet_drop_speed = 10
		self.fleet_direction = 1

		#以什么样的速度加快游戏节奏
		self.speedup_scale = 1.2

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		self.ship_speed = 1.5
		self.bullet_speed = 2
		self.alien_speed = 0.5
		self.fleet_drop_speed = 10

		#fleet_direction 为1标识向右; -1表示向左
		self.fleet_direction = 1

	def increase_speed(self):
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.fleet_drop_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points* self.speedup_scale)