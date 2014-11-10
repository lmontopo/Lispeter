from interpreter.lisp_interpreter import *
import unittest 

class Test_Entire(unittest.TestCase):
	
	def test_math(self):
	 	self.assertEqual(interpret_ft('4'), float(4))
		self.assertEqual(interpret_ft('4 6'), float(6))
		self.assertEqual(interpret_ft('(+ 3 2)'), float(5))
		self.assertEqual(interpret_ft('(- 3 2)'), float(1))
		self.assertEqual(interpret_ft('(* 3 2)'), float(6))
		self.assertEqual(interpret_ft('(/ 9 2)'), float(4.5))
		self.assertEqual(interpret_ft('(+ 1 1 1 1)'), float(4))

	def test_map(self):
		self.assertEqual(interpret_ft('(map abs (list 1 -2 -3))'), [1.0, 2.0, 3.0])

	
	def test_bool(self):
		self.assertEqual(interpret_ft('(< 10 20)'), True)
		self.assertEqual(interpret_ft('(> 10 20)'), False)
		self.assertEqual(interpret_ft('(= 3 2)'), False)
		self.assertEqual(interpret_ft('(= 3 3)'), True)
		self.assertEqual(interpret_ft('(not (< 10 (- 20 10)))'), True)
		self.assertEqual(interpret_ft('(< 0 1 2 3)'), True)

	def test_abs(self):
		self.assertEqual(interpret_ft('(abs -1)'), float(1))
		#self.assertRaises(abs_error)
	
	def test_quote(self):
		self.assertEqual(interpret_ft('(quote hello2world)'), 'hello2world')
		with self.assertRaises(MyError):
			interpret_ft('(quote 12 34)')
	
	def test_list(self):
		self.assertEqual(interpret_ft('(list 1 2 3)'), [1.0, 2.0, 3.0])
		self.assertEqual(interpret_ft('(list 1 2 (list 3 4))'), [1.0, 2.0, [3.0, 4.0]])
	
	def test_def(self):
		self.assertEqual(interpret_ft('(define (f x)(+ x 2))'), None)
		self.assertEqual(interpret_ft('(define (function x y) (+ x y)) (function 4 4)'), float(8))
		self.assertEqual(interpret_ft('(define (func x)(+ x 1))(func 1)'), float(2))
		self.assertEqual(interpret_ft('(define x 3) (+ x 2)'), float(5))
		self.assertEqual(interpret_ft('(define blah 4) blah'), float(4))
		self.assertEqual(interpret_ft('(define x 3)(define x 4) x'), float(4))

	def test_if(self):
		self.assertEqual(interpret_ft('(if (< 10 20) 11 12)'), float(11))
		#THE FOLLOWING SHOULD RAISE AN ERROR! BUT I"M NOT SURE HOW TO DO IT!
		#self.assertRaises(MyError, interpret_ft('(if (< 1 1) (+ 1 1) ((set! x 5) x))'))

	def test_cond(self):
		self.assertEqual(interpret_ft("(cond ((> 0 0) 1)(else 'bloo))"), "bloo")
	
	def test_lambda(self):
		self.assertEqual(interpret_ft('((lambda (x y) (+ x y)) 5 6)'), float(11))
		self.assertEqual(interpret_ft('((lambda (y) 42 (* y 2)) 3)'), float(6))
	
	def test_def_and_lambda_combination(self):
		self.assertEqual(interpret_ft('(define add3 (lambda (x) (+ x 3))) (add3 3)'), float(6))

	def test_let(self):
		self.assertEqual(interpret_ft('(let ((x 3)) x)'), float(3))
		self.assertEqual(interpret_ft('(let ((x 1)(y 1)) (* x y))'), float(1))
		self.assertEqual(interpret_ft('(let ((a 4) (b 3))(let ((a (* a a))(b (* b b)))(+ a b)))'), float(25))

	def test_set(self):
		self.assertEqual(interpret_ft('(define x 3)(set! x 4) x'), float(4))

	def test_if_handles_recursion(self):
		self.assertEqual(interpret_ft('(define (fib n) (cond ((= n 0) 0) ((= n 1) 1)'
						+ '(else (+ (fib (- n 1)) (fib (- n 2)))))) (fib 10)'), float(55))

	def test_begin(self):
		self.assertEqual(interpret_ft('(if (< 1 1) (+ 1 1) (begin (define x 3) x))'), float(3))


	
	