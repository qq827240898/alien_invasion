class GameStats():
	'''跟踪游戏统计信息'''

	def __init__(self, ai_settings):
		'''初始化统计信息'''
		self.ai_settings = ai_settings
		self.game_active = False
		self.score = 0
		self.high_socre = 0
		self.level = 1
		self.reset_all()

	def reset_score(self):
		'''初始化再游戏运行期间可能变化的统计信息'''
		print('reset_stats')
		self.score = 0

	def reset_all(self):
		'''初始化再游戏运行期间可能变化的统计信息'''
		print('reset_stats')
		self.score = 0
		self.level = 1
		self.ships_left = self.ai_settings.ship_limit
