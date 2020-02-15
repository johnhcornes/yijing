from thermal_printer.printer import *
from thermal_printer.constants import ALIGNMENTS
import hexagrams
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

		if is_chinese(line):
			line_template.update(FORMAT['chinese_defualt'])

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
				print_data.append(make_line(YiJingLineTrans[line], options))

		elif k is "emph_lines" or k is "normal_lines":
			for line in v:
				print_data.append(make_line(line, options))

		else:
			print_data.append(make_line(v, options))
		
		print_data.append(make_line("", {}))

	return print_data

def make_reading(hexa):
	r_hex = {}
	info = hexa.info

	r_hex['name'] = info['name']
	r_hex['name_chinese'] = info['name_chinese']

	r_hex['judgement'] = info['judgement']
	r_hex['judgement_chinese'] = info['judgement_chinese']

	r_hex['image'] = info['image']
	r_hex['image_chinese'] = info['image_chinese']

	return r_hex


if __name__ == '__main__':
	hexagram = hexagrams.YijingHexagram()

	formatted_reading = format_reading(make_reading(hexagram))

	p = DFR0503()
	print_data(formatted_reading, p)
	p.feed(2)