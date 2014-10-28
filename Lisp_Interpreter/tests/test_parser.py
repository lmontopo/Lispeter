from interpreter.lisp_interpreter import *
import unittest 


class TestParser(unittest.TestCase):
	def test_parser(self):
		self.assertEqual(parse(tokenizer('(list)(list)')), [['list'],['list']])
	