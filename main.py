from thermal_printer.printer import *
from thermal_printer.constants import ALIGNMENTS
import hexagrams
from collections import abc

""" Test printing data with print_data """

FORMAT = {
	'name' : {'options' : {'set_alignment' : ALIGNMENTS.M, 'set_bold': True}},
	'name_chinese' : {'options' : {'set_alignment' : ALIGNMENTS.M, 'set_bold': True, 'space' : True}},
	'judgement' : {'options' : {'space' : True}, 'title' : 'Judgement'},
	'image' : {'options' : {'space' : True}, 'title' : 'Image'},
	'lines' : {'options' : {'set_alignment' : ALIGNMENTS.M, 'set_row_spacing':0, 'space' : True}},
	'emph_lines' : {'options' : {'set_bold':True, 'space': True}, 'title' : "Emphasized Lines"},
	'normal_lines' : {'options' : {'space' : True}, 'title' : "Normal Lines"},
	'default' : {'options':{'space' : True}},
	'chinese_defualt' : 
		{'options':{'space' : True, 'set_chinese_mode' : True, 'set_chinese_format' : CHINESE.UTF8}},
	'title' : {'options': {'set_bold' : True, 'set_alignment' : ALIGNMENTS.M, 'set_underline' : True}}
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

	def make_line(line, options):
		line_template = {"type" : "text", "info" : '', "options" : {}}

		try:
			if is_chinese(line):
				line_template.update(FORMAT['chinese_defualt'])
		except:
			print("Uh oh this caused a woopsy poopsy error: {}".format(line))

		line_template['info'] = line
		line_template['options'].update(options)

		return line_template

	print_data = []

	for k, v in dict_iter(reading):

		if k not in FORMAT.keys():
			k = 'default'

		options = FORMAT[k]['options']

		if 'title' in FORMAT[k]:
			print_data.append(make_line(FORMAT[k]['title'], FORMAT['title']['options']))

		if k is "lines":
			for line in v:
				print_data.append(make_line(hexagrams.YiJingLineTrans[line], options))

		elif k is "emph_lines" or k is "normal_lines":
			for line in v:
				print_data.append(make_line(line, options))

		else:
			print_data.append(make_line(v, options))

		if 'space' in options and options['space']:	
			print_data.append(make_line("", {}))

	return print_data

def make_reading(h):

	r_hex = {}
	info = h.info

	r_hex['name'] = info['name']
	r_hex['name_chinese'] = info['name_chinese']

	r_hex['lines'] = [x.val for x in h.lines]

	r_hex['judgement'] = info['judgement']
	r_hex['judgement_chinese'] = info['judgement_chinese']

	r_hex['image'] = info['image']
	r_hex['image_chinese'] = info['image_chinese']


	if h.moving:
		r_hex['normal_lines'] = []

	if h.moving > 1 and h.moving < 6:
		r_hex['emph_lines'] = []

	if h.moving == 1:
		r_hex['normal_lines'].append(info['line{}'.format(h.moving_pos[0])])
	elif h.moving == 2:
		r_hex['emph_lines'].append(info['line{}'.format(h.moving_pos[1])])
		r_hex['normal_lines'].append(info['line{}'.format(h.moving_pos[0])])
	elif h.moving == 3:
		pass

	return r_hex


if __name__ == '__main__':
	hexagram = hexagrams.YijingHexagram()

	while hexagram.moving != 1:
		hexagram = hexagrams.YijingHexagram()

	formatted_reading = format_reading(make_reading(hexagram))

	# p = DFR0503()
	# print_data(formatted_reading, p)
	# p.feed(2)