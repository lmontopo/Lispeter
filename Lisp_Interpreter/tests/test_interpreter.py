from interpreter.lisp_interpreter import *
import unittest 



class Test_Entire(unittest.TestCase):
	
	def test_math(self):
	 	self.assertEqual(interpret('4'), float(4))
		self.assertEqual(interpret('4 6'), float(6))
		self.assertEqual(interpret('(+ 3 2)'), float(5))
		self.assertEqual(interpret('(- 3 2)'), float(1))
		self.assertEqual(interpret('(* 3 2)'), float(6))
		self.assertEqual(interpret('(/ 9 2)'), float(4.5))
	
	def test_bool(self):
		self.assertEqual(interpret('(< 10 20)'), True)
		self.assertEqual(interpret('(> 10 20)'), False)
		self.assertEqual(interpret('(= 3 2)'), False)
		self.assertEqual(interpret('(= 3 3)'), True)
		self.assertEqual(interpret('(not (< 10 (- 20 10)))'), True)
	
	def test_abs(self):
		self.assertEqual(interpret('(abs -1)'), float(1))
	
	def test_quote(self):
		self.assertEqual(interpret('(quote hello2world)'), 'hello2world')
	
	def test_list(self):
		self.assertEqual(interpret('(list 1 2 3)'), [1.0, 2.0, 3.0])
	
	def test_def(self):
		self.assertEqual(interpret('(define (f x)(+ x 2))'), None)
		self.assertEqual(interpret('(define (function x y) (+ x y)) (function 4 4)'), float(8))
		self.assertEqual(interpret('(define (func x)(+ x 1))(func 1)'), float(2))

	# def test_if(self):
	# 	self.assertEqual(interpret('(if (< 10 20) 11 12)'), float(11))

	def test_cond(self):
		self.assertEqual(interpret("(cond ((> 0 0) 1)(else 'bloo))"), "bloo")
	
	
	#def test_def_lambda(self):
	#	self.assertEqual(interpret('((define add3 (lambda (x) (+ x 3))) (add3 3))'), float(6))

	
	