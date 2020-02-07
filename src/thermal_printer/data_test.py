from printer import *
from constants import ALIGNMENTS

""" Test printing data with print_data """

data = [
	{'type':'text', 'info': 'Qian(乾)', 
	'kwoptions' : {'set_bold' : True, 'set_alignment' : ALIGNMENTS.M}}
]

if __name__ == '__main__':
	p = DFR0503()
	print_data(data, p)