from enum import Enum

class PREFIX(Enum):
	ESC = 27
	LF = 10
	CR = 13
	HT = 9
	GS = 29
	FS = 28
	DC2 = 18	

class COMMANDS(Enum):

	INIT = [PREFIX.ESC.value, 64]
	CHANGE_HEAT = [PREFIX.ESC.value, 55]
	STATUS = [PREFIX.ESC.value, 118, 0]
	FEED = [PREFIX.ESC.value, 100]
	SETTABS = [PREFIX.ESC.value, 68]
	TAB = [PREFIX.HT.value]
	ROWSPACING = [PREFIX.ESC.value, 51]
	ROWSPACINGDEFAULT = [PREFIX.ESC.value, 50]
	BITMAP = [PREFIX.GS.value, 118, 48, 0]
	ALIGN = [PREFIX.ESC.value, 97]
	MARGIN = [PREFIX.ESC.value, 66]
	CHRHEIGHT = [PREFIX.GS.value, 33]
	INVERSE = [PREFIX.GS.value, 66]
	ROTATE = [PREFIX.ESC.value, 86]
	FONT = [PREFIX.ESC.value, 33]
	BOLD = [PREFIX.ESC.value, 69] #nice
	RIGHTSPACE = [PREFIX.ESC.value, 32]
	UPSIDEDOWN = [PREFIX.ESC.value, 123]
	UNDERLINE = [PREFIX.ESC.value, 45]
	CHINESE_ON = [PREFIX.FS.value, 38]
	CHINESE_OFF = [PREFIX.FS.value, 46]
	CHINESE_FORMAT = [PREFIX.ESC.value, 57]
	CODEPAGE = [PREFIX.ESC.value, 116]

class CHINESE(Enum):
	GBK2312 = (0, 'gb2312')
	UTF8 = (1, 'utf-8') 
	BIG5 = (2, 'big5')

class ALIGNMENTS(Enum):
	L = 0
	M = 1
	R = 2