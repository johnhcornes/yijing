#!/usr/bin/python3

import usb.core, usb.util
import time
from constants import *
from defaults import Defaults

def init_usb(vendor, product):
	"""Initialize USB device.

	Return interface object"""
	dev = usb.core.find(idVendor=vendor, idProduct=product)

	if not dev:
		raise ValueError("Device not found")

	#if device is in use by OS, detach so we can
	#use the interface
	if dev.is_kernel_driver_active(0):
		dev.detach_kernel_driver(0)

	dev.set_configuration()

	return dev

#this is just to wrap functions that are used as formatting options
#this is probably really shitty
#i'm learning okay
def formatter(f):
	def fmtr(*args, **kwargs):
		f(*args, **kwargs)
	return fmtr

class DFR0503:
	"""Print things with DFR0503 Thermal Printer"""


	def __init__(self, idVendor=0x0fe6, idProduct=0x811e):

		self.dev = init_usb(idVendor, idProduct)

		self.cfg = self.dev.get_active_configuration()
		#set intf to first interface in configuration
		self.intf = self.cfg[(0, 0)]



		#find the first endpoint marked as OUTPUT
		ep_out = usb.util.find_descriptor(self.intf, 
										custom_match = \
										lambda e: \
										usb.util.endpoint_direction(e.bEndpointAddress) == \
										usb.util.ENDPOINT_OUT)

		ep_in = usb.util.find_descriptor(self.intf, 
										custom_match = \
										lambda e: \
										usb.util.endpoint_direction(e.bEndpointAddress) == \
										usb.util.ENDPOINT_IN)

		#set up shorter method names
		self._raw_write = ep_out.write
		self.read = ep_in.read

		time.sleep(0.5) #give printer time to wake up

		self.reset()

		#set heat times. The printer will set these automatically
		#based on voltage, but I want to do it manually to
		#ensure consistency in wait times
		self.set_heat_time(self._settings['heating_points'],
							self._settings['heating_time'],
							self._settings['heating_interval'])

	def to_bytes(self, data):

		"""Convert given data into bytes based on printer language
		settings"""

		if isinstance(data, (int, float, complex)):
			data = str(data)
		elif isinstance(data, bytes):
			return data
		elif isinstance(data, (bytearray, memoryview)):
			return bytes(data)

		return bytes(data, encoding=self._settings['encoding'] \
									if not self._settings['chinese_mode'] else 
									self._settings['chinese_format'])


	def _set_wait(self):
		"""Update wait settings based on heat parameters"""
		self._settings['wait'] = self._settings['base_wait'] + \
				((self._settings['heating_time'] * 10) / 1e6) + \
				((self._settings['heating_interval'] * 10) / 1e6)

	def _overheat_check(self):

		while self.is_overheat():
			print("Printer is running hot, waiting {} seconds".format(self.settings['overheat_sleep']))
			time.sleep(self.settings['overheat_sleep'])

	def _safe_write(self, data):
		"""Write to out endpoint. Check to make sure printer is
		ready, and that printer hasn't overheated."""

		for d in data:
			for i in range(1, self._settings['retries']+1):
				try:
					self._settings['written'] += self._raw_write(bytes([d]))
					time.sleep(self._settings['byte_wait'])
					break
				except usb.core.USBError:
					if i == self._settings['retries']:
						raise Exception("Max retries exceeded hotshot")
					continue

	def text(self, txt, nl=True, wrap=True, *args, **kwargs):
		"""Make printer print text"""

		def _by_char(text):
			for c in text:
				if self._settings['column'] >= self._settings['max_column']:
					self.feed()
					self._settings['column'] = self._settings['margin']
				
				if c == '\n':
					self.feed()
					self._settings['column'] = self._settings['margin']
					continue

				self._safe_write(self.to_bytes(c))
				self._settings['column'] += self._settings['char_width']

				
		#set formatting options
		fmt = []
		for k, v in kwargs.items():
			try:
				fn = getattr(self, k)
				fmt.append(fn)
			except AttributeError:
				continue

			if fn.__name__ == "fmtr":
				fn(v)

		if wrap:
			words = txt.strip().split(' ')

			for x, word in enumerate(words):
				# don't add space to last word
				if x < len(words) - 1:
					word += ' '

				# next word will put us over column limit for line
				#or word is longer than column
				if (len(word) * self._settings['char_width']) + \
				self._settings['column'] > self._settings['max_column']\
				and not len(word) * self._settings['char_width'] > self._settings['max_column']:
					self.feed()

				_by_char(word)
		else:
			_by_char(txt)

		if nl:
			self.feed()

		#unset formatting options
		for fn in fmt:
			fn()
	
	@formatter
	def set_alignment(self, j=ALIGNMENTS.L):
		if isinstance(j, ALIGNMENTS):
			self._send_cmd(COMMANDS.ALIGN, j.value)

		self._settings['alignment'] = j.value

	@formatter
	def set_margin(self, n=0):
		"""Set margin to n chars wide"""
		self._send_cmd(COMMANDS.MARGIN, min(n, 47))
		self._settings['margin'] = min(n, 47)

	@formatter
	def set_height(self, s=1):
		"""Scale character height"""
		self._settings['char_height'] = s

		s = min((s - 1), 7)
		self._send_cmd(COMMANDS.CHRHEIGHT, s)

	@formatter
	def set_width(self, s=1):
		"""Scale character width"""
		self._settings['char_width'] = s if not self._settings['chinese_mode'] \
										else s * 2

		s = min((s-1) * 16, 112)
		self._send_cmd(COMMANDS.CHRHEIGHT, s)

	@formatter
	def set_inverse(self, on=False):
		"""Inverse print colors for text"""

		self._send_cmd(COMMANDS.INVERSE, int(on))
		self._settings['inverse'] = bool(on)

	@formatter
	def set_rotate(self, on=False):
		"""Rotate text 90 degrees"""

		self._send_cmd(COMMANDS.ROTATE, int(on))
		self._settings['rotate'] = bool(on)

	@formatter
	def set_alt_font(self, on=False):
		"""Toggle alternate font"""

		self._send_cmd(COMMANDS.FONT, int(on))
		self._settings['font_b'] = bool(on)

	@formatter
	def set_bold(self, on=False):
		"""Toggle bold print on and off"""

		self._send_cmd(COMMANDS.BOLD, int(on))
		self._settings['bold'] = bool(on)

	@formatter
	def set_spacing(self, s=0):
		"""Set spacing to right of each character"""

		self._send_cmd(COMMANDS.RIGHTSPACE, min(s, 255))
		self._settings['line_spacing'] = s

	@formatter
	def set_upsidedown(self, on=False):
		self._send_cmd(COMMANDS.UPSIDEDOWN, int(on))
		self._settings['upside_down'] = bool(on)

	@formatter
	def set_underline(self, u=0):
		u = min(u, 2)

		self._send_cmd(COMMANDS.UNDERLINE, u)
		self._settings['underline'] = u

	@formatter
	def set_chinese_mode(self, on=False):

		if on:
			self._send_cmd(COMMANDS.CHINESE_ON)
			#Chinese characters by default are twice as wide
			self._settings['char_width'] = self._settings['char_width'] * 2
		else:
			self._send_cmd(COMMANDS.CHINESE_OFF)
			self._settings['char_width'] = max(self._settings['char_width'] // 2, 1)

		self._settings['chinese_mode'] = bool(on)

	@formatter
	def set_chinese_format(self, fmt=CHINESE.GBK2312):
		if isinstance(fmt, CHINESE):
			self._send_cmd(COMMANDS.CHINESE_FORMAT, fmt.value[0])
			self._settings['chinese_format'] = fmt.value[1]

	def get_status(self):

		self._send_cmd(COMMANDS.STATUS)
		return self.read(1)[0]

	overheat_mask = 64
	def is_overheat(self):
		"""Check to see if printer has overheated (exceeded 60C)

		Return True if overheat
		Return False otherwise"""

		return self.get_status() & self.overheat_mask

	def _send_cmd(self, command, *args):
		"""Send a command to the printer. Must be a valid command
		as defined in COMMANDS"""
		if isinstance(command, COMMANDS):
			self._safe_write(bytes(command.value))
		elif isinstance(command, PREFIX):
			self._safe_write(bytes([command.value]))
		else:
			raise Exception("Invalid command")

		for arg in args:
			self._safe_write(bytes([arg]))

	def set_heat_time(self, hp=9, ht=80, hi=2):
		"""Set heating points, heatimg time, and heating interval"""
		self._send_cmd(COMMANDS.CHANGE_HEAT, hp, ht, hi)
		# self._safe_write(bytes([hp, ht, hi]))

		self._settings['heating_points'] = hp
		self._settings['heating_time'] = ht
		self._settings['heating_interval'] = hi

		self._set_wait()
		time.sleep(0.3) #this command takes a minute to sink in

	def feed(self, n=1):
		"""Feed by n char lines"""

		n = min(n, 255)

		self._send_cmd(COMMANDS.FEED, n)
		# self._safe_write(bytes([n]))

		self._settings['column'] = self._settings['margin']
		time.sleep(((self._settings['char_height'] * \
					self._settings['wait']) * n) + \
					self._settings['wait'] * self._settings['row_spacing'])

		#probably completely unnecessary but uhhhh hhh hhhhhh hhhahadhsjad
		self._overheat_check()


	def set_tabs(self, n=0, s=0):
		"""Set tab width and number of tabs"""

		n = min(n, 16)
		s = min(s, 46)

		if n and s:
			self._send_cmd(COMMANDS.SETTABS, *[t for t in range(s, (s*n)+s, s)], 0)
		else:
			self._send_cmd(COMMANDS.SETTABS, 0)

		self._settings['tab'] = s

	@formatter
	def tab(self, n=1):
		"""Tab n times"""
		for i in range(n):
			self._send_cmd(COMMANDS.TAB)

		self._settings['column'] += self._settings['tab'] - 1
		if self._settings['column'] >= self._settings['max_column']:
			self._settings['column'] = self._settings['margin']

	def set_row_spacing(self, s=32):
		"""Set row spacing"""
		s = min(s, 255)
		self._send_cmd(COMMANDS.ROWSPACING, s)
		self._settings['row_spacing'] = s

	def bitmap(self, w, h, data):
		"""Print a bitmap

		w, h are width and height in pixels, respectively"""

		width = (w + 7) // 8 #round up to nearest byte
		clipped = min(width, 48)

		i = 0
		for chunk in range(0, h, 255):

			chunk_height = min((h - chunk), 255)

			self._send_cmd(COMMANDS.BITMAP, clipped, 0, chunk_height, 0)
			# self._safe_write(bytes([clipped, 0, chunk_height, 0]))


			buf = []
			for _ in range(chunk_height):
				for _ in range(clipped):
					buf.append(data[i])
					i += 1
				i += (width - clipped)

			self._safe_write(buf)
			time.sleep(h * self._settings['wait'])
			self._overheat_check()

		self._send_cmd(PREFIX.LF)

	def reset(self):
		"""Reset printer to defaults"""
		self._settings = dict()

		for k, v in Defaults.items():
			self._settings[k] = v

		self._send_cmd(COMMANDS.INIT)
		#init doesn't clear print cache, this flushes it
		self._send_cmd(PREFIX.LF)

	def __repr__(self):
		info = ""
		for key, value in self._settings.items():
			info += "{} = {}\n".format(key, value)
		return info

	def __str__(self):
		return self.__repr__()

def print_data(data, printer):
	""" Print data using printer, data should be in Printing Format
	[
		{
		'type' : 'image' | 'text',
		'info' : 'some stuff' | '0b000100010101010',
		'options' : {'set_bold' : True, ...}
		},
		...,
		{...}
	]
	"""

	for item in data:
		if item['type'] == 'text':
			printer.text(item['info'], **item['options'])
		elif item['type'] == 'image':
			printer.bitmap(item['info'], item['options'])
