import random
from enum import Enum
import sqlite3
from sqlite3 import Error

COIN_FLIPS = 3
TRIGRAM_LINES = 3
DATABASE = "../data/hex"

class CoinStates(Enum):
	HEADS = 0
	TAILS = 1
	DEFAULT = "Not Flipped"

class YijingCoinStates(Enum):
	HEADS = 3
	TAILS = 2
	DEFAULT = "Not Flipped"

YijingLineStates = {
	0 : "Undetermined",
	7 : "Unmoving Yang",
	8 : "Unmoving Yin",
	6: "Moving Yin",
	9: "Moving Yang"
}

YiJingLineTrans = {
	6 : "-------x------- (T) (T) (T)",
	7 : "--------------- (H) (T) (T)",
	8 : "------- ------- (H) (H) (T)",
	9 : "-------o------- (H) (H) (H)"
}

YijingResolutions = {
	6 : 7,
	9 : 8
}

MOVING = [6, 9]

def db_connect(db_name):
	conn = None
	try:
		conn = sqlite3.connect(db_name)
		conn.row_factory = sqlite3.Row
	except Error as e:
		print(e)

	return conn

class Coin(object):
	"""Coin object
	state - current integer state of coin

	flip() flip the coin and return state
	"""
	def __init__(self):
		self._state = None

	def flip(self):
		self._state = random.choice((CoinStates.HEADS, CoinStates.TAILS))
		return self._state

	@property
	def state(self):
		if self._state:
			return self._state
		else:
			return CoinStates.DEFAULT.value

	def __str__(self):
		return self.status

	def __repr__(self):
		return "Coin: {}".format(self.state)



class YijingCoin(Coin):
	"""YiJing coin object, like a normal coin, but with different
	 	values for heads and tails

	 	flip() flip the cound and return status
	 	status() get current state of coin

	 	state - current state of coin
	 	"""
	
	def flip(self):
		self._state = random.choice((YijingCoinStates.HEADS, YijingCoinStates.TAILS))
		return self._state
		

class YijingLine(object):
	"""
	Yijing line object, can yin, yang, moving yin, or moving yang
	
	data:
	val - current value of line (6, 7, 8, 9)
	moving - boolean value for if the line is moving or not
	name - name of line (moving yang, moving yin, unmoving yang, unmoving yin)
	bin - return binary value of line: 1 for yang, 0 for yin

	methods:
	build() - generate a value for the line, return object
	resolve() - if the line is moving, returns a new YijingLine object with the final
	line value
	"""

	def __init__(self, ini=0):
		self.val = ini
		self.coins = []

		#don't rebuild if supplied with initializating data
		if not ini:
			self.build()

	def build(self):
		self.val = 0
		self.coins = []

		for i in range(COIN_FLIPS):
			c = YijingCoin()
			c.flip()
			self.val += c.state.value
			self.coins.append(c)

		return self

	@property
	def moving(self):
		return self.val in MOVING

	@property
	def name(self):
		return YijingLineStates[self.val]

	@property
	def bin(self):
		#yin are even numbers, yang are odd numbers

		return self.val % 2

	def resolve(self):
		if self.moving:
			return YijingLine(YijingResolutions[self.val])
		return self

	def __str__(self):
		return YiJingLineTrans[self.val]

	def __repr__(self):
		return "Yijing Line: {}, {}".format(self.val, self.name)

class YijingTrigram(object):
	"""
	Yijing Trigram object. Value is composed of three Yijing Lines

	data:
	lines: list containing three YijingLines
	bin - list containing binary values of lines

	methods:
	build() -- build a new trigram of three YijingLines, return current object
	get_name() -- return name of trigram
	count_moving() -- return number of moving lines	
	"""

	def __init__(self, ini=[]):
		self.lines = ini
		self.info = None

		#don't rebuild if supplied with initializing data
		if ini:
			self.__lookup()
		else:
			self.build()

	def __lookup(self):
		with db_connect(DATABASE) as conn:
			cur = conn.cursor()
			cur.execute("SELECT * FROM Trigrams WHERE id=?", 
				(''.join(map(str, self.bin)), ))
			self.info = cur.fetchone()

	def build(self):
		self.lines = []

		for i in range(TRIGRAM_LINES):
			self.lines.append(YijingLine())

		self.__lookup()

		return self

	def resolve(self):
		res_lines = [l.resolve() for l in self.lines]
		return YijingTrigram(res_lines)

	@property
	def moving(self):
		return sum([x.moving for x in self.lines])

	@property
	def bin(self):
		return [x.bin for x in self.lines]

	def __repr__(self):
		return "Name: {} \n Lines: {}".format(self.info['name'], 
												self.lines)

class YijingHexagram(object):

	def __init__(self, ini=[]):
		self.trigrams = ini
		self.info = None

		if ini:
			self.__lookup()
		else:
			self.build()

	def __lookup(self):
		with db_connect(DATABASE) as conn:
			cur = conn.cursor()
			cur.execute("SELECT * FROM Hexagrams WHERE id=?", 
				(''.join(map(str, self.bin)), ))
			self.info = cur.fetchone()

	def build(self):
		self.trigrams = [YijingTrigram(), YijingTrigram()]
		self.__lookup()

	def resolve(self):
		t = [t.resolve() for t in self.trigrams]
		return YijingHexagram(t)

	@property
	def lines(self):
		"""Return list of line objects composing two trigrams"""
		lines = []
		for t in self.trigrams:
			for line in t.lines:
				lines.append(line)
		return lines

	@property
	def moving(self):
		return sum([line.moving for line in self.lines])

	@property
	def moving_pos(self):
		return [i for i, x in enumerate(reversed(self.lines)) if x.moving == True]

	@property
	def appearance(self):
		return "\n".join([str(line) for line in reversed(self.lines)])

	@property
	def bin(self):
		binary = []
		for t in self.trigrams:
			for line in t.lines:
				binary.append(line.bin)
		return binary


	def __repr__(self):		
		return "Name: {} Chinese name: {} Moving lines: {}".format(self.info['name'], self.info['chinese_name'], self.moving)