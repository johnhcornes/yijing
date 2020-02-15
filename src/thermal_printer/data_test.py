from printer import *
from constants import ALIGNMENTS
from collections import abc

""" Test printing data with print_data """

FORMAT = {
	'name' : {'options' : {'set_alignment' : ALIGNMENTS.M, 'set_bold': True}},
	'name_chinese' : {'options' : {'set_alignment' : ALIGNMENTS.M, 'set_bold': True}},
	'judgement' : {'options' : {}, 'title' : 'Judgement'},
	'image' : {'options' : {}, 'title' : 'Image'},
	'lines' : {'options' : {'set_alignment' : ALIGNMENTS.M, 'set_row_spacing':0}},
	'emph_lines' : {'options' : {'set_bold':True}, 'title' : "Emphasized Lines"},
	'normal_lines' : {'options' : {}, 'title' : "Normal Lines"},
	'default' : {'options':{}},
	'chinese_defualt' : 
		{'options':{'set_chinese_mode' : True, 'set_chinese_format' : CHINESE.UTF8}},
	'title' : {'options': {'set_bold' : True, 'set_alignment' : ALIGNMENTS.M, 'set_underline' : True}}
}

reading = {
	'hex' : {
		'name' : "Qian",
		'name_chinese' : "乾",
		'lines' : [7, 7, 7, 7, 7, 7],
		'judgement' : 'The creative works sublime success,\nFurthering through perseverance.',
		'judgement_chinese' : '大哉乾元，萬物資始，乃統天。雲行雨施，品物流形。大明始終，六位時成，時乘六龍以御天。乾道變化，各正性命，保合大和，乃利貞。首出庶物，萬國咸寧。',
		'image' : 'The movement of heaven is full of power.\nThus the superior man makes himself strong and untiring.',
		'image_chinese' : '天行健，君子以自強不息。'
	},

	'emph_lines' : ["This is a line test", "Here we go, testing the lines"],
	'normal_lines' : ["These are normal lines", "they aren't bold"]
}

YiJingLineTrans = {
	6 : "-------x------- (T) (T) (T)",
	7 : "--------------- (H) (T) (T)",
	8 : "------- ------- (H) (H) (T)",
	9 : "-------o------- (H) (H) (H)"
}

def dict_iter(d):
	for key, value in d.items():
		if isinstance(value, abc.Mapping):
			yield from dict_iter(value)
		else:
			yield key, value

def is_chinese(text):
	#yes this is dumb

	for c in text:
		if ord(c) > 255:
			return True
	return False

def format_reading(reading):

	print_data = []

	def make_line(line, options):
		line_template = {"type" : "text", "info" : '', "options" : {}}

		if is_chinese(line):
			line_template.update(FORMAT['chinese_defualt'])

		line_template['info'] = line
		line_template['options'].update(options)

		return line_template

	for k, v in dict_iter(reading):

		if k not in FORMAT.keys():
			k = 'default'

		options = FORMAT[k]['options']

		if 'title' in FORMAT[k]:
			print_data.append(make_line(FORMAT[k]['title'], FORMAT['title']['options']))

		if k is "lines":
			for line in v:
				print_data.append(make_line(YiJingLineTrans[line], options))

		elif k is "emph_lines" or k is "normal_lines":
			for line in v:
				print_data.append(make_line(line, options))

		else:
			print_data.append(make_line(v, options))
		
		print_data.append(make_line("", {}))



	return print_data



if __name__ == '__main__':
	import pprint

	pp = pprint.PrettyPrinter(indent=4)

	formatted_reading = format_reading(reading)
	# pp.pprint(formatted_reading)
	p = DFR0503()
	print_data(formatted_reading, p)
	p.feed(2)