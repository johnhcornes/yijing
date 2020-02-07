from printer import *
from constants import ALIGNMENTS

""" Test printing data with print_data """

data = [
	{'type':'text', 'info': '乾',
	'options': {'set_chinese_mode' : True,  'set_alignment' : ALIGNMENTS.M,
	 'set_chinese_format' : CHINESE.UTF8}},
	{'type':'text', 'info': 'Qian', 
	'options' : {'set_bold' : True, 'set_alignment' : ALIGNMENTS.M}},
	{'type': 'text', 'info' : '---------------', 'options' : {'set_alignment' : ALIGNMENTS.M, 
	'set_row_spacing' : 0}},
	{'type': 'text', 'info' : '---------------', 'options' : {'set_alignment' : ALIGNMENTS.M, 
	'set_row_spacing' : 0}},
	{'type': 'text', 'info' : '---------------', 'options' : {'set_alignment' : ALIGNMENTS.M, 
	'set_row_spacing' : 0}},
	{'type': 'text', 'info' : '---------------', 'options' : {'set_alignment' : ALIGNMENTS.M, 
	'set_row_spacing' : 0}},
	{'type': 'text', 'info' : '---------------', 'options' : {'set_alignment' : ALIGNMENTS.M, 
	'set_row_spacing' : 0}},
	{'type': 'text', 'info' : '---------------', 'options' : {'set_alignment' : ALIGNMENTS.M, 
	'set_row_spacing' : 0}},
	{'type':'text', 'info': 'Judgement', 
	'options': {'set_bold' : True, 'set_alignment': ALIGNMENTS.M, 'set_underline' : True}},
	{'type':'text', 'info': '大哉乾元，萬物資始，乃統天。雲行雨施，品物流形。大明始終，六位時成，時乘六龍以御天。乾道變化，各正性命，保合大和，乃利貞。首出庶物，萬國咸寧。',
	'options': {'set_chinese_mode' : True, 'set_chinese_format' : CHINESE.UTF8}},
	{'type':'text', 'info':'The creative works sublime success,\nFurthering through perseverance.\n',
	'options' : {}},
	{'type':'text', 'info': 'Image', 
	'options': {'set_bold' : True, 'set_alignment': ALIGNMENTS.M, 'set_underline' : True}},
	{'type':'text', 'info': '天行健，君子以自強不息。',
	'options': {'set_chinese_mode' : True, 'set_chinese_format' : CHINESE.UTF8}},
	{'type':'text', 'info':'The movement of heaven is full of power.\nThus the superior man makes himself strong and untiring.',
	'options' : {}}
]

if __name__ == '__main__':
	p = DFR0503()
	print_data(data, p)