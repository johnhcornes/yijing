#!/usr/bin/python3
#coding=utf-8

import unittest
from printer import *
from constants import ALIGNMENTS

class PrinterTests(unittest.TestCase):
	pr = DFR0503()


	def test_text(self):
		self.pr.text("Here is a text printing test with word wrapping on.")
		self.pr.text("Here is a text printing test with word wrapping off.", wrap=False)

	def test_tabs(self):
		self.pr.text("Tabs on (clap clap)")
		self.pr.set_tabs(16, 4)
		for i in range(16):
			self.pr.text(str(i), nl=False)
			self.pr.tab()

		self.pr.text("Tabs off (clap clap clap)")
		self.pr.set_tabs()
		for i in range(16):
			self.pr.text(str(i), nl=False)
			self.pr.tab()
		self.pr.feed()

	def test_row_space(self):
		self.pr.set_row_spacing(64)
		self.pr.text("This is")
		self.pr.text("Double row spacing boys")
		self.pr.set_row_spacing(0)
		self.pr.text("This isn't")
		self.pr.text("Double row spacing boys")

	def test_bmp(self):
		self.pr.text("Width = 192, Height = 127")
		data = [0xff if x%2==0 else 0x00 for x in range(24*127)]
		self.pr.bitmap(192, 127, data)

		self.pr.text("Width = 384, Height = 255")
		data = [0xff if x%2==0 else 0x00 for x in range(48*255)]
		self.pr.bitmap(384, 255, data)

		self.pr.text("Width = 384, Height = 510")
		data = [0xff if x%2==0 else 0x00 for x in range(48*510)]
		self.pr.bitmap(384, 510, data)

		self.pr.text("Width = 385, Height = 255")
		data = [0xff if x%2==0 else 0x00 for x in range(49*255)]
		self.pr.bitmap(385, 255, data)

	def test_align(self):
		self.pr.set_alignment(ALIGNMENTS.R)
		self.pr.text("Right aligned")

		self.pr.set_alignment(ALIGNMENTS.M)
		self.pr.text("Middle aligned")

		self.pr.set_alignment()
		self.pr.text("Left aligned")

	def test_margin(self):
		for i in range(10):
			self.pr.set_margin(i)
			self.pr.text("{} char margin".format(i))
		self.pr.set_margin()

	def test_height(self):
		for i in range(1, 9):
			self.pr.set_height(i)
			self.pr.text("Tall Boy")
		self.pr.set_height()
		self.pr.text("Normal")

	def test_width(self):
		for i in range(1, 9):
			self.pr.set_width(i)
			self.pr.text("Wide")
		self.pr.set_width()
		self.pr.text("Normal")

	def test_inverse(self):
		self.pr.set_inverse(True)
		self.pr.text("Inverted")
		self.pr.set_inverse()
		self.pr.text("Normal")

	def test_rotate(self):
		self.pr.set_rotate(True)
		self.pr.text("Rotated text lol")
		self.pr.set_rotate()
		self.pr.text("Normal")

	def test_font(self):
		self.pr.set_alt_font(True)
		self.pr.text("Alternative font")
		self.pr.set_alt_font()
		self.pr.text("Normal")

	def test_bold(self):
		self.pr.set_bold(True)
		self.pr.text("Bold text")
		self.pr.set_bold()
		self.pr.text("Normal")

	def test_upsidedown(self):
		self.pr.set_upsidedown(True)
		self.pr.text("Upside down")
		self.pr.set_upsidedown(False)
		self.pr.text("Normal")

	def test_underline(self):
		self.pr.set_underline(1)
		self.pr.text("Underline 1")
		self.pr.set_underline(2)
		self.pr.text("Underline 2")
		self.pr.set_underline()
		self.pr.text("Normal")

	def test_chinese(self):
		self.pr.set_chinese_mode(True)
		self.pr.text("你好我是汉字")
		self.pr.set_chinese_format(CHINESE.UTF8)
		self.pr.text("你好我是汉字")
		self.pr.set_chinese_format(CHINESE.BIG5)
		self.pr.text("你好我是漢子") #doesn't actually seem to work
		self.pr.set_chinese_mode()		
		self.pr.text("你好我是汉字")
		self.pr.text("^ That should be garbled")

	def tearDown(self):
		self.pr.reset()
		self.pr.text("-"*32)



if __name__ == '__main__':
	unittest.main()