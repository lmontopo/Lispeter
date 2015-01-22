from Lisp_Interpreter.lisp_interpreter import parse, tokenizer
import unittest 


class TestParser(unittest.TestCase):
	def test_parser(self):
		self.assertEqual(parse(tokenizer('(list)(list)')), [['list'],['list']])
	