from thermal_printer.printer import *
from thermal_printer.constants import ALIGNMENTS
import hexagrams
from collections import abc

""" Test printing data with print_data """

FORMAT = {
	'name' : {'options' : {'set_alignment' : ALIGNMENTS.M, 'set_bold': True}},
	'name_chinese' : {'options' : {'set_alignment' : ALIGNMENTS.M, 'set_bold': True, 'space' : True}},
	'reading' : {'options' : {'space' : True}, 'title' : 'Reading'},
	'judgement' : {'options' : {'space' : True}, 'title' : 'Judgement'},
	'image' : {'options' : {'space' : True}, 'title' : 'Image'},
	'lines' : {'options' : {'set_alignment' : ALIGNMENTS.M, 'set_row_spacing':0, 'space' : True}},
	'emph_lines' : {'options' : {'set_bold':True, 'space': True }, 'title' : "Emphasized Lines:"},
	'normal_lines' : {'options' : {'space' : True}, 'title' : "Lines:"},
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
			if v:
				for line in v:
					print_data.append(make_line(line, options))

		else:
			print_data.append(make_line(v, options))

		if 'space' in options and options['space']:	
			print_data.append(make_line("", {}))

	return print_data

def make_reading(h):

	line_type = ["line{}", "line{}_chinese"]

	def hex_header(h):
		header = {}

		header['name'] = h.info['name']
		header['name_chinese'] = h.info['name_chinese']

		header['lines'] = reversed([x.val for x in h.lines])

		header['judgement'] = h.info['judgement']
		header['judgement_chinese'] = h.info['judgement_chinese']

		header['image'] = h.info['image']
		header['image_chinese'] = h.info['image_chinese']

		return header


	def add_lines(where, *which):
		for n in which:
			where.extend(
				"{}. {}".format(n+1, h.info[x.format(n)]) for x in line_type)

	emph_lines = {"current" : [], "future" : []}
	normal_lines = {"current" : [], "future" : []}
	fh = None

	r_hex = {'current' : {},
			'future' : {}}

	if h.moving:
		r_hex['reading'] = {}
		r_hex['reading']['current'] = {}
		r_hex['reading']['future'] = {}

		if h.moving >= 3:
			fh = h.resolve()

		if h.moving == 1:
			add_lines(normal_lines['current'], h.moving_pos[0])
		elif h.moving == 2:
			add_lines(emph_lines['current'], h.moving_pos[1])
			add_lines(normal_lines['current'], h.moving_pos[0])
		elif h.moving == 3:
			add_lines(emph_lines['current'], h.moving_pos[1])
			add_lines(normal_lines['current'], h.moving_pos[0], h.moving_pos[2])

	r_hex['current'] = hex_header(h)

	if normal_lines['current'] or emph_lines['current']:
		r_hex['reading']['current']['name'] = h.info['name']
		if normal_lines['current']:
			r_hex['reading']['current']['normal_lines'] = normal_lines['current']

		if emph_lines['current']:
			r_hex['reading']['current']['emph_lines'] = emph_lines['current']

	if fh:
		r_hex['future'] = hex_header(fh)


	if normal_lines['future'] or emph_lines['future']:
		r_hex['reading']['future']['name'] = fh.info['name']

		if normal_lines['future']:
			r_hex['reading']['future']['normal_lines'] = normal_lines['future']

		if emph_lines['future']:
			r_hex['reading']['future']['emph_lines'] = emph_lines['future']

	return r_hex


if __name__ == '__main__':
	hexagram = hexagrams.YijingHexagram()

	while hexagram.moving != 3:
		hexagram = hexagrams.YijingHexagram()

	formatted_reading = format_reading(make_reading(hexagram))

	p = DFR0503()
	print_data(formatted_reading, p)
	p.feed(2)